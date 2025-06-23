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



amount_to_convert, curr_to_convert = get_wanted_sum_and_curr("90,EUR")


def covert_to(curr):
    with open("currency_codes.json", "r", encoding="utf-8") as file:
        codes_curr = json.load(file)

        source_curr_code = codes_curr[curr_to_convert]
        target_curr_code = codes_curr[curr.strip().upper()]

    with open("currency_rates.json", "r", encoding="utf-8") as file:
        curr_rates = json.load(file)
    found = False

    for i in curr_rates:
        if i["currencyCodeA"] == source_curr_code and i["currencyCodeB"] == target_curr_code:
            rate = i.get("rateBuy") or i.get("rateCross") or i.get("rateSell")
            if rate:
                result = amount_to_convert * rate
                print(f"{amount_to_convert} {curr_to_convert} = {result:.2f} {curr}")
                found = True
                break





        elif i["currencyCodeA"] == target_curr_code and i["currencyCodeB"] == source_curr_code:
            rate = i.get("rateSell") or i.get("rateCross") or i.get("rateBuy")
            if rate:
                result = amount_to_convert / rate
                print(f"{amount_to_convert} {curr_to_convert} = {result:.2f} {curr}")
                found = True
                break

    if not found:
        print("Пара валют не найдена.")

covert_to("KZT")

bot.polling()