; $Id$
; $HeadURL$

#define MyAppName "Synclosure"

; NOTE:
; ===================================================
; VERSION_PLACEHOLDER is replaced by the build script.
; ===================================================

#define MyAppVerName "Synclosure VERSION_PLACEHOLDER"
#define MyAppPublisher "WhyAskWhy.org"
#define MyAppSupportURL "http://projects.whyaskwhy.org/"
#define MyAppPublisherURL "http://www.whyaskwhy.org/"
#define MyAppCopyrightOwner "WhyAskWhy.org"
#define MyAppCopyrightYear "2007"

#define MyAppURL "http://projects.whyaskwhy.org/"
#define MyAppWikiURL "http://projects.whyaskwhy.org/projects/synclosure/wiki/"

#define MyAppNameExe "synclosure.exe"

; DEFINED VIA BUILD SCRIPT
;#define InstallerName "setup_synclosure"

#define InstallPath "{app}"

; Version info of the installer itself
; DEFINED VIA BUILD SCRIPT
;#define VersionInfoVersion "1.0"

; Version of the product being installed
#define VersionInfoProductTextVersion "VERSION_PLACEHOLDER"

#define SetupIcon "synclosure.ico"
#define ShortcutIcon "{app}\synclosure.ico"

#define APPID_GUID  "{{0053D56D-782E-403A-BA77-FB8D01D0E925}"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={#APPID_GUID}
AppName={#MyAppName}
AppVerName={#MyAppVerName}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppPublisherURL}
AppSupportURL={#MyAppSupportURL}
AppUpdatesURL={#MyAppURL}

; Set to AppPublisher value by default
;VersionInfoCompany=
AppCopyright=Original code and name (C) by raphael balimann, 2004. Modifications (C) {#MyAppCopyrightYear} {#MyAppCopyrightOwner}
; Set to AppCopyright value by default
;VersionInfoCopyright=
VersionInfoDescription={#MyAppVerName} installer
VersionInfoProductName={#MyAppName}
VersionInfoProductTextVersion={#VersionInfoProductTextVersion}
VersionInfoVersion={#VersionInfoVersion}
VersionInfoTextVersion={#VersionInfoVersion}
DefaultDirName={pf}\{#MyAppPublisher}\{#MyAppName}
DirExistsWarning=yes
DisableProgramGroupPage=no
DefaultGroupName={#MyAppPublisher}\{#MyAppName}
OutputBaseFilename={#InstallerName}
UninstallDisplayIcon={#ShortcutIcon}
SetupIconFile={#SetupIcon}

Compression=lzma/ultra64

CompressionThreads=2
SolidCompression=no

Uninstallable=yes

; User can install to a local directory and run Synclosure without problems.
PrivilegesRequired=none

; 164x314
WizardImageFile=large.bmp
WizardImageStretch=no
WizardImageBackColor=clBlack

; 55x55
WizardSmallImageFile=small.bmp

; This information shows up as a page in the installer before a dir is chosen.
InfoBeforeFile=infobefore.rtf

; This information shows up as a page in the installer after install is done.
; InfoAfterFile=infoafter.rtf

LicenseFile=..\package\licenses\synclosure\LICENSE.txt


[Messages]
BeveledLabel={#MyAppVerName} - {#MyAppSupportURL}

[CustomMessages]
removemsg=Do you wish to keep sources.ini?

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Icons]
; {group}
;The path to the Start Menu folder, as selected by the user on Setup's Select Start Menu Folder wizard page.
;On Windows NT platforms, this folder is created under the All Users profile unless the user installing
;the application does not have administrative privileges, in which case it is created in the user's profile.

Name: "{group}\{#MyAppName}"; Filename: "{#InstallPath}"; IconFilename: "{#ShortcutIcon}"; WorkingDir: "{#InstallPath}";

Name: "{group}\Documents\Readme (txt)"; Filename: "{#InstallPath}\docs\readme.txt";
Name: "{group}\Documents\Web\Homepage"; Filename: "{#MyAppURL}";
Name: "{group}\Documents\Web\Documentation"; Filename: "{#MyAppWikiURL}";

Name: "{commondesktop}\{#MyAppName}";Filename: "{#InstallPath}";IconFilename: "{#ShortcutIcon}";WorkingDir: "{#InstallPath}";Tasks: desktopicon;


;[Dirs]
; Grant full permissions recursively to app directory
; Name: "{#InstallPath}"; Permissions: users-modify

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked


[Files]
; The 'package' dir will be created during the build phase.
Source: "..\package\*"; DestDir: "{#InstallPath}"; Excludes: "\.svn"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\package\sources.ini"; DestDir: "{#InstallPath}"; Flags: uninsneveruninstall
; NOTE: Don't use "Flags: ignoreversion" on any shared system files


[Code]
procedure CurUninstallStepChanged(CurUninstallStep: TUninstallStep);
begin
 { Ask user if they wish to keep sources.ini. If they say yes, then remove it. }
 { If they say no, then Inno Setup keeps it per the 'uninsneveruninstall' flag.}
  if CurUninstallStep = usUninstall then 
  begin
   if MsgBox(ExpandConstant('{cm:removemsg}'), mbConfirmation, MB_YESNO)=IDYES then
     begin
      DeleteFile(ExpandConstant('{#InstallPath}'+'\sources.ini'), True, True, True);
     end;
 end;
end;
