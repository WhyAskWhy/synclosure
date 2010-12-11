; $Id$
; $HeadURL$

#define MyAppName "Synclosure"

; FIXME: Generate this through build script.
#define MyAppVerName "Synclosure-devel-svn"

#define MyAppPublisher "WhyAskWhy.org"
#define MyAppURL "http://projects.whyaskwhy.org/"
#define MyAppSupportURL "http://projects.whyaskwhy.org/"
#define MyAppPublisherURL "http://www.whyaskwhy.org/"
#define MyAppCopyrightOwner "TBD"
#define MyAppCopyrightYear "TBD"

#define MyAppNameExe "synclosure.exe"

#define InstallerName "setup_synclosure"

#define InstallPath "{app}"

; Version info of the installer itself?
#define VersionInfoVersion "1.0"
#define VersionInfoProductVersion "1.0"

#define SetupIcon "whyaskwhy.org.ico"
#define ShortcutIcon "{app}\whyaskwhy.org.ico"

#define APPID_GUID  "{{0053D56D-782E-403A-BA77-FB8D01D0E925}"

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={#APPID_GUID}
AppName={#MyAppName}

#ifdef MY_BUILD_VERSION
    AppVerName={#MY_BUILD_VERSION}
#else   
    AppVerName={#MyAppVerName}
#endif

AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppPublisherURL}
AppSupportURL={#MyAppSupportURL}
AppUpdatesURL={#MyAppURL}

; Set to AppPublisher value by default
;VersionInfoCompany=
VersionInfoCopyright=(c) {#MyAppCopyrightYear} {#MyAppCopyrightOwner}
VersionInfoDescription={AppVerName}
VersionInfoProductName={#MyAppName}
VersionInfoProductVersion={#VersionInfoProductVersion}
VersionInfoVersion={#VersionInfoVersion}
VersionInfoTextVersion={#VersionInfoVersion}
DefaultDirName={pf}\{#MyAppPublisher}\{#MyAppName}
DirExistsWarning=yes
DisableProgramGroupPage=no
DefaultGroupName={#MyAppPublisher}\{#MyAppName}
OutputBaseFilename={#InstallerName}
UninstallDisplayIcon={#ShortcutIcon}
SetupIconFile={#SetupIcon}

; Compiling via commandline and passing option will disable compression,
; otherwise if the option is not defined, use max compression.
#ifdef TESTING
    Compression=none    
#else   
    Compression=lzma/ultra64
#endif

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



[Messages]
BeveledLabel={#MyAppVerName} - {#MyAppSupportURL}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Icons]
; {group}
;The path to the Start Menu folder, as selected by the user on Setup's Select Start Menu Folder wizard page.
;On Windows NT platforms, this folder is created under the All Users profile unless the user installing
;the application does not have administrative privileges, in which case it is created in the user's profile.

Name: "{group}\{#MyAppName}"; Filename: "{#InstallPath}\{#MyAppNameExe}"; IconFilename: "{#ShortcutIcon}"; WorkingDir: "{#InstallPath}";

Name: "{group}\Documents\Readme (txt)"; Filename: "{#InstallPath}\docs\readme.txt";
Name: "{group}\Documents\Web\Homepage"; Filename: "{#MyAppURL}";

Name: "{commondesktop}\{#MyAppName}";Filename: "{#InstallPath}\{#MyAppNameExe}";IconFilename: "{#ShortcutIcon}";WorkingDir: "{#InstallPath}";Tasks: desktopicon;


;[Dirs]
; Grant full permissions recursively to app directory
; Name: "{#InstallPath}"; Permissions: users-modify

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked


[Files]
; The 'package' dir will be created during the build phase.
Source: "package\*"; DestDir: "{#InstallPath}"; Excludes: "\.svn"; Flags: ignoreversion recursesubdirs createallsubdirs
; NOTE: Don't use "Flags: ignoreversion" on any shared system files