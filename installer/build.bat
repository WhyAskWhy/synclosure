:: $Id$
:: $HeadURL$

@echo off

set APPLICATION_NAME=Synclosure
set SYNCLOSURE_REPO=http://projects.whyaskwhy.org/svn/synclosure/trunk/
set APP_ISS_FILE=setup.iss

set BUILD_DIR=%CD%
set OUTPUT_DIR=%CD%

set CLEANUP=NO
set TESTING=NO

:: If the export dir doesn't already exist, export it
if not exist "%BUILD_DIR%\%APPLICATION_NAME%" GOTO CHECKOUT

:: Otherwise, exit if it exists
echo Already exists: "%BUILD_DIR%\%APPLICATION_NAME%"
echo Skipping checkout and attempting to build ...
GOTO BUILD



:CHECKOUT
echo Checking out "%APPLICATION_NAME%" ...
svn export --quiet "%SYNCLOSURE_REPO%" "%BUILD_DIR%\%APPLICATION_NAME%"

:BUILD
if "%TESTING%"=="YES" goto TESTBUILD

:: Otherwise, assume a full build is desired
echo RELEASE BUILD
echo %date% %time% - Compiling %APPLICATION_NAME% && iscc /Q /O"%OUTPUT_DIR%" "%BUILD_DIR%\%APPLICATION_NAME%\%APP_ISS_FILE%"
if "%CLEANUP%"=="YES" GOTO CLEANUP
GOTO EXIT

:TESTBUILD
echo TESTBUILD
echo %date% %time% - Compiling %APPLICATION_NAME% && iscc /Q /O"%OUTPUT_DIR%" /d"TESTING=Yes" "%BUILD_DIR%\%APPLICATION_NAME%\%APP_ISS_FILE%"
if "%CLEANUP%"=="YES" GOTO CLEANUP
GOTO EXIT

:CLEANUP
:: Before actually removing the checked out files, make sure inno setup completed successfully
if ERRORLEVEL 0 GOTO RMFILES
GOTO EXIT

:RMFILES
if "%CLEANUP%"=="YES" rmdir /s /q "%BUILD_DIR%\%APPLICATION_NAME%"

:EXIT
