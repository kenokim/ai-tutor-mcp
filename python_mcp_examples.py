#!/usr/bin/env python3
"""
Model Context Protocol (MCP) Python 예제 모음
다양한 MCP 기능을 Python으로 구현한 예제 코드입니다.
"""

import json
import os
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any
import requests

# 가상의 MCP 서버 라이브러리
# 실제 구현에서는 MCP SDK를 import 해야 합니다
# from mcp.server import McpServer, Tool, Resource, Prompt

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class McpServer:
    """MCP 서버 클래스 (가상 구현)"""
    
    def __init__(self, name: str, version: str, description: str):
        self.name = name
        self.version = version
        self.description = description
        self.tools = {}
        self.resources = {}
        self.prompts = {}
        self.capabilities = {
            "prompts": {},
            "tools": {},
            "resources": {}
        }
        logger.info(f"MCP 서버 초기화: {name} v{version}")
    
    def register_tool(self, tool):
        """도구 등록"""
        self.tools[tool.name] = tool
        logger.info(f"도구 등록: {tool.name}")
        return self
    
    def register_resource(self, resource):
        """리소스 등록"""
        self.resources[resource.id] = resource
        logger.info(f"리소스 등록: {resource.id}")
        return self
    
    def register_prompt(self, prompt):
        """프롬프트 등록"""
        self.prompts[prompt.id] = prompt
        logger.info(f"프롬프트 등록: {prompt.id}")
        return self
    
    def start(self):
        """서버 시작"""
        logger.info(f"MCP 서버 시작: {self.name}")
        # 실제 구현에서는 HTTP/WebSocket/stdio 트랜스포트 설정
        print(f"MCP 서버 '{self.name}' 실행 중...")
        
    def handle_request(self, method, params=None):
        """JSON-RPC 요청 처리 (예시 구현)"""
        if method == "mcp.server.info":
            return {
                "name": self.name,
                "version": self.version,
                "description": self.description,
                "capabilities": self.capabilities
            }
        elif method == "mcp.tools.list":
            return {"tools": list(self.tools.values())}
        elif method == "mcp.tools.call":
            # 도구 호출 로직 구현
            tool_name = params.get("name")
            tool_args = params.get("arguments", {})
            if tool_name not in self.tools:
                raise ValueError(f"Tool not found: {tool_name}")
            return self.tools[tool_name].execute(tool_args)
        elif method == "mcp.prompts.list":
            return {"prompts": list(self.prompts.values())}
        elif method == "mcp.prompts.get":
            prompt_id = params.get("id")
            if prompt_id not in self.prompts:
                raise ValueError(f"Prompt not found: {prompt_id}")
            return self.prompts[prompt_id]
        else:
            raise ValueError(f"Unknown method: {method}")

class Tool:
    """MCP 도구 클래스 (가상 구현)"""
    
    def __init__(self, name, description, schema, handler):
        self.name = name
        self.description = description
        self.schema = schema
        self.handler = handler
    
    def execute(self, args):
        """도구 실행"""
        return self.handler(args)

class Resource:
    """MCP 리소스 클래스 (가상 구현)"""
    
    def __init__(self, id, type, metadata, content):
        self.id = id
        self.type = type
        self.metadata = metadata
        self.content = content

class Prompt:
    """MCP 프롬프트 클래스 (가상 구현)"""
    
    def __init__(self, id, name, description, template, parameters=None):
        self.id = id
        self.name = name
        self.description = description
        self.template = template
        self.parameters = parameters or {}


