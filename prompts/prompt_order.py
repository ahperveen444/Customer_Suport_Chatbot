from langchain_core.prompts import PromptTemplate

prompt_order = PromptTemplate(
    template="""
Give a one-line response about the customer's order.

Order Details:
{orderID}
""",
    input_variables=['orderID']
)
