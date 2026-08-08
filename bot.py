import discord
from discord.ext import commands
from discord import app_commands
import asyncio
import io
import sys
import time
import contextlib
import random
import os
from dotenv import load_dotenv
load_dotenv()

# Import thêm các hàm lấy thời gian từ main.py
from main import (
    DiscordAPI, QuestAutocompleter, fetch_latest_build_number, 
    is_enrolled, is_completed, is_completable, 
    get_quest_name, get_task_type, get_seconds_needed, get_seconds_done
)

class MyBot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix='/', intents=intents)

    async def setup_hook(self):
        await self.tree.sync()
        print("Đã đồng bộ Slash Command xịn xò thành công! :3")

bot = MyBot()

LATEST_BUILD = fetch_latest_build_number()

# Biến lưu Emoji tim động
HEART = "<a:klg23:1535400172199350332>"

# Danh sách 4 ảnh GIF cute của chồng đưa
GIF_LIST = [
    "https://i.pinimg.com/originals/18/a9/39/18a939b5eac122121cfe77defeec0e3e.gif",
    "https://media.tenor.com/iaGQEpzcRW0AAAAM/yui.gif",
    "https://media.tenor.com/tkgTNOL3nxoAAAAM/k-on-yui-hirasawa.gif",
    "https://giffiles.alphacoders.com/349/34964.gif"
]

# --- HÀM VẼ THANH TIẾN ĐỘ ---
def make_progress_bar(percentage: float) -> str:
    percentage = max(0.0, min(100.0, percentage))
    filled = int(percentage / 5) # Chia thành 20 ô vuông
    empty = 20 - filled
    return f"{'▓' * filled}{'░' * empty} **{percentage:.1f}%**"


# --- HÀM CÀY QUEST & CẬP NHẬT TIẾN ĐỘ ---
async def run_quests_with_progress(user_token: str, user: discord.User, is_keyl: bool) -> dict:
    def setup_and_get():
        api = DiscordAPI(user_token, LATEST_BUILD)
        if not api.validate_token():
            return None, {"status": "error", "msg": "Token không hợp lệ hoặc bị lỗi mạng!"}
        
        completer = QuestAutocompleter(api)
        quests = completer.fetch_quests()
        
        if not quests:
            return None, {"status": "error", "msg": "Tài khoản của bạn không có Quest nào!"}
            
        total = len(quests)
        completed_count = sum(1 for q in quests if is_completed(q))
        quests = completer.auto_accept(quests)
        
        actionable = [
            q for q in quests
            if is_enrolled(q) and not is_completed(q) and is_completable(q)
            and q.get("id") not in completer.completed_ids
        ]
        return completer, {"total": total, "completed_before": completed_count, "actionable": actionable}

    setup_result = await asyncio.to_thread(setup_and_get)
    completer = setup_result[0]
    data = setup_result[1]

    if completer is None:
        return data

    to_do = len(data["actionable"])
    success_count = 0

    # Bắt đầu chạy từng Quest
    for q in data["actionable"]:
        q_name = get_quest_name(q)
        q_type = get_task_type(q) or "UNKNOWN"
        sec_needed = get_seconds_needed(q)
        sec_done = get_seconds_done(q)
        
        mins = sec_needed // 60
        secs = sec_needed % 60
        
        # 1. Gửi tin nhắn Bắt đầu (0%)
        title_start = f"{HEART} Đang làm: {q_name}"
        desc_start = f"**Loại:** `{q_type}`\n**Thời gian cần:** `{mins} phút {secs} giây`\n\n{make_progress_bar(0.0)}"
        if is_keyl:
            desc_start += f"\n\n*Vợ đang cặm cụi cày cái này nha chồng yêu {HEART}*"
            
        embed_progress = discord.Embed(title=title_start, description=desc_start, color=0xffb6c1)
        embed_progress.set_thumbnail(url=random.choice(GIF_LIST)) # Lấy random GIF
        
        progress_msg = None
        try:
            progress_msg = await user.send(embed=embed_progress)
        except discord.Forbidden:
            pass 

        # Hàm cày thật
        def run_single():
            with contextlib.redirect_stdout(io.StringIO()):
                try:
                    completer.process_quest(q)
                    return True
                except Exception:
                    return False

        # 2. Tạo luồng chạy ngầm & Liên tục đếm giờ cập nhật (10s/lần)
        task = asyncio.create_task(asyncio.to_thread(run_single))
        start_time = time.time()
        
        if progress_msg:
            while not task.done():
                await asyncio.sleep(10) # 10 giây realtime
                if task.done():
                    break
                    
                elapsed = time.time() - start_time
                current_done = min(sec_done + elapsed, sec_needed)
                percent = (current_done / sec_needed * 100) if sec_needed > 0 else 0
                
                new_desc = f"**Loại:** `{q_type}`\n**Thời gian cần:** `{mins} phút {secs} giây`\n\n{make_progress_bar(percent)}"
                if is_keyl:
                    new_desc += f"\n\n*Vợ đang cặm cụi cày cái này nha chồng yêu {HEART}*"
                
                embed_progress.description = new_desc
                try:
                    await progress_msg.edit(embed=embed_progress)
                except Exception:
                    pass
                    
        success = await task
        
        # 3. Chạy xong -> Xóa tin nhắn thanh tiến độ & Gửi hộp quà
        if success:
            success_count += 1
            
            if progress_msg:
                try:
                    await progress_msg.delete() # Xóa tin nhắn thanh tiến độ đi cho gọn
                except Exception:
                    pass

            # Gửi thông báo "Quest hoàn thành!"
            if is_keyl:
                done_desc = f"**{q_name}**\nLoại: `{q_type}`\n\n{HEART} Xong rồi nha, thưởng cho vợ đi chồng yêu :3"
            else:
                done_desc = f"**{q_name}**\nLoại: `{q_type}`\n\n{HEART} Nhiệm vụ đã được hoàn thành thành công!"
                
            done_embed = discord.Embed(title=f"{HEART} Quest hoàn thành!", description=done_desc, color=0xffb6c1)
            done_embed.set_thumbnail(url=random.choice(GIF_LIST)) # Lấy random GIF
            try:
                await user.send(embed=done_embed)
            except Exception:
                pass

    return {
        "status": "success",
        "total": data["total"],
        "completed_before": data["completed_before"],
        "to_do": to_do,
        "success": success_count,
        "failed": to_do - success_count
    }


