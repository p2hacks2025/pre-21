import hashlib
import json
import os
import time
from typing import Any
from .config import settings

def _ensure_dirs() -> None:
    for d in [settings.jobs_dir, settings.idem_dir, settings.artifacts_dir]:
        os.makedirs(d, exist_ok=True)

def _atomic_write_json(path: str, obj: dict[str, Any]) -> None:
    tmp = f"{path}.tmp"
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
        f.flush()
        os.fsync(f.fileno())
    os.replace(tmp, path)

def idem_key_to_filename(device_id: str, idempotency_key: str) -> str:
    h = hashlib.sha256(f"{device_id}:{idempotency_key}".encode("utf-8")).hexdigest()
    return os.path.join(settings.idem_dir, f"{h}.json")

def job_path(job_id: str) -> str:
    return os.path.join(settings.jobs_dir, f"{job_id}.json")

def create_or_get_job(device_id: str, idempotency_key: str, new_job_id: str) -> tuple[str, bool]:
    """
    returns: (job_id, created_new)
    """
    _ensure_dirs()
    idem_path = idem_key_to_filename(device_id, idempotency_key)

    if os.path.exists(idem_path):
        with open(idem_path, "r", encoding="utf-8") as f:
            job_id = json.load(f)["job_id"]
        return job_id, False

    # 排他作成（存在したら誰かが先に作った）
    try:
        fd = os.open(idem_path, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o644)
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump({"job_id": new_job_id}, f, ensure_ascii=False)
            f.flush()
            os.fsync(f.fileno())
        return new_job_id, True
    except FileExistsError:
        with open(idem_path, "r", encoding="utf-8") as f:
            job_id = json.load(f)["job_id"]
        return job_id, False

def write_job(
    job_id: str,
    status: str,
    *,
    error: dict | None = None,
    artifact_path: str | None = None,
) -> None:
    _ensure_dirs()
    now = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    path = job_path(job_id)
    obj = {
        "job_id": job_id,
        "status": status,
        "error": error,
        "artifact_path": artifact_path,
        "updated_at": now,
    }
    _atomic_write_json(path, obj)

def read_job(job_id: str) -> dict:
    path = job_path(job_id)
    if not os.path.exists(path):
        raise FileNotFoundError(job_id)
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)
