from langchain_groq import ChatGroq

from dotenv import load_dotenv
from typing import List, TypedDict
from langgraph.graph import StateGraph
from pydantic import BaseModel, Field

load_dotenv()   

llm=ChatGroq(
    model="openai/gpt-oss-20b",
)

class DevSupportState(TypedDict):
    developer_query: str
    query_category: str
    response: str
    tool_used: str

class DevQueryClassificationTool(BaseModel):
    category: Literal["bug","architecture","performance","devops","general"]
    confidence: float = Field(description="분류의 신뢰도 점수입니다. 0에서 1 사이의 값으로 표현됩니다. 소숫점 4자리까지 표현됩니다.")
    reasoning: str = Field(description="분류에 대한 자세한 설명입니다. 왜 해당 카테고리에 속하는지에 대한 근거를 포함해야 합니다.")

def classify_dev_query(state: DevSupportState) -> DevSupportState:
    """개발자 지원 쿼리를 분류하는 도구입니다.
    
    Args:
        state (DevSupportState): 개발자 지원 쿼리의 상태를 나타내는 객체입니다.
        
    Returns:
        DevSupportState: 쿼리 분류 결과가 포함된 상태 객체입니다.
    """
    print("개발자의 질문을 분석합니다...")
    
    classifier_llm = llm.with_structured_output(DevQueryClassificationTool)
    
    prompt = f"""
        당신은 시니어 풀스택 개발자입니다. 다음 개발자 지원 쿼리를 분석하여 적절한 카테고리로 분류하세요.
            - bug: 코드의 버그나 오류와 관련된 질문
            - architecture: 시스템 아키텍처, 설계 패턴, 기술 선택과 관련된 질문
            - performance: 성능 최적화, 병목 현상 분석과 관련된 질문
            - devops: 배포, CI/CD, 인프라 관리와 관련된 질문, 운영, 도커, 쿠버네티스, 클라우드 인프라, 환경 설정과 관련된 질문
            - general: 위의 카테고리에 속하지 않는 일반적인 개발 질문

        개발자 질문: {state['developer_query']}

        질문의 의도를 기준으로 적합한 카테고리를 선택하세요.
    """

    classification_result = classifier_llm.invoke(prompt)#devQueryClassificationTool 객체로 반환됩니다.

    print(f"분류 결과: {classification_result.category} (신뢰도: {classification_result.confidence:.4f})")
    print(f"분류 근거: {classification_result.reasoning}")

    return {

        "query_category": classification_result.category,

    }

def handle_bug(state: DevSupportState) -> DevSupportState:
    """버그 관련 질문을 처리하는 도구입니다.
    
    Args:
        state (DevSupportState): 개발자 지원 쿼리의 상태를 나타내는 객체입니다.
        
    Returns:
        DevSupportState: 버그 관련 질문에 대한 응답이 포함된 상태 객체입니다.
    """
    print("버그 관련 질문을 처리합니다...")
    
    prompt = f"""
        당신은 시니어 풀스택 개발자입니다. 다음 버그 관련 질문에 대한 응답을 작성하세요.
        개발자 질문: {state['developer_query']}
        질문에 대한 명확하고 구체적인 해결책을 제시하세요. 필요한 경우 코드 예시를 포함할 수 있습니다.

        반드시 다음 사항을 포함해야 합니다:
        - 오류 메시지 또는 증상을 바탕으로 가능한 원인을 분석합니다
        - 수정된 코드 예시 또는 해결 방법을 제시합니다.
        - 단계별 디버깅 방법을 구체적으로 제시합니다
        - 동일한 버그가 발생하지 않도록 예방 조치를 제안합니다

        코드 예시가 필요한 경우에는 명확하고 간결한 예시를 제공하세요. 예시 코드에는 주석을 포함하여 각 부분의 역할을 설명하세요.
    """

    response = llm.invoke(prompt).content

    print("디버깅 노드 처리 완료")
    return {
        "response": response,
        "tool_used": ["stack_trace_analyzer", "code_debugger","error_log_parser"]
    }

