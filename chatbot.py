import json,os
import numpy as np
from langchain_openai import OpenAIEmbeddings,ChatOpenAI
from langchain_core.prompts import PromptTemplate
from langchain_community.document_loaders import PyPDFLoader,DirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.output_parsers import StrOutputParser,PydanticOutputParser
from langchain_core.runnables import RunnableBranch, RunnableLambda
from pydantic import BaseModel, Field
from typing import Literal
from supabase import create_client
from langchain_core.messages import HumanMessage, AIMessage
from dotenv import load_dotenv

load_dotenv()




# schema of Intention of Customer Question
class IntentionSchema(BaseModel):
    intent : Literal['normal','irrelevant','order_id'] = Field(description="Give the intent of customer query")
    order_id : int = Field(description = "Return the order id from the query. For example customer asks what is the status of my order as my order id is 1, return order_id = 1. If order id is not given then return 0")

# database
supabase = create_client(os.getenv("SUPABASE_URL"), os.getenv("SUPABASE_API_KEY"))

# models
model = ChatOpenAI(model = "gpt-4o-mini")
embedding_model = OpenAIEmbeddings(model = "text-embedding-3-small")

# parsers
str_parser = StrOutputParser()
pydantic_parser = PydanticOutputParser(pydantic_object = IntentionSchema)

# load embeddings
def load_embeddings(file_path="data/vector_backup/embedding_backup.json"):

    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Prepare text + vectors pairs
    text_embeddings = []
    metadatas = []

    for item in data:
        vector = np.array(item["vector"], dtype=np.float32)
        text_embeddings.append((item["text"], vector))
        metadatas.append(item["metadata"])

    # Build FAISS vector store WITHOUT re-embedding
    vector_store = FAISS.from_embeddings(
        text_embeddings=text_embeddings,
        embedding=embedding_model,
        metadatas=metadatas
    )

    # print statement to check for load embeddings

    # print(f"Loaded {len(text_embeddings)} embeddings from {file_path} (NO cost)")
    return vector_store



# Prompts


# Prompt for intention

prompt_intention = PromptTemplate(
    template = """
Classify the customer's message into one of three intents:

1. normal  
   - Questions about company, services, pricing, FAQs, features, support, or general information about what we offer.

2. order_id  
   - Questions asking about their order, delivery status, tracking, or order details.
   - If an order ID is mentioned, extract it.
   - If not mentioned, return order_id = 0.

3. irrelevant  
   - Greetings (hi, hello, how are you)
   - Small talk (who are you, tell me a joke, weather, news, personal questions)
   - Anything not related to company services or order details.

User message: {query}
Follow the following format:
{format}
""",
input_variables=['query'],
partial_variables={'format' : pydantic_parser.get_format_instructions()}
)


# Prompt for normal

prompt_normal = PromptTemplate(
    template = """
You are a helpful customer support assistant. Use the context below (delimited by <<CONTEXT>>) to answer the user question.
When customer asks about services just answer with the names of all the services only, provide the details when customer asks about details.
If you cannot answer from context, say "I can only answer questions about our services and your order details.". Keep answers short. <<CONTEXT>> {retrieved_chunks} <</CONTEXT>> User question: {query}

""",
input_variables=['query','retrieved_chunks']
)



# Prompt for order

prompt_order = PromptTemplate(
    template = """
You have to just give a one line response to the customer about his order details. Here is the order details:
{orderID}
"""
)

# Prompt for irrelevant

prompt_irrelevant = PromptTemplate(
    template="""
You are a helpful and polite Customer Support Assistant.
If the customer greets you just simply reply "How I can assist you?"
If customer asks irrelevant/personal/general questions, reply:
“I am a Customer Support Assistant. Please ask me questions related to our services.
""",
)


# loading the saved embeddings
vector_store = load_embeddings()


# retrieve the chunks from vector stores
retriever = vector_store.as_retriever(search_kwargs = {'k':4})



# query = input("Enter : ")
# retrieved_chunks = retriever.invoke(query)


# for i,doc in enumerate(retrieved_chunks):
#     print(f"Result {i+1}: {doc.page_content}")

intention_chain = prompt_intention | model | pydantic_parser 
# result = intention_chain.invoke({'query':query})
# print(result)

# wrapped = {
#     "intent": result.intent,
#     "order_id": result.order_id,
#     "query": query,
#     "retrieved_chunks": retrieved_chunks
# }

# Function for OrderID
def get_order(order_id):
    if(order_id == 0):
        return {"orderID": "Please provide your Order Id to know details"}
    
    response = supabase.table("orders").select("*").eq("id", order_id).single().execute()
    data = response.data
    if data is None:
        return {"orderID": f"No order found for this Order ID : {order_id}"}
    return {"orderID": json.dumps(data)}

orderID = RunnableLambda( lambda x : get_order(x["order_id"]))

# Chain Branching
branch_chain = RunnableBranch(
     (
        lambda x: x["intent"] == "normal",
        RunnableLambda(lambda x: {
            "query": x["query"],
            "retrieved_chunks": x["retrieved_chunks"]
        }) 
        | prompt_normal 
        | model 
        | str_parser
    ),
    (lambda x : x["intent"] == "order_id",
    orderID
    | prompt_order
    | model
    | str_parser
    ),
    (lambda x : x["intent"] == "irrelevant", prompt_irrelevant | model | str_parser),
    RunnableLambda(lambda x : "Sorry for inconvenience please try again later!")
)



# chain = branch_chain 

# final = chain.invoke(wrapped)
# print(final)


# Chat Loop 

# conversation history

conversation_history = []

while True:
    query = input("User : ")

    conversation_history.append(HumanMessage(content = query))
    
    if(query.lower() == "exit"):
        break

    retrieved_chunks = retriever.invoke(query)

    # get intention
    result = intention_chain.invoke({"query": query})

    wrapped = {
        "intent": result.intent,
        "order_id": result.order_id,
        "query": query,
        "retrieved_chunks": retrieved_chunks
    }

    # final result
    final = branch_chain.invoke(wrapped)
    print("Chatbot : ",final)
    conversation_history.append(AIMessage(content = final))

# print("CHAT HISTORY : ",conversation_history)