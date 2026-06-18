@echo off
echo ============================================================
echo   Lyric Translator — Cài đặt thư viện
echo ============================================================
echo.

:: Tạo virtual environment
echo [1/3] Tạo môi trường ảo Python...
python -m venv .venv
if errorlevel 1 (
    echo LỖI: Không tìm thấy Python. Vui lòng cài Python 3.10+ từ python.org
    pause
    exit /b 1
)

:: Kích hoạt venv
call .venv\Scripts\activate.bat

:: Cài dependencies
echo.
echo [2/3] Cài đặt thư viện (có thể mất 3-5 phút lần đầu)...
pip install -r requirements.txt
if errorlevel 1 (
    echo LỖI: Cài đặt thất bại.
    pause
    exit /b 1
)

echo.
echo [3/3] Hoàn tất!
echo.
echo ============================================================
echo   Chạy app: double-click run.bat
echo   Hoặc: .venv\Scripts\python.exe main.py
echo ============================================================
echo.
pause
