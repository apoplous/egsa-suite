@echo off
setlocal EnableExtensions
cd /d "%~dp0"

set "VERSION=5.6.0"
set "RELEASE_NAME=EGSA_Suite_v%VERSION%_Windows_x64"

title EGSA Suite %VERSION% - Build EXE

echo ==================================================
echo        EGSA Suite %VERSION% - Build EXE
echo ==================================================
echo.

where py >nul 2>nul
if not errorlevel 1 (
    set "PY=py"
) else (
    where python >nul 2>nul
    if errorlevel 1 (
        echo [ERROR] Python was not found.
        pause
        exit /b 1
    )
    set "PY=python"
)

%PY% --version
if errorlevel 1 goto :error

for %%F in (geotoolsgr.py hatt_coefficients.py EGSA_Suite.spec version_info.txt requirements-build.txt LICENSE THIRD_PARTY_NOTICES.md DATA_SOURCES.md) do (
    if not exist "%%F" (
        echo [ERROR] Missing required file: %%F
        goto :error
    )
)
if not exist "assets\crosshair.png" (
    echo [ERROR] Missing assets\crosshair.png
    goto :error
)
if not exist "assets\egsa_suite.ico" (
    echo [ERROR] Missing assets\egsa_suite.ico
    goto :error
)

echo [1/6] Installing build dependencies...
%PY% -m pip install -r requirements-build.txt
if errorlevel 1 goto :error

echo [2/6] Cleaning previous output...
if exist "build" rmdir /s /q "build"
if exist "dist" rmdir /s /q "dist"
if exist "release\%RELEASE_NAME%" rmdir /s /q "release\%RELEASE_NAME%"
if exist "release\%RELEASE_NAME%.zip" del /q "release\%RELEASE_NAME%.zip"
if not exist "release" mkdir "release"

echo [3/6] Building executable...
%PY% -m PyInstaller --noconfirm --clean "EGSA_Suite.spec"
if errorlevel 1 goto :error
if not exist "dist\EGSA_Suite.exe" (
    echo [ERROR] dist\EGSA_Suite.exe was not created.
    goto :error
)

echo [4/6] Staging release package...
mkdir "release\%RELEASE_NAME%"
copy /y "dist\EGSA_Suite.exe" "release\%RELEASE_NAME%\EGSA_Suite.exe" >nul
copy /y "LICENSE" "release\%RELEASE_NAME%\LICENSE.txt" >nul
copy /y "THIRD_PARTY_NOTICES.md" "release\%RELEASE_NAME%\THIRD_PARTY_NOTICES.md" >nul
copy /y "DATA_SOURCES.md" "release\%RELEASE_NAME%\DATA_SOURCES.md" >nul
xcopy /e /i /y "licenses" "release\%RELEASE_NAME%\licenses" >nul

echo [5/6] Creating release ZIP...
powershell -NoProfile -ExecutionPolicy Bypass -Command "Compress-Archive -Path 'release\%RELEASE_NAME%\*' -DestinationPath 'release\%RELEASE_NAME%.zip' -Force"
if errorlevel 1 goto :error

echo [6/6] Writing SHA-256 checksums...
powershell -NoProfile -ExecutionPolicy Bypass -Command "$files=@('dist\EGSA_Suite.exe','release\%RELEASE_NAME%.zip'); $lines=@(); foreach($f in $files){ $h=Get-FileHash $f -Algorithm SHA256; $lines += ($h.Hash.ToLower() + '  ' + (Split-Path $f -Leaf)) }; Set-Content -Path 'release\SHA256SUMS.txt' -Value $lines -Encoding ascii"
if errorlevel 1 goto :error

echo.
echo ==================================================
echo Build completed successfully.
echo EXE: %CD%\dist\EGSA_Suite.exe
echo ZIP: %CD%\release\%RELEASE_NAME%.zip
echo SHA256: %CD%\release\SHA256SUMS.txt
echo ==================================================
echo.
pause
exit /b 0

:error
echo.
echo ==================================================
echo Build failed. Review the messages above.
echo ==================================================
pause
exit /b 1
