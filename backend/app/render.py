import os
from jinja2 import Environment, FileSystemLoader, select_autoescape, TemplateNotFound
try:
    from weasyprint import HTML  # type: ignore
except Exception:  # 環境に weasyprint 依存がない場合に備える
    HTML = None  # type: ignore
from .config import settings
from .models import PrintDoc
import json

_env = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape(["html", "xml"]),
)


class RenderError(Exception):
    """Raised when rendering (templating/PDF) fails."""
    pass

def render_pdf(job_id: str, template_id: str, doc: PrintDoc) -> str:
    template_name = f"{template_id}.html.j2"
    try:
        template = _env.get_template(template_name)
    except TemplateNotFound as e:
        raise RenderError(f"template not found: {template_name}") from e

    html_str = template.render(
        title=doc.title,
        body=doc.body,
        bullets=doc.bullets,
    )

    os.makedirs(settings.artifacts_dir, exist_ok=True)
    pdf_path = os.path.join(settings.artifacts_dir, f"{job_id}.pdf")

    if HTML is None:
        # テスト環境や最小依存環境では weasyprint がないことがある
        raise RenderError("WeasyPrint not available")

    try:
        HTML(string=html_str, base_url=os.getcwd()).write_pdf(pdf_path)
    except Exception as e:
        # WeasyPrint の失敗をレンダリングエラーとして包む
        raise RenderError(f"pdf generation failed: {e}") from e
    return pdf_path


#デバッグ用
if name == 'main':
    with open("data/idem/print_doc_sample_simple.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    doc = PrintDoc.model_validate(data)
    pdf_path = render_pdf("1", "index", doc)
    print("PDF generated:", pdf_path)