from langchain_openai import ChatOpenAI
from langchain_core.output_parsers import StrOutputParser, PydanticOutputParser
from schemas.intention_schema import IntentionSchema
from config.settings import CHAT_MODEL

model = ChatOpenAI(model=CHAT_MODEL)
str_parser = StrOutputParser()
pydantic_parser = PydanticOutputParser(pydantic_object=IntentionSchema)
