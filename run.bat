@echo off
@cls

setlocal

set SOX_DIR=%~dp0\sox-14.4.2

if NOT exist "%SOX_DIR%" (
	echo Please download SoX binaries and place them in %SOX_DIR%
	goto EOF
)

set PATH=%PATH%;%SOX_DIR%

cd ./server
call ./.venv/Scripts/activate.bat
python src/main.py

:EOF
pause