import os
from app.store import create_or_get_job, write_job, read_job
from app.config import settings


def test_create_or_get_job_idempotency(tmp_path, monkeypatch):
    # 一時ディレクトリに切替
    jobs = tmp_path / "jobs"
    idem = tmp_path / "idem"
    arts = tmp_path / "artifacts"
    monkeypatch.setattr(settings, "jobs_dir", str(jobs), raising=False)
    monkeypatch.setattr(settings, "idem_dir", str(idem), raising=False)
    monkeypatch.setattr(settings, "artifacts_dir", str(arts), raising=False)

    job_id, created = create_or_get_job("dev1", "key-12345678", "job-1")
    assert created is True
    assert job_id == "job-1"

    # 同じキーでもう一度: 既存の job が返る
    job_id2, created2 = create_or_get_job("dev1", "key-12345678", "job-2")
    assert created2 is False
    assert job_id2 == job_id


def test_write_and_read_job(tmp_path, monkeypatch):
    jobs = tmp_path / "jobs"
    idem = tmp_path / "idem"
    arts = tmp_path / "artifacts"
    monkeypatch.setattr(settings, "jobs_dir", str(jobs), raising=False)
    monkeypatch.setattr(settings, "idem_dir", str(idem), raising=False)
    monkeypatch.setattr(settings, "artifacts_dir", str(arts), raising=False)

    job_id, _ = create_or_get_job("devX", "key-abcdefgh", "job-xyz")
    write_job(job_id, "RECEIVED")

    obj = read_job(job_id)
    assert obj["job_id"] == job_id
    assert obj["status"] == "RECEIVED"
    assert obj["error"] is None
    assert "updated_at" in obj

