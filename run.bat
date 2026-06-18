@echo off
:: Kích hoạt virtual environment và chạy app
if exist .venv\Scripts\activate.bat (
    call .venv\Scripts\activate.bat
    python main.py
) else (
    echo Chưa cài đặt! Hãy chạy install.bat trước.
    pause
)
