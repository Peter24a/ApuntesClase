$ErrorActionPreference = 'Stop'

$raizCuadernillo = Split-Path -Parent $MyInvocation.MyCommand.Path
Push-Location $raizCuadernillo
try {
    $salidaPdf = Join-Path $raizCuadernillo 'output/pdf'
    New-Item -ItemType Directory -Force -Path $salidaPdf | Out-Null
    $argumentoSalida = "-outdir=$salidaPdf"
    latexmk -pdf $argumentoSalida -interaction=nonstopmode -halt-on-error cuadernillo.tex
}
finally {
    Pop-Location
}
