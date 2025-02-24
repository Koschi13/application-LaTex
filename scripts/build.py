#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.12"
# dependencies = [
#     "typer",
# ]
# ///
import os
import subprocess
from typing import Optional
import typer

app = typer.Typer(help="Build LaTeX documents from templates.")

@app.command()
def build(
    project_root: str = typer.Option(None, help="Path to the Project root. If not provided the Git root is used (if available)."),
    output_dir: str = typer.Option(None, help="Path to the output directory."),
    attachments_dir: str = typer.Option(None, help="Path to the attachments directory."),
    content_dir: str = typer.Option(None, help="Path to the content directory.")
):
    PROJECT_ROOT = project_root or subprocess.getoutput("git rev-parse --show-toplevel")
    OUTPUT_DIR = output_dir or os.path.join(PROJECT_ROOT, "build/")
    ATTACHMENTS_DIR = attachments_dir or os.path.join(PROJECT_ROOT, "example/attachments/")
    CONTENT_DIR = content_dir or os.path.join(PROJECT_ROOT, "example/content/")
    ORIGINAL_DIR = os.getcwd()

    os.chdir(os.path.join(PROJECT_ROOT, "templates/"))

    def build_latex(input_file):
        command = (
            f"pdflatex --output-directory={OUTPUT_DIR} "
            f"\"\\def\\contentDir{{{CONTENT_DIR}}} "
            f"\\def\\attachmentsDir{{{ATTACHMENTS_DIR}}} "
            f"\\def\\outputDir{{{OUTPUT_DIR}}} "
            f"\\input{{{input_file}}}\""
        )
        subprocess.run(command, shell=True, check=True)

    # Clean and recreate output directory
    if os.path.exists(OUTPUT_DIR):
        subprocess.run(f"rm -r {OUTPUT_DIR}", shell=True, check=True)
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    try:
        build_latex("letter.tex")
        build_latex("cv.tex")
        build_latex("cv.tex")  # Run again for correct page numbers
        build_latex("application.tex")

    except subprocess.CalledProcessError as e:
        typer.secho(f"Error during LaTeX build: {e}", fg=typer.colors.RED)
        os.chdir(ORIGINAL_DIR)
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()