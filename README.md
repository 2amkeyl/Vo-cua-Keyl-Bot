<div align="center">
  <img src="https://media.tenor.com/ohxROUA8aW0AAAAM/shy-cute.gif" alt="Cute Yui" width="150"/>
  <h1>🌸 Vợ Của Keyl • Discord Quest Auto Completer 🌸</h1>
  <p><i>Bot hỗ trợ cày Quest Discord tự động, an toàn và siêu cấp đáng yêu!</i></p>
</div>

---

## 👑 Tôn trọng Bản Quyền (Credits)
**⚠️ QUAN TRỌNG:** Toàn bộ phần cốt lõi (Core Logic) để quét, nhận và hoàn thành các Quest trên Discord đều thuộc bản quyền của dự án gốc. Mọi người có thể tham gia Server cộng đồng của tác giả để trao đổi thêm các tính năng auto.

Xin gửi lời cảm ơn chân thành nhất đến tác giả **thanhdo1110** vì một mã nguồn quá tuyệt vời! ✨

Phiên bản **"Vợ của Keyl"** là một bản Fork (tùy biến) được khoác thêm "lớp áo" Discord Bot (`discord.py`) nũng nịu, dễ thương để phục vụ cho nhu cầu riêng của Server nhà mình.

---

## 🎀 Tính năng nổi bật

### 🧠 Tính năng cốt lõi (Từ bản gốc)
* **Auto Scan:** Tự động quét quest mới theo chu kỳ.
* **Auto Accept:** Tự động đăng ký (enroll) các quest chưa nhận.
* **Auto Complete:** Tự động hoàn thành quest bằng cách gửi progress (tiến độ) hoặc heartbeat (nhịp tim).
* **Rate Limit Handling:** Tự động chờ và thử lại khi bị giới hạn tốc độ (báo lỗi 429).
* **Build Number Fetch:** Tự động giả lập Discord Desktop Client bằng cách lấy `client_build_number` mới nhất từ trang Discord web app.

### 💖 Tính năng giao diện độc quyền (Vợ của Keyl)
* **Giao diện Dễ thương:** Lời thoại nũng nịu, đính kèm các ảnh GIF Yui-chan thay đổi ngẫu nhiên siêu cấp đáng yêu.
* **Thanh tiến độ Real-time:** Báo cáo tiến độ trực tiếp vào Inbox mỗi 10 giây và tự động dọn dẹp khi xong để giữ tin nhắn gọn gàng.
* **Báo cáo Kép:** Gửi báo cáo chi tiết vào Inbox, đồng thời "khoe" thành tích ra kênh Server công khai.
* **Bảo mật tuyệt đối:** Sử dụng file `.env` giấu Token hoàn toàn vô hình trên GitHub. Chốt chặn Server ID độc quyền, từ chối hoạt động ở các Server lạ!

---

## 🎮 Các loại nhiệm vụ (Task) hỗ trợ

Công cụ có thể xử lý mượt mà và đa dạng các loại quest sau:

| Loại Task | API Endpoint | Cơ chế hoạt động ngầm |
|---|---|---|
| `WATCH_VIDEO` | `/quests/{id}/video-progress` | Gửi timestamp tăng dần, tốc độ ~7s/lần |
| `WATCH_VIDEO_ON_MOBILE` | `/quests/{id}/video-progress` | Tương tự `WATCH_VIDEO` |
| `PLAY_ON_DESKTOP` | `/quests/{id}/heartbeat` | Gửi Heartbeat mỗi 20s với `stream_key` ngẫu nhiên |
| `STREAM_ON_DESKTOP` | `/quests/{id}/heartbeat` | Tương tự `PLAY_ON_DESKTOP` |
| `PLAY_ACTIVITY` | `/quests/{id}/heartbeat` | Gửi Heartbeat mỗi 20s với `stream_key` cố định |

---

## ⚙️ Luồng hoạt động (Workflow)
Khi người dùng gõ lệnh `/quest` trên Discord, "Vợ của Keyl" sẽ kích hoạt một luồng chạy ngầm phía sau với trình tự:
1. **Khởi động:** Xác thực Token người dùng -> Lấy Build Number giả lập Client.
2. **Quét dữ liệu:** Fetch toàn bộ danh sách Quest hiện có của tài khoản.
3. **Tự động đăng ký:** Lọc và Auto-Accept các quest ở trạng thái chưa nhận.
4. **Xử lý từng Quest:** 
   * Với Video: Liên tục gửi gói tin tiến độ (Video-progress).
   * Với Game/Hoạt động: Liên tục gửi nhịp tim (Heartbeat).
5. **Cập nhật giao diện (UI):** Bot đồng thời đếm giây song song và cập nhật thanh tiến độ phần trăm vào Inbox của người dùng.
6. **Hoàn thành:** Gửi phần thưởng và trả về bảng Báo cáo tổng kết.

---

## 🏗️ Kiến trúc mã nguồn (Architecture)
Dành cho những ai muốn tìm hiểu sâu về kỹ thuật, đây là cấu trúc của phần hệ thống:
* **`DiscordAPI`**: Lớp quản lý HTTP Session với Discord API, tạo header `X-Super-Properties` giả lập người dùng thật.
* **`Quest Helpers`**: Nhóm các hàm tiện ích dùng để trích xuất dữ liệu JSON từ Quest (`get_seconds_needed`, `get_quest_name`, v.v.).
* **`QuestAutocompleter`**: Lớp trung tâm điều khiển toàn bộ logic Auto-Complete (Fetch, Enroll, Heartbeat).
* **`MyBot`** *(trong `bot.py`)*: Lớp mở rộng của `discord.py` để xử lý Slash Command, tạo giao diện UI (Embed, Button, Progress Bar) và luồng đa nhiệm `asyncio`.

---

## 🛠️ Yêu cầu hệ thống
* Python 3.7+
* Các thư viện cần thiết: `requests`, `discord.py`, `python-dotenv`.

---

## 📝 Hướng dẫn cài đặt & Sử dụng

**1. Tải bộ mã nguồn**
Tải toàn bộ thư mục code trên kho lưu trữ này về máy tính của bạn.

**2. Cài đặt thư viện**
Mở CMD/Terminal tại thư mục code và chạy lệnh:
```bash
pip install -r requirements.txt
