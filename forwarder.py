import re
from pyrogram import Client, filters
from os import environ

# Pulling variables from Render Environment
API_ID = int(environ.get("API_ID"))
API_HASH = environ.get("API_HASH")
BOT_TOKEN = environ.get("BOT_TOKEN")
BIN_CHANNEL = int(environ.get("BIN_CHANNEL"))
ALLOWED_GROUP = int(environ.get("ALLOWED_GROUP"))

# Smart Regex: Title by Author [Lang] (Vol/Volume/V 01) (Year)
# It handles "v1", "vol 1", "volume 01" and optional years
SMART_PATTERN = r".+ by .+ \[.+\](?:.*(?:vol|volume|v|vol\.)\s?\d+)?(?:.*\d{4})?.*"

bot = Client("MikasaGatekeeper", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

@bot.on_message(filters.chat(ALLOWED_GROUP) & filters.document)
async def smart_forwarder(client, message):
    file_name = message.document.file_name
    
    # Check extension
    if not file_name.lower().endswith(('.pdf', '.epub', '.mobi', '.cbz')):
        return

    # Check the "Smart" Naming
    if re.match(SMART_PATTERN, file_name, re.IGNORECASE):
        # Format is perfect! Copy to Library
        await message.copy(BIN_CHANNEL)
        await message.reply_text(f"📚 **Success!** `{file_name}` added to Library.")
    else:
        # Wrong format - help the user
        await message.reply_text(
            "❌ **Invalid Format!**\n\n"
            "To keep the library organized, please name it:\n"
            "`Book Name by Author [Language] Vol 01 2024`"
        )

bot.run()
