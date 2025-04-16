from mcp.server.fastmcp import FastMCP

mcp = FastMCP('AI tutor')

@mcp.tool()
def get_intro(type: str) -> str:
    """어떤 것을 가르치는 선생님인지 소개합니다."""
    return f'{type} 과외 선생님입니다.'

# 수학 튜터 프롬프트 추가
@mcp.prompt("math_tutor")
def math_tutor():
    """수학 문제 해결을 도와주는 프롬프트입니다."""
    return {
        """messages": [
            {
                "role": "system",
                "content": {
                    "type": "text",
                    "text": "당신은 친절하고 명확하게 설명해주는 수학 튜터입니다. 학생의 이해 수준에 맞춰 단계별로 풀이를 제공합니다."
                }
            },
            {
                "role": "user",
                "content": {
                    "type": "text",
                    "text": f"난이도의 문제를 어떻게 풀어야 할지 설명해주세요. 개념부터 차근차근 알려주세요."
                }
            }
        ]"""
    }

if __name__ == '__main__':
    mcp.run(transport='stdio')
