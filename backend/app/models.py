from typing import Literal
from pydantic import BaseModel, Field

class PrintRequest(BaseModel):
    device_id: str = Field(default="esp32")
    idempotency_key: str = Field(min_length=8, max_length=200)
    payload: str = Field(min_length=1, max_length=4000)
    template_id: str = Field(default="default")
    copies: int = Field(default=1, ge=1, le=20)

class JobStatus(BaseModel):
    job_id: str
    status: Literal[
        "RECEIVED",
        "QUEUED",
        "LLM_PROCESSING",
        "LLM_FAILED",
        "RENDERING",
        "RENDER_FAILED",
        "PRINTING",
        "PRINT_FAILED",
        "PRINTED",
    ]

    error: dict | None = None
    artifact_path: str | None = None
    updated_at: str

class PrintDoc(BaseModel):
    name: str = Field(description="キラキラネーム")
    #body: str = Field(description="本文（複数行OK）")
    #bullets: list[str] = Field(default_factory=list, description="箇条書き（0個以上）")
