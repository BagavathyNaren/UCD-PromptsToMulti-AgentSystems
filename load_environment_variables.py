import os
from dotenv import load_dotenv

def get_open_ai_api_key():
    load_dotenv()
    OPEN_AI_API_KEY = os.environ.get("OPENAI_API_KEY")
    return OPEN_AI_API_KEY

api_key_output = get_open_ai_api_key()
print(api_key_output)