def handle_architecture(state: DevSupportState) -> DevSupportState:





    """아키텍처 관련 질문을 처리하는 도구입니다.
    
    Args:
        state (DevSupportState): 개발자 지원 쿼리의 상태를 나타내는 객체입니다.
        
    Returns:
        DevSupportState: 아키텍처 관련 질문에 대한 응답이 포함된 상태 객체입니다.
    """
    print("아키텍처 관련 질문을 처리합니다...")
    
    prompt = f"""
        당신은 소프트웨어 아키텍쳐  전문가입니다. 다음 아키텍처 관련 질문에 대한 응답을 작성하세요.
        개발자 질문: {state['developer_query']}
        질문에 대한 명확하고 구체적인 해결책을 제시하세요. 필요한 경우 시스템 다이어그램이나 코드 예시를 포함할 수 있습니다.

        반드시 다음 사항을 포함해야 합니다:
        - 시스템 요구사항 분석: 질문에서 제시된 요구사항을 바탕으로 시스템의 주요 구성 요소와 상호 작용을 분석합니다.
        - 설계 패턴 제안: 적절한 설계 패턴(예: MVC, 마이크로서비스, 이벤트 기반 아키텍처 등)을 제안하고, 그 이유를 설명합니다.
        - 기술 선택: 특정 기술 스택(프레임워크, 라이브러리, 데이터베이스 등)을 추천하고, 그 선택의 근거를 설명합니다.
        - 확장성 및 유지보수성 고려: 제안된 아키텍처가 확장성과 유지보수성을 어떻게 보장하는지 설명합니다.

        시스템 다이어그램이 필요한 경우에는 명확하고 간결한 다이어그램을 제공하세요. 다이어그램에는 각 구성 요소의 역할과 상호 작용이 명확하게 표시되어야 합니다.
    """

    response = llm.invoke(prompt).content

    print("아키텍처 노드 처리 완료")
    return {
        "response": response,
        "tool_used": ["system_diagram_generator", "design_pattern_recommender","technology_stack_analyzer"]
    }

def handle_performance(state: DevSupportState) -> DevSupportState:
    """성능 관련 질문을 처리하는 도구입니다.
    
    Args:
        state (DevSupportState): 개발자 지원 쿼리의 상태를 나타내는 객체입니다.
        
    Returns:
        DevSupportState: 성능 관련 질문에 대한 응답이 포함된 상태 객체입니다.
    """
    print("성능 관련 질문을 처리합니다...")
    
    prompt = f"""
        당신은 소프트웨어 성능 최적화 전문가입니다. 다음 성능 관련 질문에 대한 응답을 작성하세요.
        개발자 질문: {state['developer_query']}
        질문에 대한 명확하고 구체적인 해결책을 제시하세요. 필요한 경우 코드 예시나 성능 분석 도구 사용법을 포함할 수 있습니다.

        반드시 다음 사항을 포함해야 합니다:
        - 성능 문제 분석: 질문에서 제시된 성능 문제의 원인을 분석합니다. 가능한 병목 현상이나 비효율적인 코드 패턴을 식별합니다.
        - 최적화 전략 제안: 문제를 해결하기 위한 구체적인 최적화 전략(예: 알고리즘 개선, 캐싱, 병렬 처리 등)을 제안하고, 그 이유를 설명합니다.
        - 코드 예시 제공: 최적화된 코드 예시를 제공하여, 어떻게 개선할 수 있는지 보여줍니다. 예시 코드에는 주석을 포함하여 각 부분의 역할을 설명하세요.
        - 성능 분석 도구 추천: 문제를 지속적으로 모니터링하고 분석할 수 있는 적절한 성능 분석 도구(예: 프로파일러, 모니터링 툴 등)를 추천하고, 그 사용법을 간략히 설명합니다.
    """

    response = llm.invoke(prompt).content

    print("성능 노드 처리 완료")
    return {
        "response": response,
        "tool_used": ["performance_profiler", "code_optimizer","monitoring_tool_recommender"]
    }

