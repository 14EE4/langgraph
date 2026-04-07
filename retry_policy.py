#from langgraph
from typing import TypedDict, List, Annotated
import random

from langgraph.graph import StateGraph
from langgraph.types import RetryPolicy

class PaymentState(TypedDict):
    user_id: str
    amount: int
    payment_status: str
    error_message: str

class PaymentException(Exception):
    pass

def process_payment(state: PaymentState) -> PaymentState:
    print(f"Processing payment...{state['amount']}won")

    if random.random() < 0.5:  # Simulate a 50% chance of payment failure
        print("Payment failed due to a random error.")
        raise PaymentException("Random payment processing error")
    print("Payment succeeded.")
    return {
        "payment_status": "Success",
        "error_message": ""
    }

def success_handler(state: PaymentState) -> PaymentState:
    print("Handling successful payment.")
    return {
        "payment_status": "Success"
    }

def failure_handler(state: PaymentState) -> PaymentState:
    print("Handling failed payment. -> fallback")
    return {
        "payment_status": "Failed",
        "error_message": "모든 재시도 실패..."
    }

builder = StateGraph(PaymentState)
builder.add_node(
    "process_payment", 
    process_payment, 
    retry_policy=RetryPolicy(
        max_attempts=3, 
        initial_interval=1,
        backoff_factor=2,
        jitter=True,
        retry_on=PaymentException
    )
)
builder.add_node("success_handler", success_handler)
builder.add_node("failure_handler", failure_handler)

from langgraph.graph import START, END
builder.add_edge(START, "process_payment")
builder.add_edge(
    "process_payment", "success_handler")
#builder.add_edge("process_payment", "failure_handler")
builder.add_edge("success_handler", END)    
builder.add_edge("failure_handler", END)

graph = builder.compile()
initial_state = {
    "user_id": "user123",
    "amount": 10000,
    "payment_status": "",
    "error_message": ""
}
try:
    final_state = graph.invoke(initial_state)
    print("최종 상태:", final_state)
except Exception as e:
    print(f"결제 처리 중 예외 발생: {e}")
final_state = graph.invoke(initial_state)
print("최종 상태:", final_state)