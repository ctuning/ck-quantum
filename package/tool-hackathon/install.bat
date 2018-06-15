@echo off

rem CK installation script
rem
rem Developer(s):
rem  * Grigori Fursin, dividiti/cTuning foundation
rem

######################################################################################
echo Installing CK-QUANTUM HACKATHON MODULE
echo.

mkdir %INSTALL_DIR%\lib

xcopy /s /e /y %PACKAGE_DIR%\hackathon-src\* %INSTALL_DIR%\lib

exit /b 0
