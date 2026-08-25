# Cuadernillo de actividades

Plantilla modular en LaTeX para construir el cuadernillo del parcial a partir
de apuntes Markdown.

## Uso

1. Edita en `cuadernillo.tex` los comandos `\Asignatura`, `\NumeroParcial`,
   `\Docente`, `\Estudiante`, `\Grupo` y `\Periodo`.
2. Deposita los apuntes `.md` en `apuntes-md/`.
3. Incorpora los temas convertidos como archivos `.tex` dentro de `contenido/`
   y agrégalos con `\input{contenido/nombre}` en `cuadernillo.tex`.
4. Ejecuta `./compilar.ps1` desde PowerShell.

El PDF terminado se guarda en `output/pdf/cuadernillo.pdf`.

El apéndice `contenido/90-demo-diagramas.tex` contiene símbolos vectoriales de
diagramas de flujo, incluido el documento con borde inferior ondulado.
