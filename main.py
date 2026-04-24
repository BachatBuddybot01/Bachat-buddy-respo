import asyncio
import re
import os
from telethon import TelegramClient
import aiohttp

# 🔐 Load ENV variables
API_ID = os.getenv("API_ID")
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHANNEL = os.getenv("CHANNEL")

# ❗ Safety check
if not API_ID or not API_HASH or not BOT_TOKEN or not CHANNEL:
    raise ValueError("❌ Missing environment variables")

API_ID = int(API_ID)

# 📡 Source channels
SOURCE_CHANNELS = [
    "realearnkaro",
    "offerzone4",
    "offerzone3"
]

# 🧠 Duplicate protection
posted = set()

client = TelegramClient("session", API_ID, API_HASH)

# 🔗 Extract first link
def extract_link(text):
    links = re.findall(r'https?://\S+', text)
    return links[0] if links else None

# 💰 Add Amazon affiliate tag
def add_amazon_tag(url):
    if "amazon.in" in url:
        if "tag=" not in url:
            if "?" in url:
                return url + "&tag=bachatbuddy07-21"
            else:
                return url + "?tag=bachatbuddy07-21"
    return url

# 🧠 Filter valid deals
def is_valid(text):
    text_low = text.lower()

    if "₹" not in text:
        return False

    if any(x in text_low for x in ["expired", "over", "fake"]):
        return False

    if len(text) < 25:
        return False

    return True

# 📤 Send message
async def send_message(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"

    async with aiohttp.ClientSession() as session:
        await session.post(url, json={
            "chat_id": CHANNEL,
            "text": message,
            "disable_web_page_preview": False
        })

# 🚀 Main loop
async def run():
    await client.start()
    print("✅ Bot started successfully")

    while True:
        try:
            for ch in SOURCE_CHANNELS:
                async for msg in client.iter_messages(ch, limit=5):

                    if not msg.text:
                        continue

                    unique_id = f"{ch}_{msg.id}"
                    if unique_id in posted:
                        continue

                    text = msg.text.strip()

                    if not is_valid(text):
                        continue

                    link = extract_link(text)
                    if not link:
                        continue

                    # 💰 Add affiliate
                    link = add_amazon_tag(link)

                    final_message = f"""🛍 LOOT DEAL

{text}

🔥 Grab Now:
{link}

👉 Join {CHANNEL}
"""

                    print(f"📢 Posting from {ch}")

                    await send_message(final_message)

                    posted.add(unique_id)

                    await asyncio.sleep(2)

            await asyncio.sleep(60)

        except Exception as e:
            print("❌ Error:", e)
            await asyncio.sleep(10)

# ▶️ Start bot
asyncio.run(run())