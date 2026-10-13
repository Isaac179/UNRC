# ============================================================
#  publicar.ps1  -  publica en GitHub lo que ya esta en el repo
#
#  Uso, desde la raiz del repo:
#      powershell -ExecutionPolicy Bypass -File herramientas\publicar.ps1 "mensaje del commit"
#
#  1. Regenera los indices (generar_indices.py)
#  2. Agrega los cambios (git add -A)
#  3. Corre el verificador del restaurante; si falla, se detiene sin publicar
#  4. Hace commit y push
# ============================================================
param([Parameter(Position=0)][string]$Mensaje = "docs: actualizar portafolio")

$ErrorActionPreference = 'Continue'
$Repo = Split-Path -Parent $PSScriptRoot
Set-Location $Repo

function Alto($texto) { Write-Host "ALTO: $texto" -ForegroundColor Red; exit 1 }

$py = (Get-Command python -ErrorAction SilentlyContinue)
if (-not $py) { $py = (Get-Command py -ErrorAction SilentlyContinue) }
if (-not $py) { Alto "No encuentro Python en el PATH." }

Write-Host "[1/4] Regenerando indices..." -ForegroundColor Cyan
& $py.Source herramientas/generar_indices.py
if ($LASTEXITCODE -ne 0) { Alto "fallo generar_indices.py" }

Write-Host "[2/4] Agregando cambios..." -ForegroundColor Cyan
git add -A

Write-Host "[3/4] Verificando el restaurante..." -ForegroundColor Cyan
& $py.Source herramientas/verificar_restaurante.py
if ($LASTEXITCODE -ne 0) { Alto "el verificador encontro problemas; no se publico nada." }

git diff --cached --quiet
if ($LASTEXITCODE -eq 0) { Write-Host "No hay cambios que publicar." -ForegroundColor Yellow; exit 0 }

Write-Host "[4/4] Commit y push..." -ForegroundColor Cyan
git commit -m $Mensaje
if ($LASTEXITCODE -ne 0) { Alto "fallo el commit" }
git push
if ($LASTEXITCODE -ne 0) { Alto "fallo el push (revisa tu conexion o credenciales)" }

Write-Host "Publicado. El sitio se actualiza en 1-2 minutos: https://isaac179.github.io/UNRC/" -ForegroundColor Green
