from langchain_core.prompts import PromptTemplate
from services.llm_service import pydantic_parser

prompt_intention = PromptTemplate(
    template="""
Classify the customer's message into one of three intents:

1. normal  
   - Questions about company, services, pricing, FAQs, features, support, or general information about what we offer.

2. order_id  
   - Questions about their order, delivery status, tracking.
   - If an order ID is mentioned, extract it. Else order_id = 0.

3. irrelevant  
   - Greetings, small talk, weather, jokes, news, personal questions.

User message: {query}

Follow this JSON format:
{format}
""",
    input_variables=['query'],
    partial_variables={'format': pydantic_parser.get_format_instructions()}
)
