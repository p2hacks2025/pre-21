import os
from app.render import render_pdf, RenderError, HTML as REAL_HTML
from app.models import PrintDoc
from app.config import settings
import types


def test_render_missing_template_raises(tmp_path, monkeypatch):
    # 出力先を一時ディレクトリに変更
    monkeypatch.setattr(settings, "artifacts_dir", str(tmp_path), raising=False)

    doc = PrintDoc(title="t", body="b", bullets=["x"])
    with raise_render_error():
        render_pdf("job-1", "__no_such_template__", doc)


def test_render_success_creates_pdf(tmp_path, monkeypatch):
    # 出力先を一時ディレクトリに変更
    monkeypatch.setattr(settings, "artifacts_dir", str(tmp_path), raising=False)

    # WeasyPrint の HTML.write_pdf を差し替えて副作用を軽量化
    class FakeHTML:
        def __init__(self, *args, **kwargs):
            pass

        def write_pdf(self, pdf_path):
            # 生成物として空ファイルを作る
            with open(pdf_path, "wb") as f:
                f.write(b"")

    from app import render as r
    monkeypatch.setattr(r, "HTML", FakeHTML, raising=True)

    doc = PrintDoc(title="Title", body="Body", bullets=["a", "b"])
    out = render_pdf("job-xyz", "index", doc)
    assert os.path.exists(out)


# ヘルパ: RenderError を期待する with 構文
from contextlib import contextmanager


@contextmanager
def raise_render_error():
    try:
        yield
        assert False, "RenderError was not raised"
    except RenderError:
        pass

