@ECHO OFF

:: Gets this script's running directory
set CORE_DIR=%~dp0\..

CALL :NORMALIZEPATH %CORE_DIR%
SET CORE_DIR=%RETVAL%

set SCRIPT_DIR=%CORE_DIR%/python/

:: set PYTHONPATH=%SCRIPT_DIR%;
:: set XBMLANGPATH=%CORE_DIR%icons/%B
:: set MAYA_SHELF_PATH=%CORE_DIR%shelves

set PYTHONPATH=%SCRIPT_DIR%
set MAYA_MODULE_PATH=%CORE_DIR%/third_party/mgear_4.2.2/release;
set MAYA_PLUG_IN_PATH=%CORE_DIR%/plugins
set XBMLANGPATH=%CORE_DIR%/icons
set MAYA_SHELF_PATH=%CORE_DIR%/shelves

set MGEAR_SHIFTER_COMPONENT_PATH=%CORE_DIR%/third_party/mGearScripts/Components


:: Actually open maya
set KEY_NAME="HKEY_LOCAL_MACHINE\SOFTWARE\Autodesk\Maya\2020\Setup\InstallPath"
set VALUE_NAME=MAYA_INSTALL_LOCATION

FOR /F "usebackq tokens=2*" %%A IN (`REG QUERY %KEY_NAME% /v %VALUE_NAME% 2^>nul`) DO (
    set ValueName=%%A
    set ValueType=%%B
    set ValueValue=%%C
)

set MAYA_DIR_PATH="%ValueType%"
cd "%MAYA_DIR_PATH%/bin"
start maya.exe

:: Close the terminal window after opening Maya
exit

:NORMALIZEPATH
  SET RETVAL=%~f1
  EXIT /B