@echo off
rem Weekly SEO run for Task Scheduler. Output is appended to seo\logs\weekly.log.
cd /d "%~dp0.."
if not exist seo\logs mkdir seo\logs
set PYTHONIOENCODING=utf-8
echo ===== %date% %time% >> seo\logs\weekly.log
"seo\.venv\Scripts\python.exe" seo\weekly.py >> seo\logs\weekly.log 2>&1
echo exit code %errorlevel% >> seo\logs\weekly.log
