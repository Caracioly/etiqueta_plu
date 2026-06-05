@echo off
REM Build do EtiquetaPLU (CMD)
REM Uso:  build.bat
REM Gera dist\EtiquetaPLU\EtiquetaPLU.exe (modo onedir, abertura rapida, sem UAC).

echo Limpando builds anteriores...
if exist build rmdir /s /q build
if exist dist  rmdir /s /q dist

echo Compilando com PyInstaller...
pyinstaller main.spec --noconfirm
if errorlevel 1 (
    echo.
    echo ERRO: falha no PyInstaller.
    exit /b 1
)

echo.
echo Build concluido!
echo Executavel: dist\EtiquetaPLU\EtiquetaPLU.exe
