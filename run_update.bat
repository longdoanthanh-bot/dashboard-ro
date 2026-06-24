@echo off
chcp 65001 >nul
set PYTHONIOENCODING=utf-8
cd /d "%~dp0"

echo ============================================
echo   DASHBOARD RO - AUTO UPDATE PIPELINE
echo ============================================
echo.

:: === BUOC 1: Cap nhat du lieu JSON vao index.html ===
echo [1/3] Dang cap nhat du lieu tu G: Drive vao index.html...
python update_store_data.py
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [LOI] Buoc 1 that bai! Dung lai.
    pause
    exit /b 1
)
echo [OK] Buoc 1 hoan tat.
echo.

:: === BUOC 2: Git commit ===
echo [2/3] Dang commit thay doi len Git...
for /f "tokens=*" %%i in ('python -c "from datetime import datetime; print(datetime.now().strftime('%%d/%%m/%%Y %%H:%%M'))"') do set TIMESTAMP=%%i

git add index.html
if %ERRORLEVEL% NEQ 0 (
    echo [LOI] git add that bai!
    pause
    exit /b 1
)

git commit -m "Auto update %TIMESTAMP%"
if %ERRORLEVEL% NEQ 0 (
    echo [CANH BAO] Khong co thay doi moi de commit.
    echo Pipeline dung tai day - du lieu da cap nhat roi.
    pause
    exit /b 0
)
echo [OK] Buoc 2 hoan tat.
echo.

:: === BUOC 3: Git push (KI-37: push ca master va main) ===
echo [3/3] Dang push len GitHub Pages...
git push origin master
if %ERRORLEVEL% NEQ 0 (
    echo [LOI] git push origin master that bai!
    pause
    exit /b 1
)

git push origin master:main
if %ERRORLEVEL% NEQ 0 (
    echo [CANH BAO] git push master:main that bai, nhung master da push OK.
)

echo.
echo ============================================
echo   HOAN TAT! Dashboard se cap nhat trong 1-2 phut.
echo   https://longdoanthanh-bot.github.io/dashboard-ro/
echo ============================================
pause
