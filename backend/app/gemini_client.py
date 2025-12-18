from fastapi import FastAPI, HTTPException, Query
from google import genai
from google.genai import types
from config import settings

from typing import List, Optional
from pydantic import BaseModel, Field
import os  # 追加
from dotenv import load_dotenv  # 追加

load_dotenv() # .envファイルを読み込む
API_KEY = os.getenv("GOOGLE_API_KEY")

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

