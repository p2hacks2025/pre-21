import uuid
from fastapi import FastAPI, BackgroundTasks, HTTPException
from .models import PrintRequest, JobStatus
from .store import create_or_get_job, write_job, read_job
from .gemini_client import gemini_transform
from .render import render_pdf
from .print_service import print_pdf

app = FastAPI()

@app.get("/health")
def health():
    return {"ok": True}

@app.post("/v1/print", response_model=dict)
def create_print(req: PrintRequest, bg: BackgroundTasks):
    new_job_id = str(uuid.uuid4())
    job_id, created = create_or_get_job(req.device_id, req.idempotency_key, new_job_id)

    if not created:
        # 既存ジョブを返す（再送でも二重印刷しない）
        try:
            job = read_job(job_id)
            return {"job_id": job_id, "status": job["status"]}
        except FileNotFoundError:
            # 参照壊れはレアだが、ここでは作り直さずエラーにする
            raise HTTPException(status_code=409, detail="Idempotency map exists but job missing")

    write_job(job_id, "RECEIVED")
    write_job(job_id, "QUEUED")
    bg.add_task(process_job, job_id, req)
    return {"job_id": job_id, "status": "QUEUED"}

@app.get("/v1/jobs/{job_id}", response_model=JobStatus)
def get_job(job_id: str):
    try:
        job = read_job(job_id)
        return JobStatus(**job)
    except FileNotFoundError:
        raise HTTPException(status_code=404, detail="job not found")

def process_job(job_id: str, req: PrintRequest) -> None:
    try:
        write_job(job_id, "LLM_PROCESSING")
        doc = gemini_transform(req.payload)

        write_job(job_id, "RENDERING")
        pdf_path = render_pdf(job_id, req.template_id, doc)

        write_job(job_id, "PRINTING", artifact_path=pdf_path)
        print_pdf(pdf_path, req.copies)

        write_job(job_id, "PRINTED", artifact_path=pdf_path)

    except Exception as e:
        # どこで落ちたか最低限わかるようにする
        msg = str(e)
        # 状態はざっくりでも良いが、デバッグのため段階別に分ける
        status = "PRINT_FAILED" if "Print failed" in msg else "LLM_FAILED" if "GEMINI" in msg or "schema" in msg else "RENDER_FAILED"
        write_job(job_id, status, error={"message": msg})
