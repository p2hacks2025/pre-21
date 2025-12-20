import time
from fastapi.testclient import TestClient

from app.main import app
from app.store import write_job
from app.config import settings


def test_print_flow_and_idempotency(tmp_path, monkeypatch):
    # ランタイムディレクトリを一時領域へ
    monkeypatch.setattr(settings, "jobs_dir", str(tmp_path / "jobs"), raising=False)
    monkeypatch.setattr(settings, "idem_dir", str(tmp_path / "idem"), raising=False)
    monkeypatch.setattr(settings, "artifacts_dir", str(tmp_path / "artifacts"), raising=False)

    # process_job を同期・高速なダミーに差し替え（バックグラウンドタスクの完了を容易に）
    import app.main as m

    def fake_process(job_id, req):
        write_job(job_id, "LLM_PROCESSING")
        write_job(job_id, "RENDERING")
        # ダミーの成果物パス
        fake_pdf = str((tmp_path / "artifacts" / f"{job_id}.pdf").resolve())
        write_job(job_id, "PRINTING", artifact_path=fake_pdf)
        write_job(job_id, "PRINTED", artifact_path=fake_pdf)

    monkeypatch.setattr(m, "process_job", fake_process, raising=True)

    client = TestClient(app)

    body = {
        "device_id": "devA",
        "idempotency_key": "idem-12345678",
        "payload": "Hello",
        "template_id": "index",
        "copies": 1,
    }

    # 1回目: ジョブ作成
    r = client.post("/v1/print", json=body)
    assert r.status_code == 200
    data = r.json()
    job_id = data["job_id"]
    assert data["status"] in {"QUEUED", "PRINTED"}

    # バックグラウンドタスクの完了を待機（最大 1 秒）
    for _ in range(100):
        jr = client.get(f"/v1/jobs/{job_id}")
        assert jr.status_code == 200
        if jr.json()["status"] == "PRINTED":
            break
        time.sleep(0.01)
    else:
        assert False, "job did not reach PRINTED in time"

    # 2回目: 同じ idempotency_key で再送 → 既存ジョブを返す
    r2 = client.post("/v1/print", json=body)
    assert r2.status_code == 200
    data2 = r2.json()
    assert data2["job_id"] == job_id
    assert data2["status"] == "PRINTED"


def test_download_pdf(tmp_path, monkeypatch):
    monkeypatch.setattr(settings, "jobs_dir", str(tmp_path / "jobs"), raising=False)
    monkeypatch.setattr(settings, "idem_dir", str(tmp_path / "idem"), raising=False)
    monkeypatch.setattr(settings, "artifacts_dir", str(tmp_path / "artifacts"), raising=False)

    job_id = "job-123"
    pdf_path = tmp_path / "artifacts" / f"{job_id}.pdf"
    pdf_path.parent.mkdir(parents=True, exist_ok=True)
    pdf_bytes = b"%PDF-1.4\n%fake\n"
    pdf_path.write_bytes(pdf_bytes)

    write_job(job_id, "PRINTED", artifact_path=str(pdf_path))

    client = TestClient(app)
    r = client.get(f"/v1/download/{job_id}")
    assert r.status_code == 200
    assert r.headers["content-type"].startswith("application/pdf")
    assert r.content == pdf_bytes
