from fastapi import APIRouter, status

router = APIRouter()

@router.get("/")
async def index():
    return {"index": True}



@router.get("/health", status_code=200)
async def health():
    return {"ok": True}



@router.post("/generate", status_code=201)
async def generate_text():
    pass

