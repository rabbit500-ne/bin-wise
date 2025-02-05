import json
from langchain_core.messages import AIMessage


def parse(ai_message: AIMessage) -> str:
    """Parse the AI message."""
    input_string = ai_message.content
    if input_string.startswith("```json") and input_string.endswith("```"):
        clean_data = input_string.strip("```json").strip("```")
    else:
        raise ValueError("Invalid format. The input must be wrapped with ```json ... ```.")
    
    # JSONを辞書に変換
    try:
        parsed_data = json.loads(clean_data)
    except json.JSONDecodeError as e:
        raise ValueError(f"Failed to parse JSON: {e}")
    
    return parsed_data