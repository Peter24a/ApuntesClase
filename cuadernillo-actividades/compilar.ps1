$ErrorActionPreference = 'Stop'
$raiz = Split-Path -Parent $MyInvocation.MyCommand.Path
Push-Location $raiz
try {
    $salidaPdf = Join-Path $raiz 'output\pdf'
    if (-not (Test-Path $salidaPdf)) {
        New-Item -ItemType Directory -Force -Path $salidaPdf | Out-Null
    }
    Write-Host "Compilando cuadernillo.tex..." -ForegroundColor Cyan
    if (Get-Command latexmk -ErrorAction SilentlyContinue) {
        latexmk -pdf -outdir="$salidaPdf" -interaction=nonstopmode -halt-on-error cuadernillo.tex
    }
    elseif (Get-Command pdflatex -ErrorAction SilentlyContinue) {
        pdflatex -output-directory="$salidaPdf" -interaction=nonstopmode -halt-on-error cuadernillo.tex
        pdflatex -output-directory="$salidaPdf" -interaction=nonstopmode -halt-on-error cuadernillo.tex
    }
    else {
        throw "No se encontro 'latexmk' ni 'pdflatex' en el PATH. Instala una distribucion de LaTeX (MiKTeX o TeX Live)."
    }
    $pdfPath = Join-Path $salidaPdf 'cuadernillo.pdf'
    if (Test-Path $pdfPath) {
        Write-Host "Compilacion exitosa: $pdfPath" -ForegroundColor Green
    }
}
finally {
    Pop-Location
}
