#!/usr/bin/env bash
set -e

DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" >/dev/null 2>&1 && pwd)"
cd "$DIR"

mkdir -p output/pdf

echo "Compilando cuadernillo.tex..."

if command -v latexmk >/dev/null 2>&1; then
    latexmk -pdf -outdir=output/pdf -interaction=nonstopmode -halt-on-error cuadernillo.tex
elif command -v pdflatex >/dev/null 2>&1; then
    pdflatex -output-directory=output/pdf -interaction=nonstopmode -halt-on-error cuadernillo.tex
    pdflatex -output-directory=output/pdf -interaction=nonstopmode -halt-on-error cuadernillo.tex
else
    echo "ERROR: No se encontro 'latexmk' ni 'pdflatex' en el PATH."
    echo "Por favor instala TeX Live o MacTeX."
    exit 1
fi

if [ -f "output/pdf/cuadernillo.pdf" ]; then
    echo "Compilacion exitosa: output/pdf/cuadernillo.pdf"
fi
