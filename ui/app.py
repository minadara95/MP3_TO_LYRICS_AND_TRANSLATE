# ui/app.py
"""
Cửa sổ chính của Lyric Translator.

Layout:
  ┌──────────────┬─────────────────────────────────────┐
  │  Left Panel  │         Right Panel (Results)        │
  │  (Controls)  │  Header + Column labels + Table      │
  └──────────────┴─────────────────────────────────────┘
"""

import os
import threading
from tkinter import filedialog, messagebox

import customtkinter as ctk

from core.transcriber import transcribe_audio, LANGUAGE_DISPLAY, PHONETIC_LANGUAGES
from core.phonetic import add_phonetics
from core.translator import translate_lyrics
from core.exporter import export_txt, export_srt_triple, auto_base_path

# Thiết lập theme tổng thể
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Màu sắc tùy chỉnh
COLOR_BG_ROW_ODD  = "#1e1e1e"
COLOR_BG_ROW_EVEN = "#252525"
COLOR_PHONETIC    = "#9ab4ff"   # xanh nhạt cho phiên âm
COLOR_TRANSLATION = "#7ee8a2"   # xanh lá nhạt cho bản dịch
COLOR_TIMESTAMP   = "#888888"


class LyricTranslatorApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("🎵 Lyric Translator — CapCut Helper")
        self.geometry("1150x760")
        self.minsize(900, 600)

        # Trạng thái nội bộ
        self._mp3_path: str = ""
        self._segments: list[dict] = []
        self._language: str = ""
        # Mỗi phần tử là dict {text, phonetic, translation} chứa widget CTkTextbox
        self._row_widgets: list[dict] = []

        self._build_layout()

    # ─────────────────────────────────────────────────────────────────
    # Build UI
    # ─────────────────────────────────────────────────────────────────

    def _build_layout(self):
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        # Panel trái (cố định 290px)
        self._left = ctk.CTkFrame(self, width=290, corner_radius=0, fg_color="#1a1a1a")
        self._left.grid(row=0, column=0, sticky="nsew")
        self._left.grid_propagate(False)
        self._build_left_panel()

        # Panel phải (mở rộng)
        self._right = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self._right.grid(row=0, column=1, sticky="nsew", padx=8, pady=8)
        self._right.grid_rowconfigure(2, weight=1)
        self._right.grid_columnconfigure(0, weight=1)
        self._build_right_panel()

    def _build_left_panel(self):
        p = self._left
        pad = {"padx": 16}

        # ── Tiêu đề ─────────────────────────────────────────────────
        ctk.CTkLabel(p, text="🎵 Lyric Translator",
                     font=("Segoe UI", 17, "bold")).pack(pady=(22, 2), **pad)
        ctk.CTkLabel(p, text="Dịch lời nhạc → phụ đề CapCut",
                     font=("Segoe UI", 10), text_color="gray").pack(pady=(0, 10), **pad)

        # ── Chữ ký tác giả ───────────────────────────────────────────
        sig = ctk.CTkFrame(p, fg_color="#161616", corner_radius=8)
        sig.pack(fill="x", padx=16, pady=(0, 14))
        ctk.CTkLabel(sig, text="Designed by  Minh Anh Du",
                     font=("Segoe UI", 11, "bold"), text_color="#dddddd",
                     justify="left").pack(anchor="w", padx=10, pady=(8, 2))
        ctk.CTkLabel(sig, text="✉  anhminh.cowork@gmail.com",
                     font=("Segoe UI", 10, "bold"), text_color="#aaaaaa",
                     justify="left").pack(anchor="w", padx=10, pady=1)
        ctk.CTkLabel(sig, text="📞  0982.131.095",
                     font=("Segoe UI", 10, "bold"), text_color="#aaaaaa",
                     justify="left").pack(anchor="w", padx=10, pady=(1, 8))

        self._divider(p)

        # ── Chọn file MP3 ────────────────────────────────────────────
        ctk.CTkLabel(p, text="File âm thanh", font=("Segoe UI", 12, "bold")).pack(
            anchor="w", pady=(12, 4), **pad)

        btn_row = ctk.CTkFrame(p, fg_color="transparent")
        btn_row.pack(fill="x", **pad)

        ctk.CTkButton(btn_row, text="Chọn file...", width=95,
                      command=self._pick_file).pack(side="left")
        self._file_label = ctk.CTkLabel(
            btn_row, text="Chưa chọn",
            font=("Segoe UI", 10), text_color="gray",
            wraplength=155, justify="left")
        self._file_label.pack(side="left", padx=(8, 0))

        # ── Model Whisper ────────────────────────────────────────────
        ctk.CTkLabel(p, text="Model nhận diện", font=("Segoe UI", 12, "bold")).pack(
            anchor="w", pady=(16, 2), **pad)
        ctk.CTkLabel(p, text="Lớn = chính xác hơn, chậm hơn",
                     font=("Segoe UI", 10), text_color="gray").pack(anchor="w", **pad)

        self._model_var = ctk.StringVar(value="medium")
        model_options = [
            ("small",    "small  — nhanh, ổn"),
            ("medium",   "medium — cân bằng  ✓"),
            ("large-v3", "large-v3 — tốt nhất"),
        ]
        for value, label in model_options:
            ctk.CTkRadioButton(p, text=label, variable=self._model_var,
                               value=value, font=("Segoe UI", 11)).pack(
                anchor="w", padx=26, pady=2)

        # ── Backend dịch ────────────────────────────────────────────
        ctk.CTkLabel(p, text="Backend dịch", font=("Segoe UI", 12, "bold")).pack(
            anchor="w", pady=(16, 4), **pad)

        self._backend_var = ctk.StringVar(value="google")
        ctk.CTkRadioButton(
            p, text="Google Translate  (miễn phí, không cần key)",
            variable=self._backend_var, value="google",
            font=("Segoe UI", 11),
            command=self._on_backend_change,
        ).pack(anchor="w", padx=26, pady=2)
        ctk.CTkRadioButton(
            p, text="Gemini API  (tự nhiên hơn, cần key)",
            variable=self._backend_var, value="gemini",
            font=("Segoe UI", 11),
            command=self._on_backend_change,
        ).pack(anchor="w", padx=26, pady=2)

        # Frame API key — ẩn/hiện bằng cách đổi height và hide children
        self._api_frame = ctk.CTkFrame(p, fg_color="#1e2a1e", corner_radius=8)
        # Không pack ngay — chỉ pack khi chọn Gemini

        ctk.CTkLabel(self._api_frame, text="Gemini API Key",
                     font=("Segoe UI", 11, "bold")).pack(anchor="w", padx=10, pady=(8, 2))
        self._api_entry = ctk.CTkEntry(
            self._api_frame, placeholder_text="AIza...", show="*", width=240)
        self._api_entry.pack(padx=10)
        if env_key := os.environ.get("GEMINI_API_KEY", ""):
            self._api_entry.insert(0, env_key)
        ctk.CTkLabel(
            self._api_frame, text="Lấy key miễn phí: aistudio.google.com",
            font=("Segoe UI", 9), text_color="#888",
        ).pack(anchor="w", padx=10, pady=(2, 8))

        self._divider(p, top=16)

        # ── Nút xử lý ───────────────────────────────────────────────
        self._process_btn = ctk.CTkButton(
            p, text="▶  Xử lý bài hát", height=42,
            font=("Segoe UI", 13, "bold"),
            command=self._start_processing)
        self._process_btn.pack(fill="x", pady=(10, 4), **pad)

        self._status_label = ctk.CTkLabel(
            p, text="Chọn file và nhấn xử lý để bắt đầu",
            font=("Segoe UI", 10), text_color="gray",
            wraplength=258, justify="left")
        self._status_label.pack(pady=(2, 4), **pad)

        self._progress_bar = ctk.CTkProgressBar(p, width=258)
        self._progress_bar.pack(**pad)
        self._progress_bar.set(0)

    def _build_right_panel(self):
        p = self._right

        # ── Header row: tiêu đề + badge ngôn ngữ + nút export ────────
        hdr = ctk.CTkFrame(p, fg_color="transparent")
        hdr.grid(row=0, column=0, sticky="ew", pady=(0, 6))

        ctk.CTkLabel(hdr, text="Kết quả",
                     font=("Segoe UI", 14, "bold")).pack(side="left")

        self._lang_badge = ctk.CTkLabel(
            hdr, text="", font=("Segoe UI", 11),
            fg_color="#1e3a2a", corner_radius=6, padx=10, pady=2)
        self._lang_badge.pack(side="left", padx=(8, 0))

        self._count_label = ctk.CTkLabel(
            hdr, text="", font=("Segoe UI", 11), text_color="gray")
        self._count_label.pack(side="left", padx=(8, 0))

        self._retry_btn = ctk.CTkButton(
            hdr, text="🔄 Dịch lại câu lỗi", width=135, height=30,
            fg_color="#6b3a1a", hover_color="#5a2e10",
            font=("Segoe UI", 11),
            command=self._retry_failed,
        )
        # Ẩn cho đến khi có câu lỗi
        self._retry_btn.pack_forget()

        # Nút export — luôn hiển thị góc phải header
        ctk.CTkButton(
            hdr, text="🎬 Xuất 3 file .SRT", width=140, height=30,
            fg_color="#1a6b4a", hover_color="#155a3d",
            font=("Segoe UI", 11, "bold"),
            command=self._export_srt,
        ).pack(side="right", padx=(4, 0))

        ctk.CTkButton(
            hdr, text="📄 Xuất .TXT", width=105, height=30,
            fg_color="#2a4a6a", hover_color="#1e3a55",
            font=("Segoe UI", 11),
            command=self._export_txt,
        ).pack(side="right", padx=(4, 0))

        # ── Tiêu đề cột ──────────────────────────────────────────────
        col_hdr = ctk.CTkFrame(p, height=28, fg_color="#2a2a2a", corner_radius=6)
        col_hdr.grid(row=1, column=0, sticky="ew", pady=(0, 2))
        col_hdr.grid_propagate(False)
        self._configure_columns(col_hdr)

        for col_idx, text in enumerate(["#", "Thời gian", "Lời gốc", "Phiên âm", "Bản dịch tiếng Việt"]):
            ctk.CTkLabel(col_hdr, text=text,
                         font=("Segoe UI", 10, "bold"), text_color="#888").grid(
                row=0, column=col_idx, padx=6, pady=4, sticky="w")

        # ── Bảng kết quả (scrollable) ────────────────────────────────
        self._table = ctk.CTkScrollableFrame(p, fg_color="transparent")
        self._table.grid(row=2, column=0, sticky="nsew")
        self._configure_columns(self._table)

        # Placeholder khi chưa có dữ liệu
        self._placeholder = ctk.CTkLabel(
            self._table,
            text="Chọn file MP3 và nhấn ▶ Xử lý bài hát để bắt đầu...",
            font=("Segoe UI", 13), text_color="#555")
        self._placeholder.grid(row=0, column=0, columnspan=5, pady=80)

    @staticmethod
    def _configure_columns(frame):
        """Cấu hình độ rộng cột cho frame (header hoặc table)."""
        frame.grid_columnconfigure(0, minsize=36)   # #
        frame.grid_columnconfigure(1, minsize=82)   # time
        frame.grid_columnconfigure(2, weight=2)     # original
        frame.grid_columnconfigure(3, weight=2)     # phonetic
        frame.grid_columnconfigure(4, weight=3)     # translation

    @staticmethod
    def _divider(parent, top: int = 4):
        ctk.CTkFrame(parent, height=1, fg_color="#2e2e2e").pack(
            fill="x", padx=16, pady=(top, 0))

    # ─────────────────────────────────────────────────────────────────
    # Event handlers
    # ─────────────────────────────────────────────────────────────────

    def _on_backend_change(self):
        """Hiện/ẩn ô API key tuỳ theo backend được chọn."""
        if self._backend_var.get() == "gemini":
            # Chèn sau radio buttons, trước divider
            self._api_frame.pack(fill="x", padx=16, pady=(4, 0))
        else:
            self._api_frame.pack_forget()

    def _pick_file(self):
        path = filedialog.askopenfilename(
            title="Chọn file âm thanh",
            filetypes=[
                ("Audio files", "*.mp3 *.wav *.m4a *.flac *.ogg *.aac"),
                ("All files", "*.*"),
            ],
        )
        if path:
            self._mp3_path = path
            name = os.path.basename(path)
            self._file_label.configure(text=name, text_color="white")

    def _start_processing(self):
        if not self._mp3_path:
            messagebox.showwarning("Thiếu file", "Vui lòng chọn file âm thanh trước.")
            return

        backend = self._backend_var.get()
        api_key = ""
        if backend == "gemini":
            api_key = self._api_entry.get().strip()
            if not api_key:
                messagebox.showwarning(
                    "Thiếu API Key",
                    "Bạn đang dùng Gemini — hãy nhập API Key.\n"
                    "Hoặc chuyển sang Google Translate (miễn phí, không cần key).")
                return

        self._process_btn.configure(state="disabled", text="⏳ Đang xử lý...")
        self._progress_bar.set(0)
        self._status_label.configure(text="Đang khởi động...", text_color="gray")
        self._clear_table()

        threading.Thread(
            target=self._worker,
            args=(self._mp3_path, self._model_var.get(), backend, api_key),
            daemon=True,
        ).start()

    # ─────────────────────────────────────────────────────────────────
    # Background worker
    # ─────────────────────────────────────────────────────────────────

    def _worker(self, audio_path: str, model_size: str, backend: str, api_key: str):
        def prog(pct: float, msg: str):
            self.after(0, self._set_progress, pct, msg)

        try:
            segs, lang = transcribe_audio(audio_path, model_size, prog)
            segs = add_phonetics(segs, lang, prog)
            segs = translate_lyrics(segs, backend=backend, api_key=api_key,
                                    source_lang=lang, progress_callback=prog)
            self._segments = segs
            self._language = lang
            self.after(0, self._on_done, segs, lang)
        except Exception as exc:
            self.after(0, self._on_error, str(exc))

    def _set_progress(self, pct: float, msg: str):
        self._progress_bar.set(pct)
        self._status_label.configure(text=msg, text_color="gray")

    def _on_done(self, segments: list[dict], language: str):
        self._progress_bar.set(1.0)
        self._status_label.configure(
            text=f"✓ Hoàn tất! {len(segments)} câu.", text_color="#7ee8a2")
        self._process_btn.configure(state="normal", text="▶  Xử lý bài hát")

        lang_display = LANGUAGE_DISPLAY.get(language, f"🌐 {language.upper()}")
        self._lang_badge.configure(text=lang_display)
        self._count_label.configure(text=f"{len(segments)} câu")

        self._render_table(segments, language)

    def _on_error(self, error_msg: str):
        self._progress_bar.set(0)
        self._status_label.configure(text=f"❌ {error_msg}", text_color="#ff7070")
        self._process_btn.configure(state="normal", text="▶  Xử lý bài hát")
        messagebox.showerror("Lỗi xử lý", f"Có lỗi xảy ra:\n\n{error_msg}")

    # ─────────────────────────────────────────────────────────────────
    # Render table
    # ─────────────────────────────────────────────────────────────────

    def _clear_table(self):
        for w in self._table.winfo_children():
            w.destroy()
        self._row_widgets.clear()
        self._lang_badge.configure(text="")
        self._count_label.configure(text="")

    def _render_table(self, segments: list[dict], language: str):
        self._clear_table()
        has_phonetic = language in PHONETIC_LANGUAGES

        for i, seg in enumerate(segments):
            # ── Số thứ tự ──────────────────────────────────────────
            ctk.CTkLabel(
                self._table, text=str(i + 1),
                font=("Segoe UI", 10), text_color="#666", width=30,
            ).grid(row=i, column=0, padx=(4, 0), pady=(3, 0), sticky="nw")

            # ── Timestamp (MM:SS.ss để thấy rõ sub-second) ────────
            start = _fmt_mm_ss(seg['start'])
            end   = _fmt_mm_ss(seg['end'])
            ctk.CTkLabel(
                self._table, text=f"▶ {start}\n◼ {end}",
                font=("Courier New", 9), text_color=COLOR_TIMESTAMP,
                width=80, justify="left",
            ).grid(row=i, column=1, padx=2, pady=(3, 0), sticky="nw")

            # ── Lời gốc (editable) ─────────────────────────────────
            txt_box = self._make_textbox(self._table, height=52)
            txt_box.insert("1.0", seg['text'])
            txt_box.grid(row=i, column=2, padx=2, pady=2, sticky="ew")

            # ── Phiên âm (editable, mờ nếu không cần) ─────────────
            pho_box = self._make_textbox(self._table, height=52,
                                          text_color=COLOR_PHONETIC)
            pho_box.insert("1.0", seg.get('phonetic', ''))
            if not has_phonetic:
                pho_box.configure(state="disabled", fg_color="#181818",
                                  text_color="#444")
            pho_box.grid(row=i, column=3, padx=2, pady=2, sticky="ew")

            # ── Bản dịch (editable) ────────────────────────────────
            translation = seg.get('translation', '')
            original    = seg.get('text', '')
            # Đánh dấu đỏ nếu translation rỗng hoặc giống hệt text gốc (dịch lỗi)
            failed = not translation.strip() or translation.strip() == original.strip()
            tra_color  = "#ff6b6b" if failed else COLOR_TRANSLATION
            tra_border = "#8b0000" if failed else "#333"

            tra_box = self._make_textbox(self._table, height=52,
                                          text_color=tra_color,
                                          border_color=tra_border)
            tra_box.insert("1.0", translation)
            tra_box.grid(row=i, column=4, padx=(2, 4), pady=2, sticky="ew")

            self._row_widgets.append({
                'text':        txt_box,
                'phonetic':    pho_box,
                'translation': tra_box,
                'failed':      failed,
            })

        # Hiện nút retry nếu có câu lỗi
        failed_count = sum(1 for r in self._row_widgets if r.get('failed'))
        if failed_count:
            self._retry_btn.configure(text=f"🔄 Dịch lại {failed_count} câu lỗi")
            self._retry_btn.pack(side="left", padx=(8, 0))
        else:
            self._retry_btn.pack_forget()

    @staticmethod
    def _make_textbox(parent, height: int = 52, text_color: str = "white",
                      border_color: str = "#333") -> ctk.CTkTextbox:
        return ctk.CTkTextbox(
            parent,
            height=height,
            wrap="word",
            font=("Segoe UI", 11),
            fg_color="#272727",
            border_width=1,
            border_color=border_color,
            activate_scrollbars=False,
            text_color=text_color,
        )

    # ─────────────────────────────────────────────────────────────────
    # Retry failed translations
    # ─────────────────────────────────────────────────────────────────

    def _retry_failed(self):
        """Dịch lại các câu bị lỗi (translation rỗng hoặc giống text gốc)."""
        failed_indices = [
            i for i, row in enumerate(self._row_widgets) if row.get('failed')
        ]
        if not failed_indices:
            return

        self._retry_btn.configure(state="disabled", text="⏳ Đang dịch lại...")

        backend    = self._backend_var.get()
        api_key    = self._api_entry.get().strip()

        def worker():
            from core.translator import _google_translate_one, LANG_MAP
            import google.generativeai as genai

            src = LANG_MAP.get(self._language, 'auto')
            total = len(failed_indices)

            for n, i in enumerate(failed_indices):
                seg = self._segments[i]
                self.after(0, self._set_progress,
                           0.1 + n / total * 0.8,
                           f"Dịch lại... ({n + 1}/{total})")

                if backend == "gemini" and api_key:
                    try:
                        genai.configure(api_key=api_key)
                        model = genai.GenerativeModel('gemini-2.0-flash')
                        resp = model.generate_content(
                            f"Dịch câu lời bài hát sau sang tiếng Việt (chỉ trả về bản dịch, không giải thích):\n{seg['text']}"
                        )
                        result = resp.text.strip()
                    except Exception:
                        result = ""
                else:
                    result = _google_translate_one(seg['text'], src)

                if result and result != seg['text']:
                    seg['translation'] = result
                    # Cập nhật ô trong bảng
                    row = self._row_widgets[i]
                    self.after(0, self._update_translation_cell, row, result)

                import time; time.sleep(0.3)

            self.after(0, self._on_retry_done)

        threading.Thread(target=worker, daemon=True).start()

    def _update_translation_cell(self, row: dict, text: str):
        box = row['translation']
        box.configure(text_color=COLOR_TRANSLATION, border_color="#333")
        box.delete("1.0", "end")
        box.insert("1.0", text)
        row['failed'] = False

    def _on_retry_done(self):
        self._set_progress(1.0, "✓ Dịch lại xong!")
        failed_count = sum(1 for r in self._row_widgets if r.get('failed'))
        if failed_count:
            self._retry_btn.configure(
                state="normal", text=f"🔄 Dịch lại {failed_count} câu lỗi")
        else:
            self._retry_btn.pack_forget()

    # ─────────────────────────────────────────────────────────────────
    # Collect edited data + Export
    # ─────────────────────────────────────────────────────────────────

    def _collect_segments(self) -> list[dict]:
        """Đọc dữ liệu hiện tại từ các ô edit (bao gồm chỉnh sửa tay)."""
        result = []
        for i, row in enumerate(self._row_widgets):
            seg = dict(self._segments[i])
            seg['text']        = row['text'].get("1.0", "end-1c").strip()
            seg['phonetic']    = row['phonetic'].get("1.0", "end-1c").strip()
            seg['translation'] = row['translation'].get("1.0", "end-1c").strip()
            result.append(seg)
        return result

    def _export_txt(self):
        if not self._row_widgets:
            messagebox.showwarning("Chưa có dữ liệu", "Hãy xử lý bài hát trước.")
            return

        # Tên mặc định = tên file MP3 (không đuôi) + .txt
        default_name = _stem(self._mp3_path) + ".txt" if self._mp3_path else "lyrics.txt"
        path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            initialfile=default_name,
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
            title="Lưu file TXT",
        )
        if path:
            export_txt(self._collect_segments(), path)
            messagebox.showinfo("Xuất thành công", f"Đã lưu:\n{path}")

    def _export_srt(self):
        if not self._row_widgets:
            messagebox.showwarning("Chưa có dữ liệu", "Hãy xử lý bài hát trước.")
            return

        # Hỏi thư mục lưu — tên file tự động từ tên MP3
        out_dir = filedialog.askdirectory(title="Chọn thư mục lưu 3 file SRT")
        if not out_dir:
            return

        stem = _stem(self._mp3_path) if self._mp3_path else "lyrics"
        base = os.path.join(out_dir, stem)
        p_orig, p_pho, p_vi = export_srt_triple(self._collect_segments(), base)

        messagebox.showinfo(
            "Xuất thành công",
            f"Đã tạo 3 file SRT trong:\n{out_dir}\n\n"
            f"  📝 {os.path.basename(p_orig)}\n"
            f"  🔤 {os.path.basename(p_pho)}\n"
            f"  🇻🇳 {os.path.basename(p_vi)}"
        )


# ─────────────────────────────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────────────────────────────

def _fmt_mm_ss(seconds: float) -> str:
    """MM:SS.ss — hiển thị trong bảng, đủ chi tiết để phát hiện lệch timestamp."""
    m  = int(seconds // 60)
    s  = seconds % 60
    return f"{m:02d}:{s:05.2f}"


def _stem(filepath: str) -> str:
    """Lấy tên file không có đuôi mở rộng."""
    return os.path.splitext(os.path.basename(filepath))[0]
