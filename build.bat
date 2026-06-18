@echo off
echo ============================================================
echo   Lyric Translator — Build file .EXE
echo ============================================================
echo.

:: Kích hoạt venv (phải đã chạy install.bat trước)
if not exist .venv\Scripts\activate.bat (
    echo LỖI: Chưa cài đặt. Chạy install.bat trước.
    pause
    exit /b 1
)
call .venv\Scripts\activate.bat

:: Cài PyInstaller nếu chưa có
pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo Đang cài PyInstaller...
    pip install pyinstaller
)

echo.
echo [1/2] Đang build... (có thể mất 2-5 phút)
echo.

pyinstaller ^
  --onefile ^
  --windowed ^
  --name "LyricTranslator" ^
  --collect-data customtkinter ^
  --collect-all faster_whisper ^
  --collect-all ctranslate2 ^
  --collect-all tokenizers ^
  --hidden-import pypinyin ^
  --hidden-import pypinyin.phrases_dict_large ^
  --hidden-import pykakasi ^
  --hidden-import hangul_romanize ^
  --hidden-import hangul_romanize.rule ^
  --hidden-import deep_translator ^
  --hidden-import google.generativeai ^
  --hidden-import huggingface_hub ^
  main.py

if errorlevel 1 (
    echo.
    echo LỖI: Build thất bại. Xem log ở trên.
    pause
    exit /b 1
)

echo.
echo ============================================================
echo   [2/2] BUILD THÀNH CÔNG!
echo.
echo   File exe: dist\LyricTranslator.exe
echo.
echo   Lưu ý: Lần đầu chạy exe sẽ tải Whisper model (~1.5 GB).
echo          Từ lần 2 trở đi chạy offline hoàn toàn.
echo ============================================================
echo.
pause
