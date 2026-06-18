# core/transcriber.py
"""
Nhận diện lời bài hát từ file audio sử dụng faster-whisper.
Hỗ trợ đa ngôn ngữ và trả về timestamp cho từng câu/đoạn.
"""

from faster_whisper import WhisperModel
from typing import Callable

LANGUAGE_DISPLAY = {
    'zh': '🇨🇳 Tiếng Trung',
    'ja': '🇯🇵 Tiếng Nhật',
    'ko': '🇰🇷 Tiếng Hàn',
    'en': '🇬🇧 Tiếng Anh',
    'vi': '🇻🇳 Tiếng Việt',
    'fr': '🇫🇷 Tiếng Pháp',
    'es': '🇪🇸 Tiếng Tây Ban Nha',
}

PHONETIC_LANGUAGES = {'zh', 'ja', 'ko'}


def transcribe_audio(
    audio_path: str,
    model_size: str = "medium",
    progress_callback: Callable | None = None,
) -> tuple[list[dict], str]:
    def _prog(pct: float, msg: str):
        if progress_callback:
            progress_callback(pct, msg)

    _prog(0.05, f"Đang tải model Whisper ({model_size})...\n(Lần đầu sẽ tải ~1-1.5 GB, vui lòng chờ)")

    model = WhisperModel(model_size, device="cpu", compute_type="int8")

    _prog(0.15, "Đang phân tích file audio...")

    segments_gen, info = model.transcribe(
        audio_path,
        beam_size=5,

        # ── Quan trọng: tắt VAD filter ──────────────────────────────
        # vad_filter=True gom nhiều câu thành 1 chunk lớn → ra ít segment
        # Tắt đi để Whisper tự chia theo nội dung lời hát
        vad_filter=False,

        # ── Ngăn Whisper gom câu quá dài ────────────────────────────
        # max_new_tokens giới hạn độ dài mỗi segment (~1 câu hát)
        max_new_tokens=128,

        # Không dùng context câu trước để tránh Whisper "tự bịa" thêm lời
        condition_on_previous_text=False,

        # ── Chia nhỏ theo timestamp ──────────────────────────────────
        # word_timestamps giúp Whisper xác định ranh giới câu chính xác hơn
        word_timestamps=False,
    )

    detected_lang = info.language
    lang_name = LANGUAGE_DISPLAY.get(detected_lang, f"🌐 {detected_lang.upper()}")
    _prog(0.20, f"Phát hiện ngôn ngữ: {lang_name}. Đang nhận diện lời...")

    segments = []
    for seg in segments_gen:
        text = seg.text.strip()
        if text:
            segments.append({
                'start': seg.start,
                'end': seg.end,
                'text': text,
                'phonetic': '',
                'translation': '',
            })

    _prog(0.50, f"Nhận diện xong {len(segments)} câu/đoạn.")
    return segments, detected_lang
