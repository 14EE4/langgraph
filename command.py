from typing import TypedDict, Literal
from langgraph.types import Command

class OrderState(TypedDict):
    order_amount: int# 주문 금액
    discount_applied: bool
    final_price: int# 최종 가격
    message: str

def check_order_node(state: OrderState) -> Command[Literal["apply_discount_node", "no_discount_node"]]:
    """
    금액 검사 노드
    """

    amount = state['order_amount'] 

    if amount > 100_000:
        print("고액 주문자입니다. 할인 적용!")
        return Command(
            update = {
                "message": "할인 대상입니다."
            },
            goto = "apply_discount_node"
        )
    else:
        print("일반 주문자입니다. 할인 미적용.")
        return Command(
            update = {
                "message": "할인 대상이 아닙니다."
            },
            goto = "no_discount_node"
        )
    
def apply_discount_node(state: OrderState) -> TypedDict:
    """
    할인 적용 노드
    """
    print("할인 적용 노드 실행")
    amount = state['order_amount']
    discount_amount = int(amount * 0.1) # 10% 할인
    final_price = amount - discount_amount

    print(f"할인 적용 후 최종 가격: {final_price}")

    return {
        "discount_applied" : True,
        "final_price" : final_price,
        "message" : f"10% 할인 적용 완료! 최종 가격은 {final_price}원입니다."
    }

def no_discount_node(state: OrderState) -> TypedDict:
    """
    할인 미적용 노드
    """
    print("할인 미적용 노드 실행")
    amount = state['order_amount']
    print(f"최종 가격: {amount}")

    return {
        "discount_applied" : False,
        "final_price" : amount,
        "message" : f"할인 적용되지 않았습니다. 최종 가격은 {amount}원입니다."
    }

from langgraph.graph import StateGraph, START, END
builder = StateGraph(OrderState)
builder.add_node("check_order_node", check_order_node)
builder.add_node("apply_discount_node", apply_discount_node)
builder.add_node("no_discount_node", no_discount_node)
builder.add_edge(START, "check_order_node")

builder.add_edge("apply_discount_node", END)
builder.add_edge("no_discount_node", END)

graph = builder.compile()
# 테스트 실행
initial_state = {
    "order_amount": 150_000
}
final_state = graph.invoke(initial_state)
print("최종 상태:", final_state)

state_2 = {
    "order_amount": 50_000
}
final_state_2 = graph.invoke(state_2)
print("최종 상태:", final_state_2)
