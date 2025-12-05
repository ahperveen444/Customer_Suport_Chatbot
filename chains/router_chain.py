from langchain_core.runnables import RunnableLambda, RunnableBranch
from services.db_service import get_order
from services.llm_service import model, str_parser
from prompts.prompt_normal import prompt_normal
from prompts.prompt_order import prompt_order
from prompts.prompt_irrelevant import prompt_irrelevant

def orderID(x):
    return get_order(x["order_id"])

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
    (
        lambda x: x["intent"] == "order_id",
        RunnableLambda(orderID) 
        | prompt_order
        | model
        | str_parser
    ),
    (
        lambda x: x["intent"] == "irrelevant",
        prompt_irrelevant 
        | model 
        | str_parser
    ),
    RunnableLambda(lambda x: "Sorry for inconvenience please try again later!")
)