# 예제 1: 기본 AI 튜터 MCP 서버
def create_ai_tutor_server():
    """기본 AI 튜터 MCP 서버 생성 예제"""
    
    server = McpServer(
        name="ai-tutor",
        version="1.0.0",
        description="AI 튜터 MCP 서버"
    )
    
    # 수학 튜터 프롬프트 등록
    math_tutor_prompt = Prompt(
        id="math-tutor",
        name="수학 튜터",
        description="수학 문제 해결 지원",
        template="당신은 친절하고 명확한 수학 튜터입니다. {difficulty} 수준의 {topic} 문제에 대해 단계별로 설명해주세요.",
        parameters={
            "difficulty": {
                "type": "string",
                "enum": ["초급", "중급", "고급"],
                "description": "문제 난이도"
            },
            "topic": {
                "type": "string",
                "description": "수학 주제(예: 대수학, 기하학, 미적분)"
            }
        }
    )
    server.register_prompt(math_tutor_prompt)
    
    # 학습 자료 검색 도구 등록
    learning_materials = {
        "math": {
            "algebra": "대수학 기본 개념과 공식...",
            "calculus": "미적분학 기초 이론...",
            "geometry": "기하학 원리와 정리..."
        },
        "programming": {
            "python": "파이썬 프로그래밍 기초...",
            "javascript": "자바스크립트 개요 및 문법..."
        }
    }
    
    def search_materials_handler(args):
        """학습 자료 검색 도구 핸들러"""
        subject = args.get("subject")
        topic = args.get("topic")
        
        if subject not in learning_materials:
            return {"error": f"주제 '{subject}'를 찾을 수 없습니다"}
        
        if topic:
            if topic not in learning_materials[subject]:
                return {"error": f"'{subject}'에서 '{topic}'을 찾을 수 없습니다"}
            return {
                "subject": subject,
                "topic": topic,
                "content": learning_materials[subject][topic]
            }
        else:
            return {
                "subject": subject,
                "available_topics": list(learning_materials[subject].keys())
            }
    
    search_tool = Tool(
        name="search_learning_materials",
        description="학습 주제 및 자료 검색",
        schema={
            "type": "object",
            "properties": {
                "subject": {
                    "type": "string",
                    "description": "검색할 주제(math, programming 등)"
                },
                "topic": {
                    "type": "string",
                    "description": "검색할 세부 주제(선택 사항)"
                }
            },
            "required": ["subject"]
        },
        handler=search_materials_handler
    )
    server.register_tool(search_tool)
    
    # 학습 진도 추적 도구
    student_progress = {}
    
    def track_progress_handler(args):
        """학습 진도 추적 도구 핸들러"""
        student_id = args.get("student_id")
        subject = args.get("subject")
        topic = args.get("topic")
        completed = args.get("completed", False)
        score = args.get("score")
        
        if student_id not in student_progress:
            student_progress[student_id] = {}
        
        if subject not in student_progress[student_id]:
            student_progress[student_id][subject] = {}
        
        student_progress[student_id][subject][topic] = {
            "completed": completed,
            "score": score,
            "timestamp": datetime.now().isoformat()
        }
        
        return {
            "success": True,
            "student_id": student_id,
            "subject": subject,
            "topic": topic,
            "status": "완료" if completed else "진행 중",
            "score": score
        }
    
    track_tool = Tool(
        name="track_student_progress",
        description="학생의 학습 진도 추적",
        schema={
            "type": "object",
            "properties": {
                "student_id": {
                    "type": "string",
                    "description": "학생 ID"
                },
                "subject": {
                    "type": "string",
                    "description": "과목"
                },
                "topic": {
                    "type": "string",
                    "description": "주제"
                },
                "completed": {
                    "type": "boolean",
                    "description": "완료 여부",
                    "default": False
                },
                "score": {
                    "type": "integer",
                    "description": "점수(선택 사항)"
                }
            },
            "required": ["student_id", "subject", "topic"]
        },
        handler=track_progress_handler
    )
    server.register_tool(track_tool)
    
    return server

