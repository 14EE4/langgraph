from typing import TypedDict, List

from langgraph.graph import StateGraph

class Statement(TypedDict):
    messages: List[str]

builder = StateGraph(Statement)


def say_hello(state: Statement) -> Statement:
    #state['messages'].append('Hello!')
    print("say_hello node called")
    return {
        "messages": ["hello, "]
    }

def say_world(state: Statement) -> Statement:
    #state['messages'].append('World!')
    print("say_world node called")
    return {
        "messages": ["world!"]

    }


builder.add_node("hello_node", say_hello) #alias
builder.add_node("world_node", say_world)
from langgraph.graph import START, END
builder.add_edge(START, "hello_node")
builder.add_edge("hello_node", "world_node")
builder.add_edge("world_node", END)

graph = builder.compile()

graph.invoke({
    "messages": []
})