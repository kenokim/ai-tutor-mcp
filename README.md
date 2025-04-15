# AI Tutor MCP
MCP 서버로 구현한 AI 선생님

## 소개
이 프로젝트는 Model Context Protocol (MCP)을 활용한 AI 튜터 서버입니다. Claude Desktop 애플리케이션에서 사용할 수 있는 다양한 교육 프롬프트를 제공합니다.

## 기능
- 다양한 주제별 튜터 프롬프트 제공 (수학, 프로그래밍, 과학, 언어)
- MCP 프롬프트 기능 지원
- Claude Desktop과 쉬운 통합

## 설치 방법

### 요구 사항
- Python 3.7 이상
- pip (Python 패키지 관리자)

### 설치 단계
1. 저장소 클론
```bash
git clone https://github.com/yourusername/ai-tutor-mcp.git
cd ai-tutor-mcp
```

2. 필요한 패키지 설치
```bash
pip install -r requirements.txt
```

## 서버 실행
```bash
python app.py
```
서버는 기본적으로 http://localhost:5000 에서 실행됩니다.

## Claude Desktop에서 설정하기

1. Claude Desktop 설정 파일 열기 (없으면 생성)
   - macOS/Linux: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%AppData%\Claude\claude_desktop_config.json`

2. 다음 설정 추가:
```json
{
    "mcpServers": {
        "ai-tutor": {
            "command": "python",
            "args": [
                "app.py"
            ],
            "cwd": "/절대/경로/ai-tutor-mcp"
        }
    }
}
```
`/절대/경로/ai-tutor-mcp`를 실제 프로젝트 경로로 바꿔주세요.

3. Claude Desktop 재시작

## 사용 방법
1. Claude Desktop을 실행하고 MCP 서버가 연결되었는지 확인합니다.
2. 대화창에서 튜터 프롬프트를 선택합니다.
3. 선택한 주제에 대한 질문을 시작합니다.

## 커스텀 프롬프트 추가
`prompts.json` 파일을 편집하여 새로운 튜터 프롬프트를 추가할 수 있습니다. 형식은 다음과 같습니다:
```json
{
  "id": "unique-id",
  "name": "튜터 이름",
  "description": "튜터 설명",
  "prompt": "프롬프트 내용..."
}
```

## 라이센스
MIT
