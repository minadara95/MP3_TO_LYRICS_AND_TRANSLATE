@echo off
echo ============================================================
echo   Lyric Translator — Build thư mục (khởi động nhanh hơn)
echo ============================================================
echo.

if not exist .venv\Scripts\activate.bat (
    echo LỖI: Chưa cài đặt. Chạy install.bat trước.
    pause
    exit /b 1
)
call .venv\Scripts\activate.bat

pip show pyinstaller >nul 2>&1
if errorlevel 1 ( pip install pyinstaller )

echo [1/2] Đang build...
echo.

pyinstaller ^
  --onedir ^
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

if errorlevel 1 ( echo LỖI: Build thất bại. & pause & exit /b 1 )

echo.
echo ============================================================
echo   [2/2] BUILD THÀNH CÔNG!
echo.
echo   Thư mục: dist\LyricTranslator\
echo   Chạy:    dist\LyricTranslator\LyricTranslator.exe
echo.
echo   Để chia sẻ: zip toàn bộ thư mục dist\LyricTranslator\
echo ============================================================
echo.
pause