def handle_devops(state: DevSupportState) -> DevSupportState:
    """DevOps 관련 질문을 처리하는 도구입니다.
    
    Args:
        state (DevSupportState): 개발자 지원 쿼리의 상태를 나타내는 객체입니다.
        
    Returns:
        DevSupportState: DevOps 관련 질문에 대한 응답이 포함된 상태 객체입니다.
    """
    print("DevOps 관련 질문을 처리합니다...")
    
    prompt = f"""
        당신은 DevOps 및 클라우드 인프라 전문가입니다. 다음 DevOps 관련 질문에 대한 응답을 작성하세요.
        개발자 질문: {state['developer_query']}
        질문에 대한 명확하고 구체적인 해결책을 제시하세요. 필요한 경우 CI/CD 파이프라인 구성 예시나 인프라 설정 방법을 포함할 수 있습니다.

        반드시 다음 사항을 포함해야 합니다:
        - 문제 분석: 질문에서 제시된 DevOps 문제의 원인을 분석합니다. 가능한 배포 실패 원인, 인프라 구성 오류, CI/CD 파이프라인 문제 등을 식별합니다.
        - 해결책 제안: 문제를 해결하기 위한 구체적인 해결책(예: 배포 스크립트 수정, 인프라 설정 변경, CI/CD 파이프라인 개선 등)을 제안하고, 그 이유를 설명합니다.
        - 예시 제공: 필요한 경우, CI/CD 파이프라인 구성 예시나 인프라 설정 방법을 제공하여, 어떻게 개선할 수 있는지 보여줍니다. 예시에는 주석을 포함하여 각 부분의 역할을 설명하세요.
        - 도구 추천: 문제를 지속적으로 모니터링하고 관리할 수 있는 적절한 DevOps 도구(예: Jenkins, GitHub Actions, Terraform 등)를 추천하고, 그 사용법을 간략히 설명합니다.
    """

    response = llm.invoke(prompt).content

    print("DevOps 노드 처리 완료")
    return {
        "response": response,
        "tool_used": ["ci_cd_pipeline_analyzer", "infrastructure_config_checker","devops_tool_recommender"]
    }

def handle_general(state: DevSupportState) -> DevSupportState:
    """일반 개발 질문을 처리하는 도구입니다.
    
    Args:
        state (DevSupportState): 개발자 지원 쿼리의 상태를 나타내는 객체입니다.
        
    Returns:
        DevSupportState: 일반 개발 질문에 대한 응답이 포함된 상태 객체입니다.
    """
    print("일반 개발 질문을 처리합니다...")
    
    prompt = f"""
        당신은 친절한 시니어 풀스택 개발자 멘토입니다. 다음 일반 개발 질문에 대한 응답을 작성하세요.
        개발자 질문: {state['developer_query']}
        질문에 대한 명확하고 구체적인 해결책을 제시하세요. 필요한 경우 코드 예시나 관련 문서 링크를 포함할 수 있습니다.

        반드시 다음 사항을 포함해야 합니다:
        - 문제 분석: 질문에서 제시된 문제의 원인을 분석합니다. 가능한 문제의 핵심을 파악하고, 관련된 개념이나 기술을 설명합니다.
        - 해결책 제안: 문제를 해결하기 위한 구체적인 해결책(예: 코드 수정, 라이브러리 사용, 학습 자료 추천 등)을 제안하고, 그 이유를 설명합니다.
        - 예시 제공: 필요한 경우, 코드 예시나 관련 문서 링크를 제공하여, 어떻게 개선할 수 있는지 보여줍니다. 예시에는 주석을 포함하여 각 부분의 역할을 설명하세요.
    """

    response = llm.invoke(prompt).content

    print("일반 개발 노드 처리 완료")
    return {
        "response": response,
        "tool_used": ["general_dev_advisor", "code_example_provider","documentation_link_recommender"]
    }

def route_by_dev_category(state: DevSupportState) -> DevSupportState:
    """개발자 지원 쿼리를 카테고리에 따라 적절한 처리 도구로 라우팅하는 함수입니다.
    
    Args:
        state (DevSupportState): 개발자 지원 쿼리의 상태를 나타내는 객체입니다.
        
    Returns:
        DevSupportState: 카테고리에 따른 처리 결과가 포함된 상태 객체입니다.
    """
    category = state.get("query_category")

    return category

from langgrapgh import StateGraph

builder = StateGraph(DevSupportState)

builder.add_node("classify_dev_query", classify_dev_query)
builder.add_node("bug", handle_bug)
builder.add_node("architecture", handle_architecture)
builder.add_node("performance", handle_performance)
builder.add_node("devops", handle_devops)
builder.add_node("general", handle_general)


