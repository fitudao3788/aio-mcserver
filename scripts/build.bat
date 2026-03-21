@echo off

python -m nuitka --standalone --onefile --include-windows-runtime-dlls=yes --output-dir=%~dp0..\dist %~dp0..\main.py
