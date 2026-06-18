============================================================
  LYRIC TRANSLATOR
  Dịch lời bài hát & xuất phụ đề CapCut
  Designed by: Minh Anh Du | anhminh.cowork@gmail.com
============================================================


════════════════════════════════════════════════════════════
  FLOW ARCHITECTURE
════════════════════════════════════════════════════════════

  ┌─────────┐     ┌──────────────┐
  │  User   │────▶│  Audio File  │
  └─────────┘     │ MP3/WAV/M4A  │
                  └──────┬───────┘
                         │
                         ▼
          ╔══════════════════════════════════════╗
          ║           core/  (Backend)           ║
          ║                                      ║
          ║  ┌────────────────────────────────┐  ║
          ║  │  ① transcriber.py              │  ║
          ║  │     faster-whisper (CPU)        │  ║
          ║  │     Speech-to-Text + Timestamp  │  ║
          ║  │     🔍 Auto Detect Language     │  ║
          ║  │     ZH · JA · KO · EN · ...    │  ║
          ║  └───────────────┬────────────────┘  ║
          ║                  │  segments[]        ║
          ║        ┌─────────┴──────────┐         ║
          ║        │                    │         ║
          ║        ▼                    ▼         ║
          ║  ┌──────────────┐  ┌──────────────┐  ║
          ║  │ ② phonetic   │  │ ③ translator │  ║
          ║  │   .py        │  │   .py        │  ║
          ║  │              │  │              │  ║
          ║  │ ZH→ Pinyin   │  │ Google Trans │  ║
          ║  │ JA→ Romaji   │  │   (free)     │  ║
          ║  │ KO→ Romaja   │  │   hoặc       │  ║
          ║  │ EN→ (skip)   │  │ Gemini API   │  ║
          ║  └──────┬───────┘  └──────┬───────┘  ║
          ║         └────────┬─────────┘         ║
          ╚══════════════════╪══════════════════╝
                             │ segments[]
                             │ { start, end,
                             │   text, phonetic,
                             │   translation }
                             ▼
          ╔══════════════════════════════════════╗
          ║           ui/app.py  (Frontend)      ║
          ║                                      ║
          ║  ┌───────────────┐  ┌─────────────┐  ║
          ║  │  Left Panel   │  │ Right Panel │  ║
          ║  │               │  │             │  ║
          ║  │ • Chọn file   │  │ Bảng kết    │  ║
          ║  │ • Chọn model  │  │ quả (có thể │  ║
          ║  │ • Backend dịch│  │ sửa tay)    │  ║
          ║  │ • API Key     │  │             │  ║
          ║  │ • Progress    │  │ 🔴 Highlight│  ║
          ║  │ • ▶ Xử lý    │  │    câu lỗi  │  ║
          ║  └───────────────┘  └──────┬──────┘  ║
          ╚═════════════════════════════╪════════╝
                                        │
                              ┌─────────┴──────────┐
                              │     exporter.py     │
                              └────────┬────────────┘
                     ┌─────────────────┼──────────────────┐
                     ▼                 ▼                  ▼
            ┌─────────────┐  ┌──────────────┐  ┌──────────────────┐
            │  📄 .TXT    │  │ 🎬 _goc.srt  │  │ 🎬 _phienam.srt  │
            │  (tổng hợp) │  │  Lời gốc     │  │ 🎬 _viet.srt     │
            └─────────────┘  └──────────────┘  └──────────────────┘
                                     │                   │
                                     └─────────┬─────────┘
                                               ▼
                                   ┌───────────────────────┐
                                   │  🎬  CapCut           │
                                   │  Import Subtitle      │
                                   │  → Phụ đề video       │
                                   └───────────────────────┘


════════════════════════════════════════════════════════════
  TECH STACK
════════════════════════════════════════════════════════════

  Layer           Technology
  ─────────────── ──────────────────────────────────────────
  UI              Python + CustomTkinter (dark mode)
  Speech-to-Text  faster-whisper  (Whisper medium, CPU)
  Phonetics       pypinyin / pykakasi / hangul-romanize
  Translation     Google Translate (requests) / Gemini API
  Packaging       PyInstaller (single .exe)


════════════════════════════════════════════════════════════
  PROJECT STRUCTURE
════════════════════════════════════════════════════════════

  lyric-translator/
  ├── main.py              Entry point
  ├── requirements.txt     Danh sách thư viện
  ├── install.bat          Cài đặt lần đầu (tạo venv)
  ├── run.bat              Chạy app hàng ngày
  ├── build.bat            Đóng gói thành 1 file .exe
  ├── build_dir.bat        Đóng gói thành thư mục .exe
  ├── USAGE.txt            Hướng dẫn dùng (source code)
  ├── USAGE_EXE.txt        Hướng dẫn dùng (file .exe)
  ├── core/
  │   ├── transcriber.py   faster-whisper STT
  │   ├── phonetic.py      Pinyin / Romaji / Romaja
  │   ├── translator.py    Google Translate / Gemini API
  │   └── exporter.py      Xuất TXT và SRT
  └── ui/
      └── app.py           Toàn bộ giao diện CustomTkinter


════════════════════════════════════════════════════════════
  QUICK START
════════════════════════════════════════════════════════════

  Lần đầu:    install.bat  →  run.bat
  Hàng ngày:  run.bat
  Đóng gói:   build.bat    →  dist\LyricTranslator.exe

  Xem chi tiết: USAGE.txt / USAGE_EXE.txt

============================================================
  GitHub: github.com/minadara95/MP3_TO_LYRICS_AND_TRANSLATE
  Minh Anh Du | anhminh.cowork@gmail.com | 0982.131.095
============================================================
