# -*- mode: python ; coding: utf-8 -*-
# Build:  pyinstaller main.spec
#
# Configuracao:
#   - onedir  -> abertura rapida (nao descompacta tudo na temp a cada execucao)
#   - uac_admin=False -> NAO pede permissao de Administrador
#                        (o banco vai para %LOCALAPPDATA%\EtiquetaPLU, sempre gravavel)

block_cipher = None


a = Analysis(
    ["main.py"],
    pathex=[],
    binaries=[],
    datas=[
        ("imagens", "imagens"),
    ],
    hiddenimports=[
        "win32print",
        "openpyxl",
        "xlrd",
        "requests",
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name="EtiquetaPLU",
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    uac_admin=False,
    icon="imagens/logo.ico",
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name="EtiquetaPLU",
)
