import os
from jinja2 import Environment, FileSystemLoader, select_autoescape
from weasyprint import HTML
from .config import settings
from .models import PrintDoc
import json

_env = Environment(
    loader=FileSystemLoader("templates"),
    autoescape=select_autoescape(["html", "xml"]),
)

def render_pdf(job_id: str, template_id: str, doc: PrintDoc) -> str:
    template_name = f"{template_id}.html.j2"
    template = _env.get_template(template_name)

    html_str = template.render(
        title=doc.title,
        body=doc.body,
        bullets=doc.bullets,
    )

    os.makedirs(settings.artifacts_dir, exist_ok=True)
    pdf_path = os.path.join(settings.artifacts_dir, f"{job_id}.pdf")

    HTML(string=html_str, base_url=os.getcwd()).write_pdf(pdf_path)
    return pdf_path


#デバッグ用
if __name__ == '__main__':
    with open("data/idem/print_doc_sample_simple.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    doc = PrintDoc.model_validate(data)
    pdf_path = render_pdf("1", "index", doc)
    print("PDF generated:", pdf_path)