# 예제 2: 데이터베이스 접근 MCP 서버
def create_database_server():
    """데이터베이스 접근 MCP 서버 예제 (가상 구현)"""
    
    server = McpServer(
        name="db-server",
        version="1.0.0",
        description="데이터베이스 접근 MCP 서버"
    )
    
    # 가상의 데이터베이스 연결 및 스키마
    db_schema = {
        "users": [
            {"name": "id", "type": "integer", "primary_key": True},
            {"name": "username", "type": "varchar"},
            {"name": "email", "type": "varchar"},
            {"name": "created_at", "type": "timestamp"}
        ],
        "products": [
            {"name": "id", "type": "integer", "primary_key": True},
            {"name": "name", "type": "varchar"},
            {"name": "price", "type": "decimal"},
            {"name": "category", "type": "varchar"}
        ],
        "orders": [
            {"name": "id", "type": "integer", "primary_key": True},
            {"name": "user_id", "type": "integer", "foreign_key": "users.id"},
            {"name": "total", "type": "decimal"},
            {"name": "status", "type": "varchar"},
            {"name": "created_at", "type": "timestamp"}
        ]
    }
    
    # 가상 데이터
    db_data = {
        "users": [
            {"id": 1, "username": "user1", "email": "user1@example.com", "created_at": "2023-01-01T00:00:00Z"},
            {"id": 2, "username": "user2", "email": "user2@example.com", "created_at": "2023-01-02T00:00:00Z"}
        ],
        "products": [
            {"id": 1, "name": "Product A", "price": 19.99, "category": "Electronics"},
            {"id": 2, "name": "Product B", "price": 29.99, "category": "Clothing"}
        ],
        "orders": [
            {"id": 1, "user_id": 1, "total": 19.99, "status": "completed", "created_at": "2023-01-03T00:00:00Z"},
            {"id": 2, "user_id": 2, "total": 29.99, "status": "pending", "created_at": "2023-01-04T00:00:00Z"}
        ]
    }
    
    # 스키마 리소스 등록
    schema_resource = Resource(
        id="db-schema",
        type="database-schema",
        metadata={
            "description": "데이터베이스 스키마 정보"
        },
        content=json.dumps(db_schema)
    )
    server.register_resource(schema_resource)
    
    # SQL 쿼리 도구
    def query_database_handler(args):
        """SQL 쿼리 실행 핸들러 (읽기 전용, 가상 구현)"""
        query = args.get("query", "").strip().lower()
        
        # 간단한 SQL 파서 (실제 구현에서는 더 안전한 방법 사용)
        if not query.startswith(("select", "show", "explain")):
            return {"error": "읽기 전용 쿼리만 허용됩니다"}
        
        # 매우 간단한 쿼리 처리 예시
        if "from users" in query:
            return {
                "columns": ["id", "username", "email", "created_at"],
                "rows": db_data["users"],
                "rowCount": len(db_data["users"])
            }
        elif "from products" in query:
            return {
                "columns": ["id", "name", "price", "category"],
                "rows": db_data["products"],
                "rowCount": len(db_data["products"])
            }
        elif "from orders" in query:
            return {
                "columns": ["id", "user_id", "total", "status", "created_at"],
                "rows": db_data["orders"],
                "rowCount": len(db_data["orders"])
            }
        else:
            return {"error": "지원되지 않는 쿼리입니다"}
    
    query_tool = Tool(
        name="query_database",
        description="데이터베이스에 SQL 쿼리 실행 (읽기 전용)",
        schema={
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "실행할 SQL 쿼리(SELECT, SHOW, EXPLAIN만 허용)"
                },
                "params": {
                    "type": "array",
                    "description": "쿼리 파라미터(선택 사항)",
                    "items": {"type": "string"}
                }
            },
            "required": ["query"]
        },
        handler=query_database_handler
    )
    server.register_tool(query_tool)
    
    # SQL 쿼리 작성 도움말 프롬프트
    sql_prompt = Prompt(
        id="sql-helper",
        name="SQL 쿼리 작성 도우미",
        description="SQL 쿼리 작성 및 최적화 지원",
        template="""다음 데이터베이스 스키마를 사용하여 {task}에 적합한 SQL 쿼리를 작성해주세요:

스키마 정보:
{schema}

참고 조건:
{conditions}""",
        parameters={
            "task": {
                "type": "string",
                "description": "수행할 작업 설명"
            },
            "schema": {
                "type": "string",
                "description": "데이터베이스 스키마 정보"
            },
            "conditions": {
                "type": "string",
                "description": "추가 조건이나 제약사항"
            }
        }
    )
    server.register_prompt(sql_prompt)
    
    return server

