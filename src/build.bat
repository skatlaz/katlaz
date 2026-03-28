@echo off
SETLOCAL

cd /d %~dp0

SET MSYS2_PATH=C:\msys64

IF NOT EXIST "%MSYS2_PATH%\usr\bin\bash.exe" (
    echo MSYS2 not found!
    pause
    exit /b
)

echo Compiling...

"%MSYS2_PATH%\usr\bin\bash.exe" -lc "cd $(cygpath '%cd%') && g++ app/AppMain.cpp -o my_app.exe `pkg-config --cflags --libs gtk+-3.0 webkit2gtk-4.0`"

echo OK!
pause
