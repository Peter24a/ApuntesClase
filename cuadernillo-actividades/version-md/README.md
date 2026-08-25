# Versión Markdown visual

Esta carpeta contiene una copia de los apuntes cuyos diagramas se muestran como
SVG, con las mismas figuras, colores y rutas utilizadas por el cuadernillo.

## Actualizar

1. Edita el archivo fuente `../01_documento.md`.
2. Agrega, elimina o modifica los bloques `mermaid` normalmente.
3. Desde PowerShell ejecuta:

   ```powershell
   ./actualizar.ps1
   ```

El proceso realiza automáticamente lo siguiente:

- Regenera los diagramas TikZ del cuadernillo.
- Exporta cada diagrama como SVG vectorial en `diagramas/`.
- Crea `apuntes.md` sustituyendo los bloques Mermaid por las imágenes SVG.
- Elimina diagramas generados que ya no correspondan con el archivo fuente.

`apuntes.md` es un archivo generado: no debe editarse directamente.

## Requisitos

- Python 3.
- MiKTeX con `pdflatex` y `pdftocairo` disponibles en la variable `PATH`.
