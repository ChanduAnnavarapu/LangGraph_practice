from langchain_groq import ChatGroq
from typing import TypedDict, Annotated, List
from langgraph.graph import StateGraph, START, END
from langchain_core.messages import AIMessage, HumanMessage, BaseMessage, SystemMessage
from langgraph.graph.message import add_messages
from pydantic import BaseModel, Field
from langgraph.checkpoint.memory import InMemorySaver
from dotenv import load_dotenv
import os

load_dotenv()

model = ChatGroq(model=os.getenv("MODEL_NAME"),
                 api_key=os.getenv("API_KEY"),
                 temperature=0.1)

class ChatState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]


def chat_node(state: ChatState):
  """you are chat model to respond to user queries"""
  result=model.invoke(state['messages'])
  return {"messages":result}


checkpointer=InMemorySaver()
graph=StateGraph(ChatState)

graph.add_node("chat_node",chat_node)

graph.add_edge(START, "chat_node")
graph.add_edge("chat_node", END)

chatbot=graph.compile(checkpointer=checkpointer)

for message_chunk,metadata in chatbot.stream(
    {'messages':[HumanMessage(content="write 100 word essay on AI")]},
    config={'configurable':{'thread_id':'thread_1'}},
    stream_mode='messages'):
    if message_chunk.content:
        print(message_chunk.content, end=" ", flush=True)