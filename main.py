import os
import telebot
import requests
from dotenv import load_dotenv
from comunication import start_text, help_text

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def start_handler(message: telebot.types.Message):
    return bot.send_message(message.chat.id,
                            f"Hello {message.from_user.first_name}. {start_text}")

@bot.message_handler(commands=["help"])
def help_handler(message: telebot.types.Message):
    return bot.send_message(message.chat.id,
                            f"{message.from_user.first_name.capitalize() }. {help_text}")




bot.polling()