# 예제 3: 날씨 정보 MCP 서버
def create_weather_server():
    """날씨 정보 MCP 서버 예제"""
    
    server = McpServer(
        name="weather-server",
        version="1.0.0",
        description="날씨 정보 제공 MCP 서버"
    )
    
    # 날씨 검색 도구
    def get_weather_handler(args):
        """날씨 정보 검색 핸들러"""
        city = args.get("city")
        units = args.get("units", "metric")
        
        # 실제 구현에서는 외부 API 호출
        # 예시 응답 반환
        try:
            # 예시: 실제로는 https://api.weather.com/ 같은 외부 API 호출
            weather_data = {
                "location": city,
                "temperature": 22.5 if units == "metric" else 72.5,
                "humidity": 65,
                "conditions": "맑음",
                "wind_speed": 5.8 if units == "metric" else 13.0,
                "units": units
            }
            return weather_data
        except Exception as e:
            logger.error(f"날씨 정보 검색 오류: {e}")
            return {"error": f"날씨 정보를 가져오는 중 오류 발생: {str(e)}"}
    
    weather_tool = Tool(
        name="get_weather",
        description="특정 도시의 현재 날씨 정보 조회",
        schema={
            "type": "object",
            "properties": {
                "city": {
                    "type": "string",
                    "description": "날씨를 검색할 도시 이름"
                },
                "units": {
                    "type": "string",
                    "enum": ["metric", "imperial"],
                    "description": "온도 단위(미터법 또는 야드파운드법)",
                    "default": "metric"
                }
            },
            "required": ["city"]
        },
        handler=get_weather_handler
    )
    server.register_tool(weather_tool)
    
    # 날씨 경보 검색 도구
    def get_weather_alerts_handler(args):
        """날씨 경보 검색 핸들러"""
        region = args.get("region")
        severity = args.get("severity", "all")
        
        # 실제 구현에서는 외부 API 호출
        # 예시 응답 반환
        if region.lower() == "seoul":
            return {
                "alerts": [
                    {
                        "type": "폭염 주의보",
                        "severity": "moderate",
                        "description": "오후 1시부터 6시까지 폭염 주의보가 발효됩니다.",
                        "start_time": "2023-07-15T13:00:00Z",
                        "end_time": "2023-07-15T18:00:00Z"
                    }
                ],
                "region": region
            }
        elif region.lower() == "busan":
            return {
                "alerts": [
                    {
                        "type": "태풍 경보",
                        "severity": "severe",
                        "description": "태풍 접근으로 인한 강풍 및 폭우가 예상됩니다.",
                        "start_time": "2023-07-15T00:00:00Z",
                        "end_time": "2023-07-16T00:00:00Z"
                    }
                ],
                "region": region
            }
        else:
            return {
                "alerts": [],
                "region": region,
                "message": "현재 활성화된 경보가 없습니다."
            }
    
    alerts_tool = Tool(
        name="get_weather_alerts",
        description="특정 지역의 활성 날씨 경보 조회",
        schema={
            "type": "object",
            "properties": {
                "region": {
                    "type": "string",
                    "description": "경보를 검색할 지역 이름"
                },
                "severity": {
                    "type": "string",
                    "enum": ["all", "minor", "moderate", "severe"],
                    "description": "경보 심각도 필터",
                    "default": "all"
                }
            },
            "required": ["region"]
        },
        handler=get_weather_alerts_handler
    )
    server.register_tool(alerts_tool)
    
    # 날씨 예보 프롬프트
    weather_prompt = Prompt(
        id="weather-forecast",
        name="날씨 예보 설명",
        description="날씨 데이터를 바탕으로 사용자 친화적인 예보 생성",
        template="""당신은 친절한 기상 전문가입니다. 다음 날씨 데이터를 분석하여 {location}의 {time_period} 날씨에 대한 이해하기 쉬운 요약을 제공해주세요.

날씨 데이터:
{weather_data}

이 정보를 바탕으로 {audience}에게 적합한 날씨 예보를 작성해주세요. {additional_instructions}""",
        parameters={
            "location": {
                "type": "string",
                "description": "날씨 예보 지역"
            },
            "time_period": {
                "type": "string",
                "description": "예보 기간(오늘, 내일, 이번 주 등)"
            },
            "weather_data": {
                "type": "string",
                "description": "날씨 데이터 JSON 문자열"
            },
            "audience": {
                "type": "string",
                "description": "대상 청중(일반인, 농부, 여행자 등)",
                "default": "일반인"
            },
            "additional_instructions": {
                "type": "string",
                "description": "추가 지시사항",
                "default": ""
            }
        }
    )
    server.register_prompt(weather_prompt)
    
    return server

