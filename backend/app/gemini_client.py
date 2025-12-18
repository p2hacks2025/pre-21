from fastapi import HTTPException
from google import genai
from google.genai import types
from .config import settings



if not API_KEY:
    raise RuntimeError("環境変数 GOOGLE_API_KEY が設定されていません。")


MODEL_NAME = "gemini-3.0-flush"


client = genai.Client(api_key=API_KEY)

def send_text():
    pass

def generate_text():
    pass
    
def return_text():
    pass

