# core/phonetic.py
"""
Sinh phiên âm cho các ngôn ngữ:
  - Tiếng Trung (zh) → Pinyin (có dấu thanh)
  - Tiếng Nhật (ja)  → Romaji (chuẩn Hepburn)
  - Tiếng Hàn (ko)   → Romaja (chuẩn học thuật)
  - Các ngôn ngữ khác → trả về chuỗi rỗng
"""

from typing import Callable


def get_phonetic(text: str, language: str) -> str:
    """Sinh phiên âm cho một đoạn text theo ngôn ngữ."""
    if language == 'zh':
        return _to_pinyin(text)
    elif language == 'ja':
        return _to_romaji(text)
    elif language == 'ko':
        return _to_romaja(text)
    return ''


def add_phonetics(
    segments: list[dict],
    language: str,
    progress_callback: Callable | None = None,
) -> list[dict]:
    """Thêm phiên âm vào toàn bộ danh sách segments."""
    needs_phonetic = language in ('zh', 'ja', 'ko')
    if not needs_phonetic:
        if progress_callback:
            progress_callback(0.65, f"Ngôn ngữ '{language}' không cần phiên âm, bỏ qua bước này.")
        return segments

    total = len(segments)
    for i, seg in enumerate(segments):
        seg['phonetic'] = get_phonetic(seg['text'], language)
        if progress_callback:
            pct = 0.50 + (i + 1) / total * 0.15
            progress_callback(pct, f"Sinh phiên âm... ({i + 1}/{total})")

    return segments


# ── Tiếng Trung → Pinyin ─────────────────────────────────────────────

def _to_pinyin(text: str) -> str:
    from pypinyin import pinyin, Style
    # TONE: mỗi âm tiết kèm dấu thanh (nǐ hǎo)
    result = pinyin(text, style=Style.TONE, heteronym=False)
    return ' '.join(p[0] for p in result)


# ── Tiếng Nhật → Romaji (Hepburn) ────────────────────────────────────

def _to_romaji(text: str) -> str:
    import pykakasi
    kks = pykakasi.kakasi()
    items = kks.convert(text)
    # hepburn: ký tự latin; orig: giữ nguyên nếu đã là latin/số
    parts = []
    for item in items:
        roman = item.get('hepburn') or item.get('orig', '')
        if roman.strip():
            parts.append(roman)
    return ' '.join(parts)


# ── Tiếng Hàn → Romaja ───────────────────────────────────────────────

def _to_romaja(text: str) -> str:
    from hangul_romanize import Transliter
    from hangul_romanize.rule import academic
    transliter = Transliter(academic)
    return transliter.translit(text)
