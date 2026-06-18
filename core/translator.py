# core/translator.py
"""
Dịch lời bài hát sang tiếng Việt.

Hỗ trợ 2 backend:
  - "google"  : Google Translate qua HTTP trực tiếp (miễn phí, không cần key)
  - "gemini"  : Google Gemini API (cần API key, dịch tự nhiên hơn)
"""

import re
import time
import urllib.parse
import requests
from typing import Callable

GEMINI_BATCH_SIZE = 40

# Map mã ngôn ngữ Whisper → Google Translate
LANG_MAP = {
    'zh': 'zh-CN',
    'ja': 'ja',
    'ko': 'ko',
    'en': 'en',
    'vi': 'vi',
    'fr': 'fr',
    'es': 'es',
    'de': 'de',
    'th': 'th',
}


# ─────────────────────────────────────────────────────────────────────
# Hàm chính
# ─────────────────────────────────────────────────────────────────────

def translate_lyrics(
    segments: list[dict],
    backend: str = "google",
    api_key: str = "",
    source_lang: str = "auto",
    progress_callback: Callable | None = None,
) -> list[dict]:
    if backend == "gemini":
        return _translate_gemini(segments, api_key, progress_callback)
    else:
        return _translate_google(segments, source_lang, progress_callback)


# ─────────────────────────────────────────────────────────────────────
# Backend 1: Google Translate — gọi trực tiếp, không cần key
# ─────────────────────────────────────────────────────────────────────

def _translate_google(
    segments: list[dict],
    source_lang: str = "auto",
    progress_callback: Callable | None = None,
) -> list[dict]:
    # Chuyển mã ngôn ngữ Whisper sang mã Google Translate
    src = LANG_MAP.get(source_lang, 'auto')
    total = len(segments)

    for i, seg in enumerate(segments):
        if progress_callback:
            pct = 0.65 + (i / total) * 0.27
            progress_callback(pct, f"Đang dịch... ({i + 1}/{total})")

        seg['translation'] = _google_translate_one(seg['text'], src)

        # Delay nhỏ giữa các câu tránh bị block
        time.sleep(0.3)

    if progress_callback:
        progress_callback(0.92, f"Dịch xong {total} câu!")

    return segments


def _google_translate_one(text: str, src: str = 'auto', retries: int = 3) -> str:
    """
    Gọi trực tiếp endpoint Google Translate (không cần API key).
    Tự retry nếu gặp lỗi tạm thời (500, timeout...).
    """
    url = "https://translate.googleapis.com/translate_a/single"
    params = {
        'client': 'gtx',
        'sl': src,
        'tl': 'vi',
        'dt': 't',
        'q': text,
    }

    for attempt in range(retries):
        try:
            resp = requests.get(url, params=params, timeout=10)

            if resp.status_code == 200:
                data = resp.json()
                # Kết quả nằm ở data[0] — list các đoạn dịch
                translated = ''.join(
                    part[0] for part in data[0] if part and part[0]
                )
                # Kiểm tra không trả về text gốc (dấu hiệu dịch thất bại)
                if translated and translated.strip() != text.strip():
                    return translated.strip()
                return translated.strip()

            elif resp.status_code == 429:
                # Rate limit — chờ lâu hơn rồi thử lại
                time.sleep(2 * (attempt + 1))

            else:
                # Lỗi khác (500...) — chờ rồi thử lại
                time.sleep(1 * (attempt + 1))

        except requests.exceptions.Timeout:
            time.sleep(1 * (attempt + 1))
        except Exception:
            time.sleep(1 * (attempt + 1))

    # Hết retry — trả về rỗng thay vì text gốc
    return ""


# ─────────────────────────────────────────────────────────────────────
# Backend 2: Gemini API
# ─────────────────────────────────────────────────────────────────────

def _translate_gemini(
    segments: list[dict],
    api_key: str,
    progress_callback: Callable | None = None,
) -> list[dict]:
    import google.generativeai as genai
    genai.configure(api_key=api_key)
    model = genai.GenerativeModel('gemini-2.0-flash')

    total = len(segments)
    translated = 0

    for batch_start in range(0, total, GEMINI_BATCH_SIZE):
        batch = segments[batch_start: batch_start + GEMINI_BATCH_SIZE]

        if progress_callback:
            pct = 0.65 + (translated / total) * 0.27
            progress_callback(pct, f"Đang dịch (Gemini)... ({translated + 1}–{min(translated + len(batch), total)}/{total})")

        _gemini_batch(model, batch)
        translated += len(batch)

    if progress_callback:
        progress_callback(0.92, f"Dịch xong {total} câu!")

    return segments


def _gemini_batch(model, batch: list[dict]) -> None:
    numbered = "\n".join(f"{i + 1}. {seg['text']}" for i, seg in enumerate(batch))
    prompt = f"""Bạn là người dịch lời nhạc chuyên nghiệp sang tiếng Việt.

Yêu cầu:
- Dịch theo CẢM XÚC và Ý NGHĨA THƠ, KHÔNG dịch từng từ máy móc
- Giữ nhịp điệu và cảm xúc phù hợp với bài hát
- Trả về ĐÚNG {len(batch)} dòng, format: số. bản_dịch
- KHÔNG giải thích, KHÔNG ghi chú thêm

Lời bài hát:
{numbered}

Bản dịch tiếng Việt:"""

    try:
        response = model.generate_content(prompt)
        translations = _parse_numbered_lines(response.text, len(batch))
        for i, seg in enumerate(batch):
            seg['translation'] = translations.get(i, '')
    except Exception as e:
        for seg in batch:
            seg['translation'] = f'[Lỗi Gemini: {e}]'


def _parse_numbered_lines(text: str, expected: int) -> dict[int, str]:
    result = {}
    for line in text.strip().splitlines():
        line = line.strip()
        if not line:
            continue
        match = re.match(r'^(\d+)[.。)]\s*(.+)$', line)
        if match:
            idx = int(match.group(1)) - 1
            if 0 <= idx < expected:
                result[idx] = match.group(2).strip()
    return result
