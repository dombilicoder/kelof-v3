import os
import discord
from discord import app_commands
from dotenv import load_dotenv
from aiohttp import web  # discord.py ile birlikte otomatik gelir, ekstra yüklemeye gerek yok

# .env dosyasındaki değişkenleri yüklüyoruz
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

class BilgeBot(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        bot_durumu = discord.Status.dnd
        bot_aktivitesi = discord.Game(name="coZ Code Development")
        
        super().__init__(
            intents=intents, 
            status=bot_durumu, 
            activity=bot_aktivitesi
        )
        
        self.tree = app_commands.CommandTree(self)

    # Render'ın "bot yaşıyor mu" diye kontrol etmesi için web sunucusu rotası
    async def web_handler(self, request):
        return web.Response(text="Bot aktif ve çalışıyor, sıkıntı yok hacı!")

    # discord.py v2 ile gelen setup_hook, bot başlamadan hemen önce çalışır
    async def setup_hook(self):
        # Mini web sunucusunu hazırlıyoruz
        app = web.Application()
        app.router.add_get('/', self.web_handler)
        
        runner = web.AppRunner(app)
        await runner.setup()
        
        # Render otomatik olarak bir 'PORT' değişkeni atar. Yerelde çalıştırırsan 8080'i baz alır.
        port = int(os.getenv("PORT", 8080))
        
        # Sunucuyu 0.0.0.0 ve belirlenen port üzerinde ayağa kaldırıyoruz
        site = web.TCPSite(runner, "0.0.0.0", port)
        await site.start()
        print(f"🌐 Web sunucusu 0.0.0.0:{port} üzerinde başarıyla başlatıldı!")

    async def on_ready(self):
        print(f'🤖 {self.user} olarak giriş yapıldı!')
        try:
            synced = await self.tree.sync()
            print(f"🔄 {len(synced)} adet komut başarıyla senkronize edildi.")
        except Exception as e:
            print(f"❌ Komutlar senkronize edilirken bir hata oluştu: {e}")

bot = BilgeBot()

# /selam komutu tanımlaması
@bot.tree.command(name="selam", description="Botun selamınızı almasını sağlar.")
async def selam(interaction: discord.Interaction):
    await interaction.response.send_message("Aleykümselam!")

if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("❌ Hata: .env dosyası içerisinde DISCORD_TOKEN bulunamadı!")