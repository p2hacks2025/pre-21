from pathlib import Path
import subprocess

def print_service(pdf_path : str):
    here = Path(__file__).resolve().parent        # .../backend/app
    script = (here / ".." / "scripts" / "print_pdf.sh").resolve()  # .../backend/scripts/test.sh

    pdf = Path(pdf_path).resolve()

    if not script.exists():
        raise FileNotFoundError(f"script not found: {script}")

    subprocess.run(["bash", str(script), str(pdf)], check=True)

if __name__ == "__main__":
    print_service("./data/artifacts/1.pdf")