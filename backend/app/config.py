import os
from pydantic import BaseModel
from dotenv import load_dotenv

# .env を自動読み込み（ローカル開発向け）
load_dotenv()

class Settings(BaseModel):
    gemini_api_key: str | None = os.getenv("GEMINI_API_KEY")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    base_url: str = os.getenv("BASE_URL", "http://localhost:8000")
    printer_name: str | None = os.getenv("PRINTER_NAME") or None

    data_dir: str = os.getenv("DATA_DIR", "data")
    jobs_dir: str = os.getenv("JOBS_DIR", "data/jobs")
    idem_dir: str = os.getenv("IDEM_DIR", "data/idem")
    llm_dir: str = os.getenv("LLM_DIR", "data/llm")
    artifacts_dir: str = os.getenv("ARTIFACTS_DIR", "data/artifacts")

settings = Settings()
