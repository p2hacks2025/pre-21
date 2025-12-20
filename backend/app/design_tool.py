import argparse
import json
import os
from jinja2 import Environment, FileSystemLoader, select_autoescape, TemplateNotFound
from app.config import settings


def generate_preview(job_id: str) -> str | None:
    loader = FileSystemLoader("templates")
    env = Environment(
        loader=loader,
        autoescape=select_autoescape(["html", "xml"]),
    )

    llm_path = os.path.join(settings.llm_dir, f"{job_id}.json")
    if not os.path.exists(llm_path):
        print(f"エラー: LLMデータが見つかりません: {llm_path}")
        return None

    try:
        template = env.get_template("default.html.j2")
    except TemplateNotFound as e:
        print(f"エラー: テンプレートが見つかりません。\n詳細: {e}")
        return None

    try:
        with open(llm_path, "r", encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        print(f"エラー: JSONの読み込みに失敗しました。\n詳細: {e}")
        return None

    html_str = template.render(**data)

    output_dir = os.path.join(settings.data_dir, "html")
    os.makedirs(output_dir, exist_ok=True)
    output_filename = os.path.join(output_dir, f"{job_id}.html")
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(html_str)

    print("-" * 30)
    print(f"成功！ '{output_filename}' を作成しました。")
    print("このファイルをブラウザで開いてデザインを確認してください。")
    print("-" * 30)
    return output_filename


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="LLM JSONをdefault.html.j2に埋め込み、HTMLを生成します。"
    )
    parser.add_argument("job_id", help="LLM JSONのjob_id (llm/{job_id}.json)")
    args = parser.parse_args()
    generate_preview(args.job_id)
