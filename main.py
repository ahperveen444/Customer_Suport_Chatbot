from services.vector_service import load_embeddings
from services.llm_service import model, pydantic_parser
from prompts.prompt_intention import prompt_intention
from chains.router_chain import branch_chain
from utils.history import add_user_message, add_ai_message
from langchain_core.runnables import RunnableLambda
from langchain_core.messages import HumanMessage
from services.vector_service import load_embeddings
from langchain_core.output_parsers import StrOutputParser

# Load vector store
vector_store = load_embeddings()
retriever = vector_store.as_retriever(search_kwargs={'k': 4})

# Intention chain
intention_chain = prompt_intention | model | pydantic_parser

print("Customer Support Chatbot Running...\n")

while True:
    query = input("User: ")

    if query.lower() == "exit":
        break

    add_user_message(query)
    retrieved_chunks = retriever.invoke(query)

    result = intention_chain.invoke({"query": query})

    wrapped = {
        "intent": result.intent,
        "order_id": result.order_id,
        "query": query,
        "retrieved_chunks": retrieved_chunks
    }

    final = branch_chain.invoke(wrapped)

    print("Chatbot:", final)
    add_ai_message(final)
