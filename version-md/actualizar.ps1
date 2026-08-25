$ErrorActionPreference = 'Stop'

$carpeta = Split-Path -Parent $MyInvocation.MyCommand.Path
$pythonIncluido = Join-Path $env:USERPROFILE '.cache\codex-runtimes\codex-primary-runtime\dependencies\python\python.exe'

if (Test-Path -LiteralPath $pythonIncluido) {
    $python = $pythonIncluido
}
else {
    $python = (Get-Command python -ErrorAction Stop).Source
}

Push-Location $carpeta
try {
    & $python (Join-Path $carpeta 'actualizar.py')
    if ($LASTEXITCODE -ne 0) {
        throw "No se pudo actualizar la versión Markdown."
    }
}
finally {
    Pop-Location
}
