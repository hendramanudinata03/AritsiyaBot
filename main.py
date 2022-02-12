from telegram.ext import Updater, CommandHandler
import os
import configparser
import requests
import json
from functools import wraps

# Get configuration from config.ini
config = configparser.ConfigParser()
config.read("config.ini")

def getConfig(section, var):
    return config.get(section, var)

TG_BOT_TOKEN = getConfig("tgbot", "TG_BOT_TOKEN")
TG_ADMIN = getConfig("tgbot", "TG_ADMIN")
GH_API_URL = getConfig("ci", "GH_API_URL")
GH_TOKEN = getConfig("ci", "GH_TOKEN")

# Check for unauthorized user
def restricted(func):
    @wraps(func)
    def wrapped(update, context, *args, **kwargs):
        if update.effective_user.id != int(TG_ADMIN):
            update.message.reply_text("Unauthorized access!")
            return
        return func(update, context, *args, **kwargs)
    return wrapped

# /start
def start(update, context):
    text="Hello! I'm <b>Aritsiya</b>, @hendramanudinata03's helper! I'm here to help him with CI stuff, projects information, and more!"
    update.message.reply_text(text, parse_mode="HTML")

# /fw_dump
# Restricted - Nobody but me can execute it
@restricted
def fw_dump(update, context):
    try:
        # CI Inputs
        inputs = {
            "FW_URL": context.args[0]
        }
        # Headers
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": "token " + GH_TOKEN,
            "Content-Type": "application/json",
            "User-Agent": "request"
        }
        # POST parameters
        data = {
            "ref": "master",
            "inputs": inputs
        }
        update.message.reply_text("Dumping FW...")
        # Request
        requestCI = requests.post(GH_API_URL, data=json.dumps(data), headers=headers)
        print(requestCI.content)
    except (IndexError, ValueError):
        update.message.reply_text("<b>/fw_dump</b> - Dump Android firmware.\n\nUsage: <pre><code>/fw_dump FW_URL</code></pre>", parse_mode="HTML")    

# Start everything
def main():
    updater = Updater(TG_BOT_TOKEN, use_context=True)
    dispatcher = updater.dispatcher
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("fw_dump", fw_dump, run_async=True))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    os.system("clear")
    print("AritsiyaBot has been summoned! I'm ready to serve you, Master Hendra.\n\nStarting...")
    main()