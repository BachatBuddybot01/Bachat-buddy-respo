import asyncio
import re
import os
from telethon import TelegramClient
import aiohttp

# 🔐 ENV variables (set in Railway)
api_id = int(os.getenv("22399717"))
api_hash = os.getenv("32b9ab537dbb3fb3f649597f1c78660c")
BOT_TOKEN = os.getenv("8365143773:AAEefgPg4PNdqcyw2eUt1IYQXfQVlDhvGwA")
CHANNEL = os.getenv("@BachatBudy")

# 📡 Source channels
channels = [
    "realearnkaro",
    "offerzone4.0",
    "offerzone3.0"
]

# 🧠 Memory for duplicates (simple)
posted_ids = set()

client = TelegramClient("session", api_id, api_hash)

# 📤 Send message to your channel
async def send_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    async with aiohttp.ClientSession() as session:
        await session.post(url, json={
            "chat_id": CHANNEL,
            "text": message,
            "disable_web_page_preview": False
        })

# 🔗 Extract first link
def extract_link(text):
    links = re.findall(r'(https?://\S+)', text)
    return links[0] if links else None

# 🧠 Filter valid deals
def is_valid_deal(text):
    text = text.lower()

    if "₹" not in text:
        return False

    if any(x in text for x in ["expired", "over", "fake"]):
        return False

    if len(text) < 25:
        return False

    return True

# 🚀 Main loop
async def main():
    await client.start()
    print("✅ Bot started...")

    while True:
        try:
            for ch in channels:
                async for msg in client.iter_messages(ch, limit=5):

                    if not msg.text:
                        continue

                    # ❌ Skip duplicates
                    if msg.id in posted_ids:
                        continue

                    text = msg.text.strip()

                    if not is_valid_deal(text):
                        continue

                    link = extract_link(text)
                    if not link:
                        continue

                    final_msg = f"{text}\n\n👉 Join {CHANNEL}"

                    print(f"📢 Posting from {ch}")

                    await send_message(final_msg)

                    posted_ids.add(msg.id)

                    # ⏱ Prevent Telegram rate limit
                    await asyncio.sleep(2)

            # 🔁 Repeat every 60 sec
            await asyncio.sleep(60)

        except Exception as e:
            print("❌ Error:", e)
            await asyncio.sleep(10)

# ▶️ Run bot
asyncio.run(main())