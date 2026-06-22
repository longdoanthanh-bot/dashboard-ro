@echo off
chcp 65001 >nul
echo Dang cap nhat du lieu tu G: Drive vao index.html...
python update_store_data.py
if %ERRORLEVEL% EQU 0 (
    echo.
    echo CAP NHAT THANH CONG!
) else (
    echo.
    echo CO LOI XAY RA! Kiem tra lai xem da cai dat Python chua.
)
pause
