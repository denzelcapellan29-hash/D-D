@echo off
setlocal
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0install_windows.ps1" %*
if errorlevel 1 (
  echo.
  echo Acq Foundry 3D MCP install failed.
  pause
)
exit /b %ERRORLEVEL%
