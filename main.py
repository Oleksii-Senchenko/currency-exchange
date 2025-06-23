import os
import telebot
import requests
from dotenv import load_dotenv
from comunication import start_text, help_text
import json



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



def get_currency():
    rates = requests.get("https://api.monobank.ua/bank/currency").json()
    with open("currency_rates.json", "w", encoding="utf-8") as file:
        json.dump(rates, file, indent=4)

def get_wanted_sum_and_curr(ammount):
    integer, curr = ammount.split(",")
    return int(integer), curr

bot.polling()