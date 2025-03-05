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
from pathlib import Path

PROJECT_ROOT_DIR = Path(__file__).parent.parent.absolute()
app = typer.Typer(help="Build LaTeX documents from templates.")

def get_git_root_or_default() -> Path:
    code, output = subprocess.getstatusoutput("git rev-parse --show-toplevel")
    if code != 0:
        return PROJECT_ROOT_DIR
    return Path(output).absolute()

@app.command()
def build(
    project_root: Path = typer.Option(help="Path to the Project root. Defaults to the git root or the parent direcotory of this script if not a git repo.", default_factory=get_git_root_or_default),
    output_dir: Path = typer.Option(get_git_root_or_default() / "build/", help="Path to the output directory."),
    attachments_dir: Path = typer.Option(get_git_root_or_default() / "example/attachments/", help="Path to the attachments directory."),
    content_dir: Path = typer.Option(get_git_root_or_default() / "example/content/", help="Path to the content directory."),
    language_file: Path = typer.Option(get_git_root_or_default() / "language/german.tex", help="Path to the language file."),
):
    if not attachments_dir.exists():
        raise RuntimeError(f"Directory '{attachments_dir}' does not exist!")
    elif not attachments_dir.is_dir():
        raise RuntimeError(f"{attachments_dir} is not a directory!")
    elif not attachments_dir.is_absolute():
        attachments_dir = attachments_dir.absolute()
    
    if not content_dir.exists():
        raise RuntimeError(f"Directory '{content_dir}' does not exist!")
    elif not content_dir.is_dir():
        raise RuntimeError(f"{content_dir} is not a directory!")
    elif not content_dir.is_absolute():
        content_dir = content_dir.absolute()

    if not language_file.exists():
        raise RuntimeError(f"File '{content_dir}' does not exist!")
    elif not language_file.is_file():
        raise RuntimeError(f"{language_file} is not a directory!")
    elif not language_file.is_absolute():
        language_file = language_file.absolute()

    original_dir = os.getcwd()

    os.chdir(os.path.join(project_root, "templates/"))

    def build_latex(input_file):
        command = (
            f"pdflatex --output-directory={output_dir} \""
            f"\\def\\contentDir{{{content_dir}}} "
            f"\\def\\attachmentsDir{{{attachments_dir}}} "
            f"\\def\\outputDir{{{output_dir}}} "
            f"\\def\\languageFile{{{language_file}}} "
            f"\\input{{{input_file}}}"
            "\""
        )
        subprocess.run(command, shell=True, check=True)

    # Clean and recreate output directory
    if os.path.exists(output_dir):
        subprocess.run(f"rm -r {output_dir}", shell=True, check=True)
    os.makedirs(output_dir, exist_ok=True)

    try:
        build_latex("letter.tex")
        build_latex("cv.tex")
        build_latex("cv.tex")  # Run again for correct page numbers
        build_latex("application.tex")

    except subprocess.CalledProcessError as e:
        typer.secho(f"Error during LaTeX build: {e}", fg=typer.colors.RED)
        os.chdir(original_dir)
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()