from mcp.server.fastmcp import FastMCP

mcp = FastMCP('AI tutor')

@mcp.tool()
def get_intro(type: str) -> str:
    """어떤 것을 가르치는 선생님인지 소개합니다."""
    return f'{type} 과외 선생님입니다.'

if __name__ == '__main__':
    mcp.run(transport='stdio')
