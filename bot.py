from telethon import TelegramClient, events
from telegram import Bot
import asyncio
import os
from keep_alive import keep_alive  # Keep alive faylini import qilamiz

# Telegram API ma'lumotlari
api_id = 20489573
api_hash = '88d9c2a5da125854f09f13e30a46085f'
bot_token = '7625709541:AAFsxlFVPn_ZitegOVl4DCrCEkx3tjF64K8'

# Kanal manzillari
source_channel = 'https://t.me/soliyvcc'
target_channel = 'https://t.me/+42tmSsLOKQk4NTJi'

# Telegram mijozlar
client = TelegramClient('user_session', api_id, api_hash)
bot = Bot(token=bot_token)

# Reklama so'zlari ro'yxati
blocked_keywords = ['@', 't.me', 'https://', 'obuna', 'reklama', 'ulanish', 'link']

@client.on(events.NewMessage(chats=source_channel))
async def handler(event):
    try:
        text = event.raw_text.lower()

        # Faylni yuklab olish (agar media bo‘lsa)
        file_path = None
        if event.media:
            file_path = await event.download_media()

        # Bot orqali yuborish
        if file_path:
            with open(file_path, 'rb') as f:
                sent = await bot.send_document(chat_id=target_channel, document=f, caption=event.text)
            os.remove(file_path)
        else:
            sent = await bot.send_message(chat_id=target_channel, text=event.text)

        # Reklama bo‘lsa, xabarni o‘chir
        if any(bad in text for bad in blocked_keywords):
            await asyncio.sleep(3)
            await bot.delete_message(chat_id=target_channel, message_id=sent.message_id)

    except Exception as e:
        print("Xatolik:", e)

def main():
    print("Bot ishlayapti. Postlar tekshirilmoqda...")
    client.start()
    client.run_until_disconnected()

if __name__ == '__main__':
    keep_alive()  # Flask serverni ishga tushiramiz
    main()  # Botni ishga tushuramiz
