; Instalador do EtiquetaPLU - Inno Setup
; Pre-requisito: build feito (dist\EtiquetaPLU\) via .\build.ps1
; Compilar: abrir este arquivo no Inno Setup Compiler e clicar em Compile,
;           ou rodar  iscc installer.iss
; Resultado: dist_installer\EtiquetaPLU_Setup.exe

#define MyAppName "EtiquetaPLU"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Super Somar LTDA"
#define MyAppExeName "EtiquetaPLU.exe"

[Setup]
AppId={{A1F4E2B7-9C3D-4E6A-8B12-ETIQUETA0PLU}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
OutputDir=dist_installer
OutputBaseFilename=EtiquetaPLU_Setup
SetupIconFile=imagens\logo.ico
Compression=lzma2
SolidCompression=yes
WizardStyle=modern
; NAO exige administrador: instala no perfil do usuario por padrao.
PrivilegesRequiredOverridesAllowed=dialog
PrivilegesRequired=lowest

[Languages]
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"

[Tasks]
Name: "desktopicon"; Description: "Criar atalho na area de trabalho"; GroupDescription: "Atalhos adicionais:"

[Files]
; Empacota toda a pasta gerada pelo PyInstaller (modo onedir)
Source: "dist\EtiquetaPLU\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Abrir {#MyAppName} agora"; Flags: nowait postinstall skipifsilent
