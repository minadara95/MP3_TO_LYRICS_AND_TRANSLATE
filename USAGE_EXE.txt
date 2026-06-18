============================================================
  LYRIC TRANSLATOR — Hướng dẫn sử dụng (Phiên bản EXE)
  Designed by: Minh Anh Du | anhminh.cowork@gmail.com
============================================================


════════════════════════════════════════════════════════════
  YÊU CẦU HỆ THỐNG
════════════════════════════════════════════════════════════

  - Windows 10 / 11 (64-bit)
  - RAM tối thiểu: 4 GB (khuyến nghị 8 GB)
  - Dung lượng trống: 3 GB (cho Whisper model)
  - Kết nối internet lần đầu để tải model


════════════════════════════════════════════════════════════
  CHẠY LẦN ĐẦU
════════════════════════════════════════════════════════════

Bước 1 — Mở app
  Double-click vào file:  LyricTranslator.exe
  ⚠ Nếu Windows hiện cảnh báo "Windows protected your PC":
     → Nhấn "More info" → "Run anyway"
     (App không có virus, chỉ bị cảnh báo vì chưa có chữ ký số)

Bước 2 — Chờ app khởi động
  Lần đầu mở app sẽ mất 10-30 giây do giải nén file.
  Các lần sau khởi động nhanh hơn.

Bước 3 — Lần đầu xử lý nhạc
  Khi nhấn "Xử lý bài hát" lần đầu tiên, app sẽ tự động
  tải Whisper model về máy (~1.5 GB).
  Cần có kết nối internet. Quá trình này mất 5-15 phút
  tùy tốc độ mạng. Từ lần 2 trở đi không cần tải lại.

  Model được lưu tại:
  C:\Users\<tên máy>\.cache\huggingface\hub\


════════════════════════════════════════════════════════════
  HƯỚNG DẪN SỬ DỤNG
════════════════════════════════════════════════════════════

── BƯỚC 1: Chọn file nhạc ──────────────────────────────────

  Nhấn "Chọn file..." ở panel trái
  Hỗ trợ định dạng: MP3, WAV, M4A, FLAC, AAC, OGG


── BƯỚC 2: Chọn model nhận diện ────────────────────────────

  small    → Nhanh (~1 phút), phù hợp thử nghiệm
  medium   → Cân bằng (~2-3 phút), khuyến nghị dùng hàng ngày ✓
  large-v3 → Chính xác nhất (~5-8 phút), dùng khi cần độ chính xác cao


── BƯỚC 3: Chọn phương thức dịch ──────────────────────────

  Google Translate (mặc định)
  → Miễn phí, không cần đăng ký, dùng được ngay
  → Phù hợp cho hầu hết các bài hát

  Gemini API
  → Dịch tự nhiên hơn, giữ văn phong bài hát tốt hơn
  → Cần API Key (lấy miễn phí tại: aistudio.google.com/apikey)
  → Nhập key vào ô "Gemini API Key" sau khi chọn


── BƯỚC 4: Xử lý bài hát ───────────────────────────────────

  Nhấn nút "▶ Xử lý bài hát"

  App sẽ tự động thực hiện:
    1. Nhận diện lời bài hát và timestamp
    2. Phát hiện ngôn ngữ (Trung / Nhật / Hàn / Anh...)
    3. Sinh phiên âm nếu cần:
         Tiếng Trung → Pinyin (ví dụ: nǐ hǎo)
         Tiếng Nhật  → Romaji (ví dụ: konnichiwa)
         Tiếng Hàn   → Romaja (ví dụ: annyeonghaseyo)
    4. Dịch toàn bộ lời sang tiếng Việt


── BƯỚC 5: Kiểm tra và chỉnh sửa ──────────────────────────

  Kết quả hiện ra bảng gồm 5 cột:
    #  |  Thời gian  |  Lời gốc  |  Phiên âm  |  Bản dịch tiếng Việt

  - Tất cả các ô đều có thể CHỈNH SỬA TRỰC TIẾP
  - Ô viền đỏ = câu bị lỗi dịch, cần sửa tay hoặc dịch lại
  - Nếu có ô đỏ: nhấn "🔄 Dịch lại X câu lỗi" để thử lại tự động


── BƯỚC 6: Xuất file ───────────────────────────────────────

  📄 Xuất .TXT
  → 1 file tổng hợp đầy đủ thông tin để lưu trữ/đối chiếu
  → Tên file tự động theo tên bài hát

  🎬 Xuất 3 file .SRT
  → Chọn thư mục lưu → app tạo tự động 3 file:

     tenbaihat_goc.srt       Lời ngôn ngữ gốc
     tenbaihat_phienam.srt   Phiên âm (Pinyin / Romaji / Romaja)
     tenbaihat_viet.srt      Bản dịch tiếng Việt ← dùng cái này cho CapCut


════════════════════════════════════════════════════════════
  IMPORT VÀO CAPCUT
════════════════════════════════════════════════════════════

  1. Mở CapCut → tạo hoặc mở project video
  2. Chọn tab "Phụ đề" (Caption) ở thanh công cụ
  3. Nhấn "Nhập phụ đề" (Import captions)
  4. Chọn file .srt muốn dùng:
       _viet.srt      → hiển thị tiếng Việt
       _goc.srt       → hiển thị lời gốc
       _phienam.srt   → hiển thị phiên âm
  5. Chỉnh font, màu, vị trí theo ý muốn trong CapCut


════════════════════════════════════════════════════════════
  LƯU Ý
════════════════════════════════════════════════════════════

  Ngôn ngữ hỗ trợ nhận diện:
    Tiếng Trung, Nhật, Hàn, Anh, Việt, Pháp, Tây Ban Nha
    và hơn 90 ngôn ngữ khác (Whisper tự phát hiện)

  Chất lượng nhận diện:
    Tốt nhất với bài hát có lời rõ, nhạc đệm vừa phải.
    Nhạc quá nhiều bass / reverb nặng có thể bị sai một số câu.
    Nên dùng model "large-v3" cho các bài khó.

  Timestamp lệch:
    Đây là giới hạn của Whisper với nhạc có beat mạnh.
    Có thể điều chỉnh timestamp trực tiếp trong CapCut
    sau khi import file SRT.

============================================================
  Mọi góp ý / hỗ trợ:
  Minh Anh Du | anhminh.cowork@gmail.com | 0982.131.095
============================================================
