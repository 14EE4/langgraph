from typing import TypedDict

class OrderState(TypedDict):
    order_amount: int
    discount_applied: bool
    final_price: int
    message: str