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
