import types
import subprocess
import pytest

from app.print_service import print_pdf, PrintError
from app import print_service as ps


def test_print_pdf_calls_script_with_printer(monkeypatch, tmp_path):
    # プリンタ名を設定
    monkeypatch.setattr(ps.settings, "printer_name", "PRN001", raising=False)

    called = {}

    def fake_run(cmd, check, text, capture_output):
        called["cmd"] = cmd
        # 成功として何も返さない（呼び出し側は値を使用しない）
        return types.SimpleNamespace()

    monkeypatch.setattr(subprocess, "run", fake_run)

    pdf = str(tmp_path / "sample.pdf")
    print_pdf(pdf, 2)

    assert called["cmd"] == [
        "bash",
        "scripts/print_pdf.sh",
        pdf,
        "2",
        "PRN001",
    ]


def test_print_pdf_raises_on_failure(monkeypatch, tmp_path):
    monkeypatch.setattr(ps.settings, "printer_name", "PRN001", raising=False)

    def fail_run(cmd, check, text, capture_output):
        raise subprocess.CalledProcessError(returncode=1, cmd=cmd, stderr="boom")

    monkeypatch.setattr(subprocess, "run", fail_run)

    with pytest.raises(PrintError):
        print_pdf(str(tmp_path / "x.pdf"), 1)

