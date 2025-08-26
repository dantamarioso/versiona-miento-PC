; Script de instalación para Nicole

#define MyAppName "NICOLE"
#define MyAppVersion "0.0.1"
#define MyAppPublisher "ALPHA 22"
#define MyAppURL "nicole.sytes.net"
#define MyAppExeName "nicole.exe"
#define MyAppAssocName "NICOLE"
#define MyAppAssocExt ".myp"
#define MyAppAssocKey StringChange(MyAppAssocName, " ", "") + MyAppAssocExt

[Setup]
AppId={{72B08665-CB80-48F7-A94E-539660FA7FA9}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\Nicole
UninstallDisplayIcon={app}\{#MyAppExeName}
ArchitecturesAllowed=x64compatible
ArchitecturesInstallIn64BitMode=x64compatible
ChangesAssociations=yes
DisableProgramGroupPage=yes
LicenseFile=C:\Users\danta\Downloads\APP\versiona-miento-PC\License.txt
InfoBeforeFile=C:\Users\danta\Downloads\APP\versiona-miento-PC\INSTRUCIONES.txt
PrivilegesRequiredOverridesAllowed=dialog
OutputBaseFilename=Nicole
SetupIconFile=C:\Users\danta\Downloads\APP\versiona-miento-PC\brain_icon.ico
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; Ejecutable
Source: "C:\Users\danta\Downloads\APP\versiona-miento-PC\dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
; Archivo de configuración .env
Source: "C:\Users\danta\Downloads\APP\versiona-miento-PC\.env"; DestDir: "{app}"; Flags: ignoreversion
; Manual principal (html)
Source: "C:\Users\danta\Downloads\manual\now.html"; DestDir: "{app}\manual"; Flags: ignoreversion
; Carpeta completa del manual
Source: "C:\Users\danta\Downloads\manual\*"; DestDir: "{app}\manual"; Flags: ignoreversion recursesubdirs createallsubdirs

[Registry]
Root: HKA; Subkey: "Software\Classes\{#MyAppAssocExt}\OpenWithProgids"; ValueType: string; ValueName: "{#MyAppAssocKey}"; ValueData: ""; Flags: uninsdeletevalue
Root: HKA; Subkey: "Software\Classes\{#MyAppAssocKey}"; ValueType: string; ValueName: ""; ValueData: "{#MyAppAssocName}"; Flags: uninsdeletekey
Root: HKA; Subkey: "Software\Classes\{#MyAppAssocKey}\DefaultIcon"; ValueType: string; ValueName: ""; ValueData: "{app}\{#MyAppExeName},0"; Flags: uninsdeletekey
Root: HKA; Subkey: "Software\Classes\{#MyAppAssocKey}\shell\open\command"; ValueType: string; ValueName: ""; ValueData: """{app}\{#MyAppExeName}"" ""%1"""; Flags: uninsdeletekey

[Icons]
; Accesos directos al programa
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; WorkingDir: "{app}"; Tasks: desktopicon

; Accesos directos al manual (siempre se crean)
Name: "{autoprograms}\Manual de {#MyAppName}"; Filename: "{app}\manual\now.html"
Name: "{autodesktop}\Manual de {#MyAppName}"; Filename: "{app}\manual\now.html"

[Run]
; Ejecutar el programa al finalizar instalación
Filename: "{app}\{#MyAppExeName}"; \
    Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; \
    Flags: nowait postinstall skipifsilent

; Abrir el manual automáticamente después de instalar
Filename: "{app}\manual\now.html"; \
    Description: "Abrir manual de uso e instalación"; \
    Flags: shellexec postinstall skipifsilent
