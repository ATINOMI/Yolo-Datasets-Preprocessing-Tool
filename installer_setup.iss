; YOLO Dataset Preprocessing Tool - Inno Setup 安装脚本
; 版本: 1.0.0

#define MyAppName "YOLO数据集预处理工具"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "YOLO Dataset Tools"
#define MyAppExeName "YOLO数据集预处理工具.exe"

[Setup]
; 应用程序基本信息
AppId={{A5B8C9D0-E1F2-3456-7890-ABCDEF123456}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
OutputDir=installer
OutputBaseFilename=YOLO数据集预处理工具_v{#MyAppVersion}_Setup
SetupIconFile=
Compression=lzma
SolidCompression=yes
WizardStyle=modern

; 权限要求
PrivilegesRequired=lowest
PrivilegesRequiredOverridesAllowed=dialog

; 目录和许可证
LicenseFile=
InfoBeforeFile=
InfoAfterFile=
DisableProgramGroupPage=yes
DisableWelcomePage=no

; 语言
ShowLanguageDialog=auto

; 卸载支持
UninstallDisplayIcon={app}\{#MyAppExeName}
UninstallDisplayName={#MyAppName}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode

[Files]
; 打包后的所有文件
Source: "dist\YOLO数据集预处理工具\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
; 开始菜单快捷方式
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"

; 桌面快捷方式
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

; 快速启动快捷方式（Windows 7 及以下）
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: quicklaunchicon

[Run]
; 安装完成后运行程序（可选）
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Code]
// 检查是否已安装旧版本
function InitializeSetup(): Boolean;
var
  OldVersion: String;
begin
  Result := True;
  if RegQueryStringValue(HKLM, 'Software\Microsoft\Windows\CurrentVersion\Uninstall\{#SetupSetting("AppId")}_is1', 'DisplayVersion', OldVersion) then
  begin
    if MsgBox('检测到已安装版本 ' + OldVersion + '。是否继续安装新版本？', mbConfirmation, MB_YESNO) = IDNO then
      Result := False;
  end;
end;
