import configparser
import enum
import os
import typing as t
from pathlib import Path
from vyper import v

from telebot import TeleBot
from telebot.apihelper import ApiTelegramException

from telegram_notifier.exceptions import TelegramNotifierError

config = Path(__file__).parent.joinpath("../../").joinpath("config")
v.set_config_name('prod')
v.add_config_path(config)
v.read_in_config()

os.environ["TELEGRAM_BOT_CHAT_ID"] = v.get("telegram.chat_id")
os.environ["TELEGRAM_BOT_ACCESS_TOKEN"] = v.get("telegram.token")


def send_file(

):
    telegram_bot = TeleBot("telegram.token")
    file_path = Path(__file__).parent.joinpath('../../').joinpath("swagger-coverage-dm_api_account.html")
    with open(file_path,'rb') as document:
        telegram_bot.send_document(
            "telegram.chat_id",
            document=document,
            caption="coverage",
        )
if __name__ == "__main__":
    send_file()