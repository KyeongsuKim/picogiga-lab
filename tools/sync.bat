@echo off
rem Double-click to refresh the publication list from Google Scholar.
cd /d "%~dp0.."
python tools\sync_publications.py
pause