# --- GIAO DIỆN NÚT BẤM ---
class ToSView(discord.ui.View):
    def __init__(self, user_token: str, is_keyl: bool):
        super().__init__(timeout=120)
        self.user_token = user_token
        self.is_keyl = is_keyl

    @discord.ui.button(label="Làm đi nè 🥰", style=discord.ButtonStyle.green, custom_id="accept_btn")
    async def accept(self, interaction: discord.Interaction, button: discord.ui.Button):
        for child in self.children:
            child.disabled = True
        
        if self.is_keyl:
            desc = f"Chồng ngoan uống miếng nước đợi vợ xíu nha.\n🍰 Vợ sẽ báo cáo tiến độ vào Inbox cho anh xem nha! {HEART}"
        else:
            desc = f"Cậu ngoan uống miếng nước đợi chút xíu nha.\n🍰 Mình sẽ nhắn tiến độ từ từ vào Inbox cho cậu nhé! {HEART}"
            
        embed = discord.Embed(title=f"{HEART} Đang cặm cụi làm việc nè... {HEART}", description=desc, color=0xffb6c1)
        embed.set_thumbnail(url=random.choice(GIF_LIST))
        await interaction.response.edit_message(embed=embed, view=self)

        user = interaction.user
        channel = interaction.channel

        # Chạy cày quest
        result = await run_quests_with_progress(self.user_token, user, self.is_keyl)
        
        # Bảng Tổng Kết (Report Embed)
        if result["status"] == "error":
            title_err = f"{HEART} Chồng ơi, vợ bị vấp té rồi..." if self.is_keyl else f"{HEART} Ây da, có lỗi rồi cậu ơi..."
            desc_err = f"**Có lỗi kẹt lại nè:**\n{result['msg']}\n\n{'Chồng' if self.is_keyl else 'Cậu'} check lại giúp nha :3"
            report_embed = discord.Embed(title=title_err, description=desc_err, color=0xff6961)
        else:
            title_ok = f"{HEART} BÁO CÁO HOÀN THÀNH {HEART}"
            desc_ok = f"Tadaaa! Vợ đã dọn sạch quest cho chồng rồi nè {HEART}" if self.is_keyl else f"Tadaaa! Mình đã dọn dẹp sạch sẽ đống quest cho cậu rồi nè {HEART}"
            
            report_embed = discord.Embed(title=title_ok, description=desc_ok, color=0xffb6c1)
            report_embed.add_field(name=f"{HEART} Tình hình tủ Quest", value=f"```\nTổng cộng: {result['total']}\nĐã xong trước đó: {result['completed_before']}\nCần quét dọn: {result['to_do']}\n```", inline=False)
            report_embed.add_field(name=f"✨ Thành quả", value=f"```\nĐã xử lý: {result['to_do']}\nThành công: {result['success']}\nThất bại: {result['failed']}\n```", inline=False)
            report_embed.set_footer(text="Vợ của Keyl • Lúc nào cũng thương anh nhất 🥰" if self.is_keyl else "Vợ của Keyl • Bot xịn xò của nhà tụi mình 🥰")
        
        report_embed.set_thumbnail(url=random.choice(GIF_LIST))
        
        # 1. Chỉnh sửa tin nhắn ban đầu
        finish_embed = embed.copy()
        finish_embed.title = f"{HEART} Đã hoàn thành xong xuôi nè! {HEART}"
        finish_embed.description = f"Xong hết rồi đó, chồng xem kết quả ở dưới nha! {HEART}" if self.is_keyl else f"Quét dọn xong xuôi! Cảm ơn cậu đã dùng nha {HEART}"
        finish_embed.set_thumbnail(url=random.choice(GIF_LIST))
        try:
            await interaction.edit_original_response(embed=finish_embed)
        except Exception:
            pass

        # 2. GỬI BÁO CÁO VÀO INBOX (DM)
        try:
            msg_dm = f"Vợ cày xong gửi báo cáo nè chồng yêu {HEART}" if self.is_keyl else f"Mình gửi báo cáo dọn dẹp cho cậu nha {HEART}"
            await user.send(content=msg_dm, embed=report_embed)
        except discord.Forbidden:
            pass 

        # 3. GỬI BÁO CÁO RA KÊNH CHAT SERVER CÔNG KHAI
        if channel:
            if self.is_keyl:
                public_msg = f"Mọi người ơi! Vợ vừa dọn dẹp xong hòm quest cho chồng yêu {user.mention} rồi nè! Đảm đang chưa :3"
            else:
                public_msg = f"Tadaaa! Vợ của Keyl vừa hỗ trợ dọn dẹp quest xong cho khách yêu {user.mention} rồi nha :3"
            
            await channel.send(content=public_msg, embed=report_embed)


    @discord.ui.button(label="Thôi hổng cần 🥺", style=discord.ButtonStyle.gray, custom_id="decline_btn")
    async def decline(self, interaction: discord.Interaction, button: discord.ui.Button):
        for child in self.children:
            child.disabled = True
        desc = "Vậy thôi chồng nghỉ ngơi đi nha, cần thì gọi vợ :3" if self.is_keyl else "Cậu đổi ý thì cứ gọi lại mình nha :3"
        await interaction.response.edit_message(embed=discord.Embed(title="🧸 Đã hủy dọn dẹp", description=desc, color=0xd3d3d3), view=self)


