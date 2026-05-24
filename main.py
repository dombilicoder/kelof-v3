import os
import discord
from discord import app_commands
from dotenv import load_dotenv

# .env dosyasındaki değişkenleri yüklüyoruz
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

class BilgeBot(discord.Client):
    def __init__(self):
        # Varsayılan intent'leri (izinleri) ayarlıyoruz
        intents = discord.Intents.default()
        super().__init__(intents=intents)
        
        # Slash komutlarını yönetmek için CommandTree nesnesi oluşturuyoruz
        self.tree = app_commands.CommandTree(self)

    async def on_ready(self):
        print(f'🤖 {self.user} olarak giriş yapıldı!')
        try:
            # Komutları Discord API'sine küresel (global) olarak kaydediyoruz
            # Not: Global senkronizasyonun Discord'da görünmesi birkaç dakika sürebilir.
            synced = await self.tree.sync()
            print(f"🔄 {len(synced)} adet komut başarıyla senkronize edildi.")
        except Exception as e:
            print(f"❌ Komutlar senkronize edilirken bir hata oluştu: {e}")

bot = BilgeBot()

# /selam komutu tanımlaması
@bot.tree.command(name="selam", description="Botun selamınızı almasını sağlar.")
async def selam(interaction: discord.Interaction):
    # Kullanıcıya yanıt veriyoruz
    await interaction.response.send_message("Aleykümselam!")

if __name__ == "__main__":
    if TOKEN:
        bot.run(TOKEN)
    else:
        print("❌ Hata: .env dosyası içerisinde DISCORD_TOKEN bulunamadı!")