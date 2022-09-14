import asyncio
import discord
from discord.ext.commands import Bot
import os
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import filters, MessageHandler, ApplicationBuilder, ContextTypes, PicklePersistence

load_dotenv()

class DiscordCommand:
    def __init__(self, name, handler, ctx = False):
      self.name = name
      self.handler = handler
      self.ctx = ctx

    async def execute_command(self, channel, args, ctx):
        await self.handler(channel, args, ctx)

intents = discord.Intents.default()
intents.message_content = True

prompt = '>_'
client = Bot(description="My Cool Bot", command_prefix=prompt, pm_help = False, intents=intents)
defined_commands = []

async def send_to_telegram(msg):
    await app.bot.send_message(chat_id=os.getenv('TELEGRAM_CHANNEL'), text=msg) # AIAMOND Chat

@client.event
async def on_ready():
    print("Ready")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if not message.content.startswith(prompt):
        if str(message.channel.category_id) == str(os.getenv('DISCORD_CATEGORY')):
            await send_to_telegram('Discord--> ' + message.channel.name + " (" + message.author.name + "): " + message.content)
        return

    cmd = next((c for c in defined_commands if message.content.startswith(prompt + ' ' + c.name)))
    if cmd is not None:
        await cmd.execute_command(message.channel, message.content.replace(prompt + ' ' + cmd.name, ''), message)

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.username == "discord_connector_bot":
        return

    if update.message.reply_to_message.text[0:10] == "Discord-->":
        found_channel = ""
        for server in client.guilds:
            for schannel in server.channels:
                if str(schannel.type) == 'text' and schannel.name == update.message.reply_to_message.text[11:update.message.reply_to_message.text.find("(")].strip():
                    found_channel = schannel

        if found_channel:
            await found_channel.send("Telegram (" + update.message.from_user.first_name + "): " + update.message.text)

async def freqtrade_echo_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.username == "aiamond_freqtrade_bot" and update.message.reply_to_message.text.find("Open Rate") > -1:
        found_channel = ""
        for server in client.guilds:
            for schannel in server.channels:
                if str(schannel.type) == 'text' and schannel.id == os.getenv('FREQ_DISCORD_CHANNEL'):
                    found_channel = schannel

        if found_channel:
            await found_channel.send("FREQTRADE: " + update.message.text)


my_persistence = PicklePersistence(filepath='./pers', update_interval=1)
app = ApplicationBuilder().token(os.getenv('TELEGRAM_TOKEN')).persistence(persistence=my_persistence).build()
echo_handler = MessageHandler(filters.REPLY, echo)
app.add_handler(echo_handler)

freqtrade_echo = MessageHandler(filters.CHAT, freqtrade_echo_handler)
app.add_handler(freqtrade_echo)

async def startT():
    await app.initialize()
    await app.updater.initialize()
    await app.updater.start_polling()
    await app.start()

async def startD():
    await client.start(os.getenv('DISCORD_TOKEN'))

async def main():
    tasks = [await startT(), await startD()]
    await asyncio.gather(*tasks)

asyncio.run(main())