@bot.event
async def on_ready():
    print(f'Vợ ơi, Bot {bot.user} đã sẵn sàng cày quest thật rồi nhé :3')


@bot.tree.command(name="quest", description="Gọi vợ của Keyl ra cày Auto Quest nè 🥰")
@app_commands.describe(token="Đưa chìa khóa (Token) đây nè (Tuyệt đối bảo mật nha)")
async def quest_command(interaction: discord.Interaction, token: str):
    # --- CHỐT CHẶN ĐỘC QUYỀN SERVER CỦA CHỒNG ---
    SERVER_NHA_MINH = 1535278578155921420 
    
    if interaction.guild_id != SERVER_NHA_MINH:
        tu_choi_desc = f"🥺 Ây da... Vợ chỉ được phép làm việc dọn dẹp ở trong nhà (Server) của chồng Keyl thôi.\n\nXin lỗi khách yêu nha, mình mà làm ở ngoài là chồng ghen chết đó! {HEART}"
        tu_choi_embed = discord.Embed(title=f"{HEART} Hổng được đâu ạ! {HEART}", description=tu_choi_desc, color=0xff6961)
        tu_choi_embed.set_thumbnail(url=random.choice(GIF_LIST))
        
        await interaction.response.send_message(embed=tu_choi_embed, ephemeral=True)
        return 

    # --- NẾU ĐÚNG SERVER THÌ CHẠY BÌNH THƯỜNG ---
    KEYL_ID = 1147592525696204822 
    is_keyl = (interaction.user.id == KEYL_ID)
    
    if is_keyl:
        desc = f"Trước khi vợ xắn tay áo lên cày quest, anh nhớ đọc nha:\n\n{HEART} Vợ chỉ cầm chìa khóa để chạy nhiệm vụ thôi.\n{HEART} Cày xong là vợ vứt chìa khóa đi liền!\n\nBấm nút xanh bên dưới để vợ làm việc nha chồng yêu :3"
    else:
        desc = f"Chào khách yêu, mình là bot hỗ trợ do chồng Keyl code nè :3\nTrước khi mình xắn tay áo cày quest, cậu nhớ đọc nha:\n\n{HEART} Mình chỉ cầm chìa khóa để chạy nhiệm vụ thôi.\n{HEART} Cày xong là mình vứt chìa khóa đi liền, an tâm tuyệt đối nha!\n\nBấm nút xanh bên dưới để mình bắt đầu làm việc nhé 🥰"

    embed = discord.Embed(title=f"{HEART} Lời Dặn Dò Của Vợ Keyl {HEART}", description=desc, color=0xffb6c1)
    embed.set_thumbnail(url=random.choice(GIF_LIST))
    embed.set_footer(text="Vợ của Keyl • Sẵn sàng chăm sóc tài khoản 💖")
    
    view = ToSView(user_token=token, is_keyl=is_keyl)
    await interaction.response.send_message(embed=embed, view=view, ephemeral=True)

bot.run(os.getenv('BOT_TOKEN'))