@echo off
REM Wrapper script para ejecutar el CLI en Windows

cd /d %~dp0\backend
python cli.py %*
