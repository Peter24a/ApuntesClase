# Cuadernillo de actividades

Paquete autónomo y editable del cuadernillo de **Razonamiento computacional y
diseño de algoritmos**. Incluye el proyecto LaTeX, el PDF compilado, los apuntes
fuente en Markdown y una versión Markdown con diagramas SVG.

## Contenido

```text
cuadernillo-actividades/
|-- cuadernillo.tex             Archivo maestro de LaTeX
|-- 01_documento.md             Apuntes fuente
|-- compilar.ps1                Compilación en PowerShell
|-- compilar.bat                Compilación por doble clic en Windows
|-- compilar.sh                 Compilación en Linux o macOS
|-- contenido/
|   |-- 10-apuntes-clase.tex    Contenido editable del PDF
|   `-- diagramas/              Diagramas TikZ editables
|-- herramientas/               Conversores y generador de diagramas
|-- version-md/
|   |-- apuntes.md              Markdown visual generado
|   |-- actualizar.ps1          Automatización de los SVG
|   `-- diagramas/              Diagramas SVG vectoriales
`-- output/pdf/cuadernillo.pdf  PDF final
```

## Recompilar el PDF

### Windows

Puede hacerse doble clic en `compilar.bat` o ejecutar desde PowerShell:

```powershell
./compilar.ps1
```

### Linux o macOS

```bash
chmod +x compilar.sh
./compilar.sh
```

El resultado se guarda en `output/pdf/cuadernillo.pdf`.

## Editar el cuadernillo

- Los datos de portada están al comienzo de `cuadernillo.tex`.
- El texto del PDF está en `contenido/10-apuntes-clase.tex`.
- Cada diagrama TikZ se encuentra en `contenido/diagramas/`.
- Después de cualquier cambio debe ejecutarse nuevamente el script de compilación.

## Actualizar la versión Markdown visual

Los apuntes Markdown se editan en `01_documento.md`. Para volver a crear
`version-md/apuntes.md` y sus SVG, ejecutar:

```powershell
cd version-md
./actualizar.ps1
```

La automatización también regenera los archivos TikZ de `contenido/diagramas/`.
Si se modifica el texto narrativo del Markdown, el cambio no se copia
automáticamente a `contenido/10-apuntes-clase.tex`; ese archivo debe ajustarse
directamente para reflejar el cambio en el PDF.

## Requisitos

Para compilar el PDF:

- MiKTeX o TeX Live con `pdflatex`.
- Se recomienda `latexmk`, aunque los scripts pueden usar `pdflatex` directamente.
- Paquetes LaTeX habituales, incluidos TikZ, `tcolorbox`, `adjustbox`, `longtable`,
  `listings`, `babel-spanish` y `lmodern`.

Para regenerar la versión Markdown visual también se requiere:

- Python 3.
- `pdftocairo`, normalmente incluido con MiKTeX, TeX Live o Poppler.

## Overleaf

Se puede subir el contenido completo de esta carpeta a Overleaf. El archivo
principal es `cuadernillo.tex` y el compilador recomendado es **pdfLaTeX**.
