import discord
from discord import app_commands
from discord.ext import commands
import wavelink

TOKEN = "YOUR_BOT_TOKEN"  # 🔁 Thay bằng token bot Discord của bạn

intents = discord.Intents.default()
bot = commands.Bot(command_prefix="!", intents=intents)

# Khi bot sẵn sàng
@bot.event
async def on_ready():
    print(f"✅ Bot đã đăng nhập thành {bot.user}")
    try:
        await wavelink.NodePool.create_node(
            bot=bot,
            host="lava.link",   # có thể thay bằng node LavaLink riêng
            port=80,
            password="youshallnotpass"
        )
        print("🎵 Kết nối LavaLink thành công!")
    except Exception as e:
        print("❌ Không thể kết nối LavaLink:", e)

# Slash command /start
@bot.tree.command(name="start", description="Bot vào voice channel và phát nhạc")
@app_commands.describe(channel_id="ID của voice channel")
async def start(interaction: discord.Interaction, channel_id: str):
    channel = bot.get_channel(int(channel_id))
    if not isinstance(channel, discord.VoiceChannel):
        await interaction.response.send_message("⚠️ ID không phải là voice channel!", ephemeral=True)
        return

    vc = await channel.connect(cls=wavelink.Player)
    await interaction.response.send_message(f"✅ Đã vào kênh **{channel.name}** và bắt đầu phát nhạc!")

    # Lặp nhạc liên tục (ví dụ 1 bài từ YouTube)
    track = await wavelink.YouTubeTrack.search("https://www.youtube.com/watch?v=jfKfPfyJRdk", return_first=True)
    await vc.play(track, replace=True)

# Slash command /stop
@bot.tree.command(name="stop", description="Dừng phát nhạc và rời kênh")
async def stop(interaction: discord.Interaction):
    if not interaction.guild.voice_client:
        await interaction.response.send_message("⚠️ Bot không đang trong kênh nào!", ephemeral=True)
        return

    await interaction.guild.voice_client.disconnect()
    await interaction.response.send_message("🛑 Đã dừng phát và rời kênh!")

bot.run(TOKEN)
