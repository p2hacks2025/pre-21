import os
from jinja2 import Environment, FileSystemLoader

# -------------------------------------------------
# 1. テスト用のデータ（ここで表示内容を変えられます）
# -------------------------------------------------
dummy_data = {
    "name": "夜空",           # 漢字の名前
    "ruby": "よぞら",       # ふりがな
    "bullets": [             # 箇条書きデータ
        "星がきれい",
        "月が輝く夜",
        "静かな時間"
    ]
}

# -------------------------------------------------
# 2. テンプレートを読み込んでHTMLを作る
# -------------------------------------------------
def generate_preview():
    # テンプレートがあるフォルダを指定
    # (このスクリプトと同じ場所に templates フォルダがある前提)
    loader = FileSystemLoader("templates")
    env = Environment(loader=loader)

    try:
        # 読み込むテンプレートファイル名（適宜書き換えてください）
        template = env.get_template("default.html.j2")
    except Exception as e:
        print(f"エラー: テンプレートが見つかりません。\n詳細: {e}")
        return

    # データを流し込む
    html_str = template.render(**dummy_data)

    # HTMLファイルとして保存
    output_filename = "design_preview.html"
    with open(output_filename, "w", encoding="utf-8") as f:
        f.write(html_str)

    print("-" * 30)
    print(f"成功！ '{output_filename}' を作成しました。")
    print("このファイルをブラウザで開いてデザインを確認してください。")
    print("-" * 30)

if __name__ == "__main__":
    generate_preview()