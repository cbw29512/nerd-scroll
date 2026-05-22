#define MyAppName "Nerd Scroll"
#define MyAppVersion "0.9.0"
#define MyAppPublisher "Nerd Scroll"
#define MyAppExeName "NerdScroll.exe"

[Setup]
AppId={{B1F6D3F7-6C94-4F36-9A30-8E50B853D431}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\Nerd Scroll
DefaultGroupName=Nerd Scroll
AllowNoIcons=yes
OutputDir=..\release
OutputBaseFilename=NerdScrollSetup-v{#MyAppVersion}
Compression=lzma
SolidCompression=yes
WizardStyle=modern

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional icons:"; Flags: unchecked

[Files]
Source: "..\dist\NerdScrollApp\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{group}\Nerd Scroll"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\Uninstall Nerd Scroll"; Filename: "{uninstallexe}"
Name: "{autodesktop}\Nerd Scroll"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch Nerd Scroll"; Flags: nowait postinstall skipifsilent
