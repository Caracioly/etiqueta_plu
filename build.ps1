# Build do EtiquetaPLU (PowerShell)
# Uso:  .\build.ps1
#
# Gera dist\EtiquetaPLU\EtiquetaPLU.exe (modo onedir, abertura rapida, sem UAC).

$ErrorActionPreference = "Stop"

Write-Host "Limpando builds anteriores..." -ForegroundColor Cyan
if (Test-Path "build") { Remove-Item -Recurse -Force "build" }
if (Test-Path "dist")  { Remove-Item -Recurse -Force "dist" }

Write-Host "Compilando com PyInstaller..." -ForegroundColor Cyan
pyinstaller main.spec --noconfirm
if ($LASTEXITCODE -ne 0) { throw "Falha no PyInstaller (exit $LASTEXITCODE)" }

Write-Host ""
Write-Host "Build concluido!" -ForegroundColor Green
Write-Host "Executavel: dist\EtiquetaPLU\EtiquetaPLU.exe"
