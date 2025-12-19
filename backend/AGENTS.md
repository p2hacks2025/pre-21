# Repository Guidelines

## プロジェクト構成とモジュール
- `app/`: FastAPIアプリ本体。API (`app/main.py`)、モデル、各サービス。
- `test/`: pytestのテスト一式（例: `test/test_main.py`, `test/test_store.py`）。
- `templates/`: PDF生成に使うJinja2テンプレート（`templates/index.html.j2`）。
- `scripts/`: 開発/運用向けスクリプト（`scripts/dev.sh`, `scripts/test.sh`, `scripts/print_pdf.sh`）。
- `data/`: 実行時に生成されるジョブ状態や成果物（JSON、PDF）。
- `font/`: PDFレンダリング用フォント（`font/ipamjm.ttf`）。
- `output/`: 生成物置き場。必要性が明示されない限り一時ファイル扱い。

## ビルド/テスト/開発コマンド
- `pip install -r requirements.txt`: 依存関係のインストール。
- `scripts/dev.sh`: リロード付きでFastAPIを起動（`uvicorn app.main:app`）。
- `scripts/test.sh`: pytestでテスト実行（`pytest -q`）。
- `scripts/print_pdf.sh <pdf> [copies] [printer]`: CUPSの`lp`でPDF印刷。

## コーディング規約と命名
- Python、インデントは4スペース、PEP 8準拠を意識。
- 関数/変数は`snake_case`、クラスは`PascalCase`。
- 可能な範囲で型ヒントを付与（`app/store.py`参照）。
- APIエンドポイントは`app/main.py`に集約し、追加サービスは`app/`配下へ。

## テスト方針
- フレームワーク: pytest。
- 命名規則: ファイルは`test_*.py`、関数は`test_*`。
- 実行方法: `scripts/test.sh`または`pytest -q`。
- 新規APIやジョブの状態遷移にはテスト追加を推奨。

## コミット & PR ガイドライン
- 履歴は説明的な文体（日本語が多め）。同じトーンで具体的に書く。
- PRには概要、実行したテスト、設定変更や必要な環境変数を記載。

## 設定と環境
- ローカル開発では`.env`を`app/config.py`が自動読み込み。
- 主要変数: `GEMINI_API_KEY`, `GEMINI_MODEL`, `BASE_URL`, `PRINTER_NAME`, `DATA_DIR`, `JOBS_DIR`, `IDEM_DIR`, `ARTIFACTS_DIR`。

## gemini_transformの実装方針
- ESP32から0か1のデータ5個送信されます。それに基づいて場合分けしてプロンプトを変える処理をしたいです
- 最終的にそのgemini apiにデータを送信して結果をjson形式で返します
- 整合性についてはほかファイルの仕様を優先して取ってください