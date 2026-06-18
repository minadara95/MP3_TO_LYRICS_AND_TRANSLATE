# core/exporter.py
"""
Xuất kết quả ra file .txt và .srt.

export_txt()        — 1 file TXT tổng hợp
export_srt_triple() — 3 file SRT riêng: lời gốc / phiên âm / bản dịch
"""

import os


def export_txt(segments: list[dict], filepath: str) -> None:
    """Xuất file TXT tổng hợp, đủ 4 thành phần mỗi câu."""
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write("=" * 60 + "\n")
        f.write("  LYRIC TRANSLATOR — Kết quả dịch lời bài hát\n")
        f.write("=" * 60 + "\n\n")

        for i, seg in enumerate(segments):
            start = _fmt_display(seg['start'])
            end   = _fmt_display(seg['end'])
            f.write(f"[{i + 1:03d}]  {start} → {end}\n")
            f.write(f"  Gốc  : {seg.get('text', '')}\n")
            if phonetic := seg.get('phonetic', '').strip():
                f.write(f"  Âm   : {phonetic}\n")
            f.write(f"  Dịch : {seg.get('translation', '')}\n")
            f.write("\n")


def export_srt_triple(segments: list[dict], base_path: str) -> tuple[str, str, str]:
    """
    Xuất 3 file SRT riêng biệt từ base_path.

    Ví dụ base_path = "D:/output/bai_hat"  →  tạo ra:
        bai_hat_goc.srt       (lời gốc)
        bai_hat_phienam.srt   (phiên âm — bỏ qua nếu không có)
        bai_hat_viet.srt      (bản dịch tiếng Việt)

    Returns: tuple 3 đường dẫn đã ghi.
    """
    path_orig     = base_path + "_goc.srt"
    path_phonetic = base_path + "_phienam.srt"
    path_vi       = base_path + "_viet.srt"

    _write_srt(segments, path_orig,     key='text')
    _write_srt(segments, path_phonetic, key='phonetic')
    _write_srt(segments, path_vi,       key='translation')

    return path_orig, path_phonetic, path_vi


def _write_srt(segments: list[dict], filepath: str, key: str) -> None:
    """Ghi 1 file SRT với nội dung từ key được chỉ định."""
    index = 1
    with open(filepath, 'w', encoding='utf-8') as f:
        for seg in segments:
            content = seg.get(key, '').strip()

            # Với file dịch: bỏ qua nếu translation giống hệt text gốc
            # (dấu hiệu dịch thất bại, trả về nguyên bản)
            if key == 'translation':
                original = seg.get('text', '').strip()
                if not content or content == original:
                    continue

            elif not content:
                continue

            f.write(f"{index}\n")
            f.write(f"{_fmt_srt(seg['start'])} --> {_fmt_srt(seg['end'])}\n")
            f.write(f"{content}\n")
            f.write("\n")
            index += 1


def auto_base_path(mp3_path: str, out_dir: str | None = None) -> str:
    """
    Tạo base path tự động từ tên file MP3.
    Ví dụ: mp3_path="D:/nhac/yoru_ni_kakeru.mp3"  →  "D:/nhac/yoru_ni_kakeru"
    Nếu out_dir được truyền vào thì dùng thư mục đó thay vì thư mục MP3.
    """
    stem = os.path.splitext(os.path.basename(mp3_path))[0]
    folder = out_dir if out_dir else os.path.dirname(mp3_path)
    return os.path.join(folder, stem)


# ── Helpers timestamp ──────────────────────────────────────────────────

def _fmt_display(seconds: float) -> str:
    """MM:SS.s  — dùng trong TXT để dễ đọc."""
    m  = int(seconds // 60)
    s  = seconds % 60
    return f"{m:02d}:{s:05.2f}"


def _fmt_srt(seconds: float) -> str:
    """HH:MM:SS,mmm — chuẩn SRT."""
    h  = int(seconds // 3600)
    m  = int((seconds % 3600) // 60)
    s  = int(seconds % 60)
    ms = int(round((seconds % 1) * 1000))
    if ms >= 1000:
        s += 1
        ms = 0
    return f"{h:02d}:{m:02d}:{s:02d},{ms:03d}"
