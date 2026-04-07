from typing import TypedDict

class TypedDictState(TypedDict):
    query: str
    answer: int

from langgraph.graph import StateGraph
builder = StateGraph(TypedDictState)

