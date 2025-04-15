from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import uuid
import logging

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

app = Flask(__name__)
CORS(app)

# MCP server configuration
SERVER_NAME = "ai-tutor"
SERVER_VERSION = "1.0.0"
SERVER_DESCRIPTION = "AI Tutor MCP Server for Claude Desktop"

# Load prompts from JSON file
def load_prompts():
    try:
        if os.path.exists('prompts.json'):
            with open('prompts.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            # Create default prompts if file doesn't exist
            default_prompts = {
                "prompts": [
                    {
                        "id": "math-tutor",
                        "name": "수학 과외 선생님",
                        "description": "수학 문제 풀이와 개념 설명을 도와주는 과외 선생님입니다.",
                        "prompt": "당신은 친절하고 인내심 있는 수학 과외 선생님입니다. 학생들이 질문하는 수학 문제에 대해 단계별로 명확한 설명을 제공합니다. 개념을 쉽게 이해할 수 있도록 다양한 예시를 들어 설명하며, 학생이 스스로 답을 찾을 수 있도록 안내합니다. 문제를 바로 풀어주기보다 힌트를 제공하고 학생이 생각할 기회를 줍니다. 학생의 이해도를 확인하기 위한 질문을 적절히 사용하세요."
                    },
                    {
                        "id": "programming-tutor",
                        "name": "프로그래밍 지도 선생님",
                        "description": "코딩 학습과 문제 해결을 돕는 프로그래밍 교육자입니다.",
                        "prompt": "당신은 경험이 풍부한 프로그래밍 교육자입니다. 학생들에게 코딩 개념을 이해하기 쉽게 설명하고, 실용적인 예제 코드를 제공합니다. 학생들이 직면한 코딩 문제를 해결하는 과정을 단계별로 안내하되, 완성된 코드를 바로 제공하기보다 학생이 스스로 생각하고 해결할 수 있도록 도와주세요. 코딩 모범 사례와 효율적인 접근 방식을 알려주고, 학생의 코드를 개선할 수 있는 방법을 제안하세요."
                    },
                    {
                        "id": "science-tutor",
                        "name": "과학 선생님",
                        "description": "과학 개념과 원리를 설명하는 과학 교육자입니다.",
                        "prompt": "당신은 열정적인 과학 교육자입니다. 복잡한 과학 개념을 이해하기 쉬운 언어로 설명하고, 일상 생활의 예시를 활용하여 학생들의 이해를 돕습니다. 과학적 사실과 최신 연구를 정확하게 전달하며, 학생들의 호기심을 자극하는 질문을 던집니다. 학생들이 스스로 생각하고 가설을 세울 수 있도록 유도하고, 과학적 방법론을 통해 문제를 해결하는 과정을 안내합니다."
                    },
                    {
                        "id": "language-tutor",
                        "name": "언어 교육 선생님",
                        "description": "언어 학습과 작문을 도와주는 언어 교육 전문가입니다.",
                        "prompt": "당신은 언어 교육 전문가입니다. 학생들의 작문 실력 향상을 위한 구체적인 피드백을 제공하고, 문법과 어휘 사용에 대한 조언을 합니다. 학생들이 자신의 생각을 명확하고 논리적으로 표현할 수 있도록 돕고, 효과적인 의사소통 기술을 가르칩니다. 학생들의 글을 존중하면서도 개선점을 제시하며, 다양한 글쓰기 스타일과 형식에 대한 지침을 제공합니다."
                    }
                ]
            }
            with open('prompts.json', 'w', encoding='utf-8') as f:
                json.dump(default_prompts, f, ensure_ascii=False, indent=2)
            return default_prompts
    except Exception as e:
        logger.error(f"Error loading prompts: {e}")
        return {"prompts": []}

# MCP JSON-RPC endpoint
@app.route('/mcp', methods=['POST'])
def mcp_endpoint():
    try:
        request_data = request.json
        logger.info(f"Received request: {request_data}")
        
        if not request_data or 'method' not in request_data:
            return jsonify({"jsonrpc": "2.0", "error": {"code": -32600, "message": "Invalid Request"}, "id": None})
        
        request_id = request_data.get('id', None)
        method = request_data.get('method')
        params = request_data.get('params', {})
        
        # Handle MCP methods
        if method == "mcp.server.info":
            return jsonify({
                "jsonrpc": "2.0",
                "result": {
                    "name": SERVER_NAME,
                    "version": SERVER_VERSION,
                    "description": SERVER_DESCRIPTION,
                    "capabilities": {
                        "prompts": {}
                    }
                },
                "id": request_id
            })
        
        elif method == "mcp.prompts.list":
            prompts_data = load_prompts()
            prompts_list = [
                {
                    "id": p["id"],
                    "name": p["name"],
                    "description": p["description"]
                } for p in prompts_data.get("prompts", [])
            ]
            
            return jsonify({
                "jsonrpc": "2.0",
                "result": prompts_list,
                "id": request_id
            })
        
        elif method == "mcp.prompts.get":
            prompt_id = params.get("id")
            if not prompt_id:
                return jsonify({"jsonrpc": "2.0", "error": {"code": -32602, "message": "Invalid params: missing id"}, "id": request_id})
            
            prompts_data = load_prompts()
            prompt = next((p for p in prompts_data.get("prompts", []) if p["id"] == prompt_id), None)
            
            if not prompt:
                return jsonify({"jsonrpc": "2.0", "error": {"code": -32602, "message": f"Prompt not found: {prompt_id}"}, "id": request_id})
            
            return jsonify({
                "jsonrpc": "2.0",
                "result": {
                    "id": prompt["id"],
                    "name": prompt["name"],
                    "description": prompt["description"],
                    "prompt": prompt["prompt"]
                },
                "id": request_id
            })
        
        else:
            return jsonify({"jsonrpc": "2.0", "error": {"code": -32601, "message": f"Method not found: {method}"}, "id": request_id})
            
    except Exception as e:
        logger.error(f"Error processing request: {e}")
        return jsonify({"jsonrpc": "2.0", "error": {"code": -32603, "message": f"Internal error: {str(e)}"}, "id": request_data.get('id', None)})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True) 