# 예제 4: AI 샘플링 기능을 사용하는 MCP 서버 
def create_sampling_server():
    """AI 샘플링 기능을 사용하는 MCP 서버 예제"""
    
    server = McpServer(
        name="ai-sampling-server",
        version="1.0.0",
        description="AI 샘플링 기능을 사용하는 MCP 서버"
    )
    
    # AI 계산기 도구
    def ai_calculator_handler(args, exchange=None):
        """AI를 사용한 계산기 핸들러"""
        expression = args.get("expression", "")
        
        # 실제 구현에서는 exchange 객체를 통해 클라이언트에 샘플링 요청
        # 이 예제에서는 가상 구현으로 직접 결과 반환
        if exchange and hasattr(exchange, 'get_client_capabilities'):
            if not exchange.get_client_capabilities().get('sampling'):
                return "클라이언트가 AI 샘플링을 지원하지 않습니다."
            
            # 실제 구현에서는 다음과 같이 요청 생성 및 전송
            """
            request = {
                "content": {"type": "text", "text": f"Calculate: {expression}"},
                "modelPreferences": {
                    "hints": ["claude-3-sonnet", "claude"],
                    "intelligencePriority": 0.8,
                    "speedPriority": 0.5
                },
                "systemPrompt": "You are a helpful calculator assistant. Provide only the numerical answer.",
                "maxTokens": 100
            }
            
            response = exchange.create_message(request)
            answer = response.content.text
            return answer
            """
            
            # 가상 구현
            return f"계산 결과: {eval(expression)}"  # 주의: 실제 환경에서는 eval 사용하지 말 것
        else:
            # 샘플링 없이 기본 구현
            try:
                result = eval(expression)  # 주의: 실제 환경에서는 eval 사용하지 말 것
                return f"계산 결과: {result}"
            except Exception as e:
                return f"계산 오류: {str(e)}"
    
    calculator_tool = Tool(
        name="ai_calculator",
        description="AI를 사용하여 수학 표현식 계산",
        schema={
            "type": "object",
            "properties": {
                "expression": {
                    "type": "string",
                    "description": "계산할 수학 표현식"
                }
            },
            "required": ["expression"]
        },
        handler=ai_calculator_handler
    )
    server.register_tool(calculator_tool)
    
    # 텍스트 요약 도구
    def text_summarizer_handler(args, exchange=None):
        """AI를 사용한, 텍스트 요약 핸들러"""
        text = args.get("text", "")
        max_length = args.get("max_length", 100)
        
        # 실제 구현에서는 exchange 객체를 통해 클라이언트에 샘플링 요청
        if exchange and hasattr(exchange, 'get_client_capabilities'):
            if not exchange.get_client_capabilities().get('sampling'):
                return "클라이언트가 AI 샘플링을 지원하지 않습니다."
            
            # 실제 구현에서는 다음과 같이 요청 생성 및 전송
            """
            request = {
                "content": {"type": "text", "text": f"Summarize: {text}"},
                "modelPreferences": {
                    "hints": ["claude-3-opus", "claude-3-sonnet"],
                    "intelligencePriority": 0.9,
                    "speedPriority": 0.3
                },
                "systemPrompt": "You are an expert summarizer. Provide a concise yet informative summary.",
                "maxTokens": max_length
            }
            
            response = exchange.create_message(request)
            summary = response.content.text
            return summary
            """
            
            # 가상 구현
            if len(text) <= max_length:
                return text
            return text[:max_length - 3] + "..."
        else:
            # 샘플링 없이 기본 구현
            if len(text) <= max_length:
                return text
            return text[:max_length - 3] + "..."
    
    summarizer_tool = Tool(
        name="text_summarizer",
        description="AI를 사용한 텍스트 요약",
        schema={
            "type": "object",
            "properties": {
                "text": {
                    "type": "string",
                    "description": "요약할 텍스트"
                },
                "max_length": {
                    "type": "integer",
                    "description": "최대 요약 길이(글자 수)",
                    "default": 100
                }
            },
            "required": ["text"]
        },
        handler=text_summarizer_handler
    )
    server.register_tool(summarizer_tool)
    
    return server

# 메인 실행 코드
if __name__ == "__main__":
    print("MCP 서버 예제 코드")
    print("1. AI 튜터 서버")
    print("2. 데이터베이스 서버")
    print("3. 날씨 정보 서버")
    print("4. AI 샘플링 서버")
    
    choice = input("실행할 서버 번호 선택: ")
    
    if choice == "1":
        server = create_ai_tutor_server()
    elif choice == "2":
        server = create_database_server()
    elif choice == "3":
        server = create_weather_server()
    elif choice == "4":
        server = create_sampling_server()
    else:
        print("잘못된 선택입니다.")
        exit(1)
    
    server.start()
    
    print("\n서버가 시작되었습니다. Ctrl+C로 종료할 수 있습니다.")
    try:
        # 간단한 테스트 요청 처리
        print("\n서버 정보 요청:")
        info = server.handle_request("mcp.server.info")
        print(json.dumps(info, indent=2, ensure_ascii=False))
        
        # 도구 목록 요청
        print("\n도구 목록 요청:")
        tools = server.handle_request("mcp.tools.list")
        print(f"사용 가능한 도구: {len(tools['tools'])}개")
        for tool in tools['tools']:
            print(f" - {tool.name}: {tool.description}")
        
        # 대기
        while True:
            input("\n아무 키나 누르면 종료됩니다...")
            break
            
    except KeyboardInterrupt:
        print("\n서버를 종료합니다.")
    except Exception as e:
        print(f"\n오류 발생: {e}") 