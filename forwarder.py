import re
import threading
from os import environ
from flask import Flask
from pyrogram import Client, filters

# --- 1. WEB SERVER FOR RENDER/UPTIMEROBOT ---
app = Flask(__name__)

@app.route('/')
def home():
    return "Mikasa Gatekeeper is Online! 📚"

def run_flask():
    # Render looks for a web server on port 10000
    app.run(host='0.0.0.0', port=10000)

# --- 2. THE BOT LOGIC ---
API_ID = int(environ.get("API_ID"))
API_HASH = environ.get("API_HASH")
BOT_TOKEN = environ.get("BOT_TOKEN")
BIN_CHANNEL = int(environ.get("BIN_CHANNEL"))
ALLOWED_GROUP = int(environ.get("ALLOWED_GROUP"))

# Pattern: Title by Author [Lang] (Vol/Year optional)
SMART_PATTERN = r".+ by .+ \[.+\](?:.*(?:vol|volume|v|vol\.)\s?\d+)?(?:.*\d{4})?.*"

bot = Client("MikasaGatekeeper", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.chat(ALLOWED_GROUP) & filters.document)
async def smart_forwarder(client, message):
    file_name = message.document.file_name
    if not file_name: return
    if not file_name.lower().endswith(('.pdf', '.epub', '.mobi', '.cbz')):
        return

    if re.match(SMART_PATTERN, file_name, re.IGNORECASE):
        # Format is perfect! Copy to Library
        await message.copy(BIN_CHANNEL)
        await message.reply_text(f"✅ **Verified & Added:**\n`{file_name}`")
    else:
        # Wrong format - help the user
        await message.reply_text(
            "❌ **Invalid Format!**\n\n"
            "Please rename to: `Book Name by Author [Language] Vol 01`"
        )

# --- 3. STARTING EVERYTHING ---
if __name__ == "__main__":
    # Start the web server in the background thread
    threading.Thread(target=run_flask, daemon=True).start()
    # Start the bot in the main thread
    bot.run()
