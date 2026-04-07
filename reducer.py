from typing import TypedDict, List, Annotated
from operator import add
class Statement(TypedDict):
    
    data: str
    execution_path: Annotated[List[str], add]

def node_a(state: Statement) -> Statement:
    print("node_a called")

    print(f"Current state: {state}")
    return {

        "data": state["data"],
        "execution_path": ["node_a"]
    }

def node_b(state: Statement) -> Statement:
    print("node_b called")
    print(f"Current state: {state}")
    return {

        "data": state["data"],
        "execution_path": ["node_b"]

    }

def node_c(state: Statement) -> Statement:
    print("node_c called")
    print(f"Current state: {state}")
    return {

        "data": state["data"],
        "execution_path": ["node_c"]
    }

def node_d(state: Statement) -> Statement:
    print("node_d called")
    print(f"Current state: {state}")
    return {

        "data": state["data"],
        "execution_path": ["node_d"]
    }

def should_continue(state: Statement):
    print(f"Checking if should continue with state: {state}")
    if "go_c" in state['data']:
        print("Continuing to node_c")
        return "node_c"
    else:
        print("go to node_d")
        return "node_d"
from langgraph.graph import StateGraph, START, END
builder = StateGraph(Statement)
builder.add_node(node_a)
builder.add_node(node_b)
builder.add_node(node_c)
builder.add_node(node_d)
builder.add_edge(START, "node_a")
builder.add_edge("node_a", "node_b")
builder.add_conditional_edges(
    source="node_b", 
    path=should_continue
)
builder.add_edge("node_c", END)
builder.add_edge("node_d", END)
graph = builder.compile()

test1_args = {
    "data": "Initial data",
    "execution_path": []
}
test2_args = {
    "data": "Initial data with go_c",
    "execution_path": []
}
result1 = graph.invoke(test1_args)
result2 = graph.invoke(test2_args)    

print("Result 1:", result1)
print("Result 2:", result2)

for node in result1['execution_path']:
    print(f"{node}", end=" -> ")

print("\n")
for node in result2['execution_path']:
    print(f"{node}", end=" -> ")