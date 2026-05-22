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
AllowNoIcons=no
OutputDir=..\release
OutputBaseFilename=NerdScrollSetup-v{#MyAppVersion}
Compression=lzma
SolidCompression=yes
WizardStyle=modern
DisableProgramGroupPage=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "Create a Nerd Scroll desktop shortcut"; GroupDescription: "Shortcuts:"; Flags: checkedonce
Name: "desktopfiles"; Description: "Create easy folders on the Desktop for homemade and purchased scrollers"; GroupDescription: "Nerd Scroll folders:"; Flags: checkedonce

[Files]
Source: "..\dist\NerdScrollApp\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\installer\desktop-workspace\README_FIRST.txt"; DestDir: "{autodesktop}\Nerd Scroll Files"; Flags: ignoreversion; Tasks: desktopfiles
Source: "..\installer\desktop-workspace\Homemade Scrollers\README_PUT_HOMEMADE_SCROLLERS_HERE.txt"; DestDir: "{autodesktop}\Nerd Scroll Files\Homemade Scrollers"; Flags: ignoreversion; Tasks: desktopfiles
Source: "..\installer\desktop-workspace\Purchased Scrollers\README_PUT_PURCHASED_SCROLLERS_HERE.txt"; DestDir: "{autodesktop}\Nerd Scroll Files\Purchased Scrollers"; Flags: ignoreversion; Tasks: desktopfiles

[Dirs]
Name: "{autodesktop}\Nerd Scroll Files"; Tasks: desktopfiles
Name: "{autodesktop}\Nerd Scroll Files\Homemade Scrollers"; Tasks: desktopfiles
Name: "{autodesktop}\Nerd Scroll Files\Purchased Scrollers"; Tasks: desktopfiles

[Icons]
Name: "{group}\Nerd Scroll"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\Nerd Scroll Files"; Filename: "{autodesktop}\Nerd Scroll Files"; Tasks: desktopfiles
Name: "{group}\Uninstall Nerd Scroll"; Filename: "{uninstallexe}"
Name: "{autodesktop}\Nerd Scroll"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
Name: "{autodesktop}\Nerd Scroll Files"; Filename: "{autodesktop}\Nerd Scroll Files"; Tasks: desktopfiles

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "Launch Nerd Scroll"; Flags: nowait postinstall skipifsilent
