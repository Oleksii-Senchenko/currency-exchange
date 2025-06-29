import os

import telebot
import requests
from dotenv import load_dotenv
from requests import RequestException

from comunication import start_text, help_text,failed_to_find, unknown_currency, wrong_calculation
import json

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

sum_from = None
curr_from = None


@bot.message_handler(commands=["start"])
def start_handler(message: telebot.types.Message):
    return bot.send_message(message.chat.id,
                            f"Hello {message.from_user.first_name}. {start_text}")


@bot.message_handler(commands=["help"])
def help_handler(message: telebot.types.Message):
    return bot.send_message(message.chat.id,
                            f"{message.from_user.first_name.capitalize()}. {help_text}")


def get_currency():
    rates = requests.get("https://api.monobank.ua/bank/currency").json()
    with open("currency_rates.json", "w", encoding="utf-8") as file:
        json.dump(rates, file, indent=4)





@bot.message_handler(func=lambda message: isinstance(message.text, str) and len(message.text.strip().split()) == 2)
def get_wanted_sum_and_curr(message: telebot.types.Message):
    global sum_from, curr_from

    text = message.text.strip().upper()
    parts = text.split()


    try:
        get_currency()
    except RequestException as e:
        return bot.send_message(
            message.chat.id,
            "Failed to fetch currency data. Please try again later."
        )

    if not parts[0].isdigit():
        return bot.send_message(
            message.chat.id,
            "First part must be a number. Example: 228 UAH"
        )


    if not parts[1].isalpha() or len(parts[1]) != 3:
        return bot.send_message(
            message.chat.id,
            "Second part must be a valid currency. Example: 228 UAH"
        )

    sum_from = int(parts[0])
    curr_from = parts[1]

    return bot.send_message(
        message.chat.id,
        f"Saved: {sum_from} {curr_from}"
    )




@bot.message_handler(func=lambda message: isinstance(message.text, str) and len(message.text.split()) == 1 and message.text.isalpha())
def calculate_to_required_curr(message: telebot.types.Message):
    global sum_from, curr_from

    curr_to_convert = message.text.strip().upper()

    try:
        with open('currency_codes.json', "r") as file:
            codes_curr = json.load(file)

        source_curr_code = codes_curr[curr_from]
        target_curr_code = codes_curr[curr_to_convert]

        with open('currency_rates.json', "r") as file:
            curr_rates = json.load(file)

        found = False
        for i in curr_rates:
            if i["currencyCodeA"] == source_curr_code and i["currencyCodeB"] == target_curr_code:
                buy = i.get("rateBuy")
                sell = i.get("rateSell")
                cross = i.get("rateCross")
                found = True
                break

            elif i["currencyCodeA"] == target_curr_code and i["currencyCodeB"] == source_curr_code:
                buy = i.get("rateSell")
                sell = i.get("rateBuy")
                cross = i.get("rateCross")
                found = True
                break

        if not found:
            return bot.send_message(message.chat.id, failed_to_find)

        reply = f"💱 Exchange {sum_from} {curr_from} to {curr_to_convert}:\n"
        if buy:
            converted_buy = sum_from * buy
            reply += f"🔻 Sell ({buy:.2f}): {converted_buy:.2f} {curr_to_convert}\n"
        if sell:
            converted_sell = sum_from * sell
            reply += f"🔺 Buy ({sell:.2f}): {converted_sell:.2f} {curr_to_convert}\n"
        if not buy and not sell and cross:
            converted_cross = sum_from * cross
            reply += f"🔄 Cross rate ({cross:.2f}): {converted_cross:.2f} {curr_to_convert}"

        return bot.send_message(message.chat.id, reply)

    except KeyError:
        return bot.send_message(message.chat.id, unknown_currency)

    except Exception as e:
        print(e)
        return bot.send_message(message.chat.id, wrong_calculation)


bot.polling()
