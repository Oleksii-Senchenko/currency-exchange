import os
import telebot
import requests
from dotenv import load_dotenv


load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["start"])
def start_handler(message: telebot.types.Message):
    return bot.send_message(message.chat.id,
                            f"Hello {message.from_user.first_name}. Nice to see you here!\n\nType /help to get information about what I can do:)")




bot.polling()