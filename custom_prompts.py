import json
import os
import sys

def load_prompts():
    """Load existing prompts from prompts.json"""
    try:
        if os.path.exists('prompts.json'):
            with open('prompts.json', 'r', encoding='utf-8') as f:
                return json.load(f)
        else:
            return {"prompts": []}
    except Exception as e:
        print(f"Error loading prompts: {e}")
        return {"prompts": []}

def save_prompts(prompts_data):
    """Save prompts to prompts.json"""
    try:
        with open('prompts.json', 'w', encoding='utf-8') as f:
            json.dump(prompts_data, f, ensure_ascii=False, indent=2)
        print("프롬프트가 성공적으로 저장되었습니다.")
    except Exception as e:
        print(f"Error saving prompts: {e}")

def add_prompt():
    """Add a new prompt to prompts.json"""
    prompts_data = load_prompts()
    
    print("\n===== AI 튜터 커스텀 프롬프트 추가 =====")
    
    prompt_id = input("고유 ID (영문, 숫자, 하이픈만 사용): ")
    name = input("튜터 이름: ")
    description = input("튜터 설명: ")
    
    print("\n프롬프트 내용을 입력하세요 (입력을 마치려면 빈 줄에서 Enter를 누르세요):")
    lines = []
    while True:
        line = input()
        if not line:
            break
        lines.append(line)
    
    prompt = "\n".join(lines)
    
    # Create new prompt object
    new_prompt = {
        "id": prompt_id,
        "name": name,
        "description": description,
        "prompt": prompt
    }
    
    # Add to existing prompts
    prompts_data["prompts"].append(new_prompt)
    
    # Save to file
    save_prompts(prompts_data)
    
    print(f"\n새 튜터 프롬프트 '{name}'가 추가되었습니다.")

def list_prompts():
    """List all existing prompts"""
    prompts_data = load_prompts()
    
    print("\n===== 현재 등록된 AI 튜터 프롬프트 =====")
    
    if not prompts_data["prompts"]:
        print("등록된 프롬프트가 없습니다.")
        return
    
    for i, prompt in enumerate(prompts_data["prompts"], 1):
        print(f"{i}. ID: {prompt['id']}")
        print(f"   이름: {prompt['name']}")
        print(f"   설명: {prompt['description']}")
        print()

def delete_prompt():
    """Delete a prompt by ID"""
    prompts_data = load_prompts()
    
    if not prompts_data["prompts"]:
        print("삭제할 프롬프트가 없습니다.")
        return
    
    list_prompts()
    
    prompt_id = input("\n삭제할 프롬프트의 ID를 입력하세요: ")
    
    # Find and remove the prompt
    prompt_index = next((i for i, p in enumerate(prompts_data["prompts"]) if p["id"] == prompt_id), None)
    
    if prompt_index is None:
        print(f"ID '{prompt_id}'와 일치하는 프롬프트를 찾을 수 없습니다.")
        return
    
    deleted_prompt = prompts_data["prompts"].pop(prompt_index)
    
    # Save updated prompts
    save_prompts(prompts_data)
    
    print(f"프롬프트 '{deleted_prompt['name']}'이(가) 삭제되었습니다.")

def main():
    while True:
        print("\n===== AI 튜터 프롬프트 관리 도구 =====")
        print("1. 프롬프트 목록 보기")
        print("2. 새 프롬프트 추가")
        print("3. 프롬프트 삭제")
        print("4. 종료")
        
        choice = input("\n선택: ")
        
        if choice == '1':
            list_prompts()
        elif choice == '2':
            add_prompt()
        elif choice == '3':
            delete_prompt()
        elif choice == '4':
            print("프로그램을 종료합니다.")
            sys.exit(0)
        else:
            print("올바른 옵션을 선택하세요.")

if __name__ == "__main__":
    main() 