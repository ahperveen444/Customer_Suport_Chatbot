from langchain_core.messages import HumanMessage, AIMessage

conversation_history = []

def add_user_message(msg):
    conversation_history.append(HumanMessage(content=msg))

def add_ai_message(msg):
    conversation_history.append(AIMessage(content=msg))
