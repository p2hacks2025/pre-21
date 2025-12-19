import subprocess
from subprocess import CalledProcessError
from .config import settings

class PrintError(Exception):
    """Raised when printing fails."""

def print_pdf(pdf_path: str, copies: int = 1) -> None:
    """
    Print the PDF file at pdf_path copies times using scripts/print_pdf.sh.
    """
    printer = settings.printer_name or ""
    cmd = ["bash", "scripts/print_pdf.sh", pdf_path, str(copies), printer]
    # helpful debug output
    print("Running print command:", cmd)
    try:
        subprocess.run(cmd, check=True, text=True, capture_output=True)
    except CalledProcessError as e:
        raise PrintError(f"Print failed: {e.stderr}") from e


if __name__ == "__main__":
    print_pdf("data/artifacts/1.pdf", 1)
