import re
import shutil
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FOLDER = Path(__file__).resolve().parent
SOURCE = ROOT / "01_documento.md"
TIKZ_FOLDER = ROOT / "contenido" / "diagramas"
SVG_FOLDER = FOLDER / "diagramas"
TEMP_FOLDER = ROOT / "tmp" / "markdown-visual"
OUTPUT = FOLDER / "apuntes.md"


def run(command, cwd=ROOT, quiet=False):
    if not quiet:
        subprocess.run(command, cwd=cwd, check=True)
        return
    result = subprocess.run(
        command,
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
    )
    if result.returncode:
        print(result.stdout)
        raise subprocess.CalledProcessError(result.returncode, command)


def executable(name):
    found = shutil.which(name)
    if not found:
        raise RuntimeError(
            f"No se encontró '{name}'. Instala MiKTeX con esa herramienta disponible."
        )
    return found


def latex_style():
    main = (ROOT / "cuadernillo.tex").read_text(encoding="utf-8")
    colors = "\n".join(re.findall(r"^\\definecolor\{.*$", main, flags=re.M))
    start = main.index("% --- Diagramas de flujo")
    end = main.index("% --- Encabezados y enlaces", start)
    diagram_style = main[start:end]
    return colors + "\n" + diagram_style


def standalone_document(tikz_source, style):
    picture = re.search(
        r"\\begin\{tikzpicture\}.*?\\end\{tikzpicture\}",
        tikz_source,
        flags=re.S,
    )
    if not picture:
        raise ValueError("No se encontró el entorno tikzpicture.")
    return (
        "\\documentclass[tikz,border=4pt]{standalone}\n"
        "\\usepackage[T1]{fontenc}\n"
        "\\usepackage[utf8]{inputenc}\n"
        "\\usepackage{lmodern}\n"
        "\\usepackage{xcolor}\n"
        + style
        + "\n\\begin{document}\n"
        + picture.group(0)
        + "\n\\end{document}\n"
    )


def export_svgs():
    python = sys.executable
    pdflatex = executable("pdflatex")
    pdftocairo = executable("pdftocairo")
    run([python, str(ROOT / "herramientas" / "generar_diagramas.py")])

    SVG_FOLDER.mkdir(parents=True, exist_ok=True)
    TEMP_FOLDER.mkdir(parents=True, exist_ok=True)
    for previous in SVG_FOLDER.glob("diagrama-*.svg"):
        previous.unlink()

    style = latex_style()
    diagrams = sorted(TIKZ_FOLDER.glob("diagrama-*.tex"))
    for diagram in diagrams:
        stem = diagram.stem
        tex = TEMP_FOLDER / f"{stem}.tex"
        tex.write_text(
            standalone_document(diagram.read_text(encoding="utf-8"), style),
            encoding="utf-8",
        )
        run([
            pdflatex,
            "-interaction=nonstopmode",
            "-halt-on-error",
            f"-output-directory={TEMP_FOLDER}",
            str(tex),
        ], quiet=True)
        run([
            pdftocairo,
            "-svg",
            str(TEMP_FOLDER / f"{stem}.pdf"),
            str(SVG_FOLDER / f"{stem}.svg"),
        ], quiet=True)
    return len(diagrams)


def generate_markdown(expected):
    markdown = SOURCE.read_text(encoding="utf-8")
    counter = 0

    def replace(_match):
        nonlocal counter
        counter += 1
        name = f"diagrama-{counter:02d}.svg"
        return f"![Diagrama de flujo {counter}](diagramas/{name})"

    result = re.sub(r"```mermaid\s*\n.*?\n```", replace, markdown, flags=re.S)
    if counter != expected:
        raise RuntimeError(
            f"Se detectaron {counter} bloques Mermaid, pero se exportaron {expected} SVG."
        )
    notice = (
        "<!-- ARCHIVO GENERADO AUTOMÁTICAMENTE. "
        "Edita ../01_documento.md y ejecuta ./actualizar.ps1. -->\n\n"
    )
    OUTPUT.write_text(notice + result, encoding="utf-8")
    return counter


def main():
    count = export_svgs()
    generate_markdown(count)
    print(f"Listo: {OUTPUT}")
    print(f"Diagramas SVG generados: {count}")


if __name__ == "__main__":
    main()
