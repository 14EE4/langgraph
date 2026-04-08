from langchain_core.tools import tool

@tool
def get_weather(city: str) -> str:
    """도시의 날씨를 반환하는 도구입니다.
    
    Args:
        city (str): 날씨를 알고 싶은 도시의 이름입니다.
        
    Returns:
        str: 해당 도시의 현재 날씨 정보입니다.
    """

    weather_data={
        "Seoul": "맑음, 25°C",
        "New York": "흐림, 22°C",
        "Tokyo": "비, 28°C",
        "Paris": "맑음, 20°C"
    }

    return weather_data.get(city, "도시 이름이 잘못되었거나 날씨 정보를 찾을 수 없습니다.")

@tool
def calculate_tax(total_amount: int, tax_rate: int) -> int:
    """전체 계산 금액과 해당 금액의 백분율에 해당하는 세금을 계산하는 도구입니다.
    
    Args:
        total_amount (int): 전체 계산 금액입니다.
        tax_rate (int): 세금 비율입니다.
        
    Returns:
        int: 계산된 세금 금액입니다.
    """
    
    
    tax = total_amount * (tax_rate / 100)
    
    
    return tax

from dotenv import load_dotenv

from langchain_groq import ChatGroq

load_dotenv()

llm = ChatGroq(
    model="opanai/gpt-oss-20b",
    temperature=0.7,
)

llm_with_tools = llm.bind_tools([
    get_weather, 
    calculate_tax
])


