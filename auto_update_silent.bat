@echo off
chcp 65001 >nul
set PYTHONIOENCODING=utf-8
set GITHUB_TOKEN=
cd /d "%~dp0"

echo ============================================ >> auto_update.log
echo [%DATE% %TIME%] Bat dau cap nhat tu dong >> auto_update.log

python update_store_data.py >> auto_update.log 2>&1
python update_excel_data.py >> auto_update.log 2>&1

git add index.html tele.html tasks.html >> auto_update.log 2>&1
for /f "tokens=*" %%i in ('python -c "from datetime import datetime; print(datetime.now().strftime('%%d/%%m/%%Y %%H:%%M'))"') do set TIMESTAMP=%%i
git commit -m "Auto update %TIMESTAMP%" >> auto_update.log 2>&1

git push origin master >> auto_update.log 2>&1

echo [%DATE% %TIME%] Hoan tat >> auto_update.log
echo ============================================ >> auto_update.log
