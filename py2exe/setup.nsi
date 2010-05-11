# GetTube NSIS Script
!define VERSION "0.6.8"

# include modern UI2
!include MUI2.nsh

Outfile "GetTube-${VERSION}-setup.exe"
Name "GetTube"
InstallDir "$PROGRAMFILES\GetTube"
SetCompressor lzma
RequestExecutionLevel admin

# MUI2 settings
!define MUI_ICON "gettube_64x64.ico"
!define MUI_ABORTWARNING

# Installer pages
Var SMFolder

!insertmacro MUI_PAGE_WELCOME
!insertmacro MUI_PAGE_LICENSE "COPYING.txt"
!insertmacro MUI_PAGE_DIRECTORY
!define MUI_STARTMENUPAGE_REGISTRY_ROOT "HKCU"
!define MUI_STARTMENUPAGE_REGISTRY_KEY "gettube"
!define MUI_STARTMENUPAGE_REGISTRY_VALUENAME "Start Menu Folder"
!insertmacro MUI_PAGE_STARTMENU Application $SMFolder
!insertmacro MUI_PAGE_INSTFILES
!define MUI_FINISHPAGE_RUN "$INSTDIR\GetTube.exe"
!insertmacro MUI_PAGE_FINISH

# Uninstaller pages
!insertmacro MUI_UNPAGE_CONFIRM
!insertmacro MUI_UNPAGE_INSTFILES
!insertmacro MUI_UNPAGE_FINISH

# set Languages
!insertmacro MUI_LANGUAGE "English"

# install section
Section
# Workaround for shortcut deletion bug on Vista/7
# See http://nsis.sourceforge.net/Shortcuts_removal_fails_on_Windows_Vista
# for more information
SetShellVarContext all
setOutPath $INSTDIR
File /r 'dist\*'

# Create uninstaller
WriteUninstaller $INSTDIR\uninstall.exe

# Create shortcuts
CreateSHortCut "$DESKTOP\GetTube.lnk" \
	"$INSTDIR\GetTube.exe"
!insertmacro MUI_STARTMENU_WRITE_BEGIN Application
	CreateDirectory "$SMPROGRAMS\$SMFolder"
	CreateSHortCut "$SMPROGRAMS\$SMFolder\GetTube.lnk" \
		"$INSTDIR\GetTube.exe"
	CreateShortCut "$SMPROGRAMS\$SMFolder\Uninstall.lnk" \
		"$INSTDIR\Uninstall.exe"
!insertmacro MUI_STARTMENU_WRITE_END

# Write Registry
WriteRegStr HKLM \
	"Software\Microsoft\Windows\CurrentVersion\Uninstall\GetTube" \
	"DisplayIcon" "$INSTDIR\GetTube.exe"
WriteRegStr HKLM \
	"Software\Microsoft\Windows\CurrentVersion\Uninstall\GetTube" \
	"DisplayName" "GetTube"
WriteRegStr HKLM \
	"Software\Microsoft\Windows\CurrentVersion\Uninstall\GetTube" \
	"DisplayVersion" "${VERSION}"
WriteRegStr HKLM \
	"Software\Microsoft\Windows\CurrentVersion\Uninstall\GetTube" \
	"Publisher" "AZ (Wei-Ning Huang)"
WriteRegStr HKLM \
	"Software\Microsoft\Windows\CurrentVersion\Uninstall\GetTube" \
	"UninstallString" "$\"$INSTDIR\uninstall.exe$\""
WriteRegStr HKLM \
	"Software\Microsoft\Windows\CurrentVersion\Uninstall\GetTube" \
	"URLInfoAbout" "http://github.com/Aitjcize/GetTube"
SectionEnd

# uninstall section
Section "uninstall"
# Workaround for shortcut deletion bug on Vista/7
# See http://nsis.sourceforge.net/Shortcuts_removal_fails_on_Windows_Vista
# for more information
SetShellVarContext all

rmdir /r $INSTDIR
Delete "$DESKTOP\GetTube.lnk"
!insertmacro MUI_STARTMENU_GETFOLDER Application $SMFolder
rmdir /r "$SMPROGRAMS\$SMFolder"
DeleteRegKey HKLM \
"Software\Microsoft\Windows\CurrentVersion\Uninstall\GetTube"

DeleteRegKey /ifempty HKCU "GetTube"
sectionEnd
