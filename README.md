<div align="center">
  <img src="https://media.tenor.com/ohxROUA8aW0AAAAM/shy-cute.gif" alt="Cute Yui" width="150"/>
  <h1>🌸 Vợ Của Keyl • Discord Quest Auto Completer 🌸</h1>
  <p><i>Bot hỗ trợ cày Quest Discord tự động, an toàn và siêu cấp đáng yêu!</i></p>
</div>

---

## 👑 Tôn trọng Bản Quyền (Credits)
**⚠️ QUAN TRỌNG:** Toàn bộ phần cốt lõi (Core Logic) để quét, nhận và hoàn thành các Quest trên Discord đều thuộc bản quyền của dự án gốc. Mọi người có thể tham gia Server cộng đồng của tác giả để trao đổi thêm các tính năng auto[cite: 1].

Xin gửi lời cảm ơn chân thành nhất đến tác giả **thanhdo1110** vì một mã nguồn quá tuyệt vời! ✨

Phiên bản **"Vợ của Keyl"** là một bản Fork (tùy biến) được khoác thêm "lớp áo" Discord Bot (`discord.py`) nũng nịu, dễ thương để phục vụ cho nhu cầu riêng của Server nhà mình.

---

## 🎀 Tính năng nổi bật

### 🧠 Tính năng cốt lõi (Từ bản gốc)
* **Auto Scan:** Tự động quét quest mới theo chu kỳ[cite: 1].
* **Auto Accept:** Tự động đăng ký (enroll) các quest chưa nhận[cite: 1].
* **Auto Complete:** Tự động hoàn thành quest bằng cách gửi progress (tiến độ) hoặc heartbeat (nhịp tim)[cite: 1].
* **Rate Limit Handling:** Tự động chờ và thử lại khi bị giới hạn tốc độ (báo lỗi 429)[cite: 1].
* **Build Number Fetch:** Tự động lấy `client_build_number` mới nhất từ Discord web app[cite: 1].
* **Hỗ trợ đa dạng Task:** Xử lý mượt mà các nhiệm vụ như xem video (`WATCH_VIDEO`), chơi game (`PLAY_ON_DESKTOP`, `STREAM_ON_DESKTOP`), và các hoạt động khác (`PLAY_ACTIVITY`)[cite: 1].

### 💖 Tính năng giao diện độc quyền (Vợ của Keyl)
* **Giao diện Dễ thương:** Lời thoại nũng nịu, đính kèm các ảnh GIF Yui-chan thay đổi ngẫu nhiên siêu cấp đáng yêu.
* **Thanh tiến độ Real-time:** Báo cáo tiến độ trực tiếp vào Inbox mỗi 10 giây và tự động dọn dẹp khi xong để giữ tin nhắn gọn gàng.
* **Báo cáo Kép:** Gửi báo cáo chi tiết vào Inbox, đồng thời "khoe" thành tích ra kênh Server công khai.
* **Bảo mật tuyệt đối:** Sử dụng file `.env` giấu Token. Chốt chặn Server ID độc quyền, từ chối hoạt động ở các Server lạ!

---

## 🛠️ Yêu cầu hệ thống
* Yêu cầu cài đặt Python 3.7+[cite: 1].
* Thư viện gốc: `requests`[cite: 1].
* Thư viện cho Bot: `discord.py` và `python-dotenv`.

---

## 📝 Hướng dẫn cài đặt & Sử dụng

**1. Tải bộ mã nguồn**
Tải toàn bộ thư mục code trên kho lưu trữ này về máy tính của bạn.

**2. Cài đặt thư viện**
Mở CMD/Terminal tại thư mục code và chạy lệnh:
```bash
pip install -r requirements.txt
