# main.py
"""Entry point — chạy file này để khởi động Lyric Translator."""

from ui.app import LyricTranslatorApp

if __name__ == "__main__":
    app = LyricTranslatorApp()
    app.mainloop()
