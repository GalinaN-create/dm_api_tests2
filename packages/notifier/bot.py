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

os.environ["TELEGRAM_BOT_CHAT_ID"] = "-1002679774566"
os.environ["TELEGRAM_BOT_ACCESS_TOKEN"] = "7426744771:AAHqadA03JM-gXln0x5HNVAo3giXsJHrbWQ"


def send_file(
        self
):
    telegram_bot = TeleBot("7426744771:AAHqadA03JM-gXln0x5HNVAo3giXsJHrbWQ")
    file_path = Path(__file__).parent.joinpath('../../').joinpath("swagger-coverage-dm_api_account.html")
    with open(file_path,'rb') as document:
        telegram_bot.send_document(
            "-1002679774566",
            document=document,
            caption="coverage",
        )
    # print(v.get("telegram.chat_id"))
if __name__ == "__main__":
    send_file()