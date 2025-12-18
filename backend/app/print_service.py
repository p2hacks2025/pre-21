import subprocess

def print_pdf(copies: str) -> None:
    cmd = ["bash", "scripts/print_pdf.sh", "data/artifacts" + "/" + f"{copies}.pdf"]

    print(cmd)

    subprocess.run(cmd, check=True, text=True, capture_output=True)


if __name__ == "__main__":
    print_pdf("1")