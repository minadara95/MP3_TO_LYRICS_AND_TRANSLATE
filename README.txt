============================================================
  LYRIC TRANSLATOR — Hướng dẫn sử dụng
  Dịch lời bài hát & xuất phụ đề CapCut
============================================================


════════════════════════════════════════════════════════════
  LẦN ĐẦU SỬ DỤNG
════════════════════════════════════════════════════════════

Yêu cầu:
  - Windows 10/11
  - Python 3.10 trở lên (tải tại https://python.org)
    ⚠ Khi cài Python, nhớ tick chọn "Add Python to PATH"

Bước 1 — Cài đặt thư viện
  Double-click vào file:  install.bat
  Chờ cho đến khi cửa sổ hiện "Chạy app: double-click run.bat"
  (Quá trình này cần kết nối internet, mất khoảng 3-5 phút)

Bước 2 — Mở app
  Double-click vào file:  run.bat

Bước 3 — Lần đầu nhận diện nhạc
  Lần đầu tiên nhấn "Xử lý bài hát", app sẽ tự động tải
  Whisper model về máy (~1.5 GB). Cần internet, mất 5-10 phút
  tùy tốc độ mạng. Từ lần 2 trở đi không cần tải lại.


════════════════════════════════════════════════════════════
  SỬ DỤNG HÀNG NGÀY
════════════════════════════════════════════════════════════

Mở app:
  Double-click vào file:  run.bat


── PANEL TRÁI (Cài đặt) ────────────────────────────────────

1. File âm thanh
   Nhấn "Chọn file..." → chọn file MP3/WAV/M4A/FLAC

2. Model nhận diện
   - small    : nhanh (~1 phút/bài), độ chính xác tạm
   - medium   : cân bằng (~2-3 phút/bài), khuyến nghị ✓
   - large-v3 : chậm (~5-8 phút/bài), chính xác nhất

3. Backend dịch
   - Google Translate : miễn phí, không cần key, dùng được ngay
   - Gemini API       : dịch tự nhiên hơn, cần API key
     → Lấy key miễn phí tại: https://aistudio.google.com/apikey

4. Nhấn "▶ Xử lý bài hát"
   App sẽ tự động:
     - Nhận diện lời bài hát + timestamp
     - Phát hiện ngôn ngữ (Trung/Nhật/Hàn/Anh...)
     - Sinh phiên âm nếu cần (Pinyin / Romaji / Romaja)
     - Dịch sang tiếng Việt


── PANEL PHẢI (Kết quả) ────────────────────────────────────

Sau khi xử lý xong, bảng kết quả hiện ra với 5 cột:
  #  |  Thời gian  |  Lời gốc  |  Phiên âm  |  Bản dịch tiếng Việt

Tất cả các ô đều có thể sửa tay trực tiếp trước khi xuất.
Nên kiểm tra lại những câu bị nhận diện sai hoặc dịch chưa đúng.


── XUẤT FILE ───────────────────────────────────────────────

📄 Xuất .TXT
  Xuất 1 file tổng hợp gồm timestamp + lời gốc + phiên âm + bản dịch.
  Tên file đặt tự động theo tên bài hát.
  Dùng để đối chiếu, lưu trữ, hoặc in ra.

🎬 Xuất 3 file .SRT
  Chọn thư mục lưu → app tự tạo 3 file:
    tenbaihat_goc.srt      → lời ngôn ngữ gốc
    tenbaihat_phienam.srt  → phiên âm (Pinyin/Romaji/Romaja)
    tenbaihat_viet.srt     → bản dịch tiếng Việt

  Import vào CapCut:
    Mở project CapCut → chọn track cần thêm phụ đề
    → "Phụ đề" → "Nhập phụ đề" → chọn file .srt tương ứng


════════════════════════════════════════════════════════════
  GHI CHÚ
════════════════════════════════════════════════════════════

Ngôn ngữ hỗ trợ:
  Tiếng Trung  → nhận diện + sinh Pinyin (có dấu thanh)
  Tiếng Nhật   → nhận diện + sinh Romaji (chuẩn Hepburn)
  Tiếng Hàn    → nhận diện + sinh Romaja (chuẩn học thuật)
  Tiếng Anh và các ngôn ngữ khác → nhận diện + dịch thẳng,
                                    không có phiên âm

Về độ chính xác:
  Whisper hoạt động tốt với bài hát có lời rõ ràng.
  Nhạc có nhiều nhạc đệm, reverb nặng hoặc giọng thì thầm
  có thể bị nhận diện sai một số câu — nên kiểm tra lại
  trong bảng trước khi xuất.

Về timestamp:
  Timestamp trong bảng hiển thị dạng MM:SS.ss.
  Nếu thấy lệch, đây là giới hạn của Whisper với nhạc có
  nhạc đệm — bạn có thể điều chỉnh trong CapCut sau khi import.

============================================================
