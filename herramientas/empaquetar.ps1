$ErrorActionPreference = 'Stop'

$origen = 'c:\Users\pedro\work\Peter24a\ApuntesClase'
$destino = Join-Path $origen 'cuadernillo-actividades'

if (Test-Path $destino) {
    Remove-Item -Recurse -Force $destino
}

New-Item -ItemType Directory -Force -Path $destino | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $destino 'contenido') | Out-Null
New-Item -ItemType Directory -Force -Path (Join-Path $destino 'output\pdf') | Out-Null

# 1. Copiar archivo maestro y contenido
Copy-Item (Join-Path $origen 'cuadernillo.tex') $destino
Copy-Item -Recurse (Join-Path $origen 'contenido\*') (Join-Path $destino 'contenido')

# 2. Copiar PDF ya compilado si existe
$pdfOrigen = Join-Path $origen 'output\pdf\cuadernillo.pdf'
if (Test-Path $pdfOrigen) {
    Copy-Item $pdfOrigen (Join-Path $destino 'output\pdf\cuadernillo.pdf')
}

# 3. Crear script compilar.ps1
$scriptPs1 = @'
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
'@
Set-Content -Path (Join-Path $destino 'compilar.ps1') -Value $scriptPs1 -Encoding UTF8

# 4. Crear script compilar.bat
$scriptBat = @'
@echo off
setlocal
cd /d "%~dp0"

if not exist "output\pdf" mkdir "output\pdf"

echo Compilando cuadernillo.tex...
where latexmk >nul 2>nul
if %errorlevel% equ 0 (
    latexmk -pdf -outdir=output\pdf -interaction=nonstopmode -halt-on-error cuadernillo.tex
) else (
    where pdflatex >nul 2>nul
    if %errorlevel% equ 0 (
        pdflatex -output-directory=output\pdf -interaction=nonstopmode -halt-on-error cuadernillo.tex
        pdflatex -output-directory=output\pdf -interaction=nonstopmode -halt-on-error cuadernillo.tex
    ) else (
        echo ERROR: No se encontro latexmk ni pdflatex en el sistema.
        echo Por favor instala MiKTeX o TeX Live.
        pause
        exit /b 1
    )
)

if exist "output\pdf\cuadernillo.pdf" (
    echo.
    echo ========================================================
    echo  Compilacion exitosa!
    echo  El PDF se encuentra en: output\pdf\cuadernillo.pdf
    echo ========================================================
)
echo.
pause
'@
Set-Content -Path (Join-Path $destino 'compilar.bat') -Value $scriptBat -Encoding ASCII

# 5. Crear script compilar.sh
$scriptSh = @'
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
'@
Set-Content -Path (Join-Path $destino 'compilar.sh') -Value $scriptSh -Encoding UTF8

# 6. Crear README.md
$readme = @'
# Cuadernillo de Actividades — Razonamiento Computacional y Diseño de Algoritmos

Paquete modular autónomo en LaTeX listo para compilar y compartir.

---

## 📁 Estructura del Paquete

```text
cuadernillo-actividades/
├── cuadernillo.tex         # Archivo maestro principal de LaTeX
├── compilar.ps1            # Script de compilación para PowerShell (Windows)
├── compilar.bat            # Script de compilación por doble clic (Windows)
├── compilar.sh             # Script de compilación para Bash (Linux / macOS)
├── README.md               # Este archivo de instrucciones
├── contenido/              # Capítulos y temas modulares
│   ├── 10-apuntes-clase.tex
│   ├── 01-presentacion.tex
│   ├── 02-actividades.tex
│   ├── 20-actividades-parcial.tex
│   ├── 90-demo-diagramas.tex
│   └── diagramas/          # 24 diagramas de flujo vectoriales TikZ (.tex)
│       ├── diagrama-01.tex
│       ├── ...
│       └── diagrama-24.tex
└── output/
    └── pdf/
        └── cuadernillo.pdf # PDF compilado final
```

---

## ⚙️ Requisitos

Para recompilar este proyecto se requiere una distribución de LaTeX estándar:

- **Windows**: [MiKTeX](https://miktex.org/) o [TeX Live](https://www.tug.org/texlive/)
- **Linux (Debian/Ubuntu)**: `sudo apt install texlive-latex-extra texlive-lang-spanish latexmk`
- **macOS**: [MacTeX](https://www.tug.org/mactex/)
- **En la nube**: Compatible con [Overleaf](https://www.overleaf.com/) (subiendo la carpeta completa).

---

## 🚀 ¿Cómo compilar?

### En Windows (Opción 1 - Doble clic)
Haz doble clic sobre `compilar.bat`.

### En Windows (Opción 2 - PowerShell)
Abre PowerShell en esta carpeta y ejecuta:
```powershell
.\compilar.ps1
```

### En Linux / macOS (Terminal)
Abre una terminal en esta carpeta y ejecuta:
```bash
chmod +x compilar.sh
./compilar.sh
```

El PDF resultante siempre se genera en:
`output/pdf/cuadernillo.pdf`

---

## ✏️ Personalización

En la cabecera del archivo `cuadernillo.tex` puedes modificar rápidamente los datos del encabezado y la portada:

```latex
\newcommand{\Asignatura}{Razonamiento computacional y diseño de algoritmos}
\newcommand{\NumeroParcial}{1}
\newcommand{\Docente}{Walter Alexander Mata López}
\newcommand{\Estudiante}{}
\newcommand{\Grupo}{}
```
'@
Set-Content -Path (Join-Path $destino 'README.md') -Value $readme -Encoding UTF8

Write-Host "Estructura del paquete generada en: $destino" -ForegroundColor Cyan

# 7. Compilar dentro de la carpeta empaquetada para verificar
Push-Location $destino
try {
    Write-Host "Verificando compilacion dentro del paquete..." -ForegroundColor Cyan
    & .\compilar.ps1
}
finally {
    Pop-Location
}

# 8. Generar archivo ZIP para compartir directamente
$zipDestino = Join-Path $origen 'cuadernillo-actividades.zip'
if (Test-Path $zipDestino) {
    Remove-Item -Force $zipDestino
}
Compress-Archive -Path $destino -DestinationPath $zipDestino
Write-Host "Archivo comprimido listo en: $zipDestino" -ForegroundColor Green
