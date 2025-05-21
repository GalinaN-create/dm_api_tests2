from json import loads

from dm_api_account.apis.account_api import AccountApi
from helpers.account_helper import AccountHelper
from mailhog_api.apis.mailhog_api import MailhogApi
import structlog
from restclient.configuration import Configuration as DmApiConfiguration
from restclient.configuration import Configuration as MailhogConfiguration
import random
from services.dm_api_account import DmApiAccount
from services.mailhog_api import MailHogApi

# Настройка логов
structlog.configure(
    processors=[
        structlog.processors.JSONRenderer(
            indent=4,
            ensure_ascii=True,
            sort_keys=True
        )
    ]
)


def test_put_v1_account_token():
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051', disable_log=False)
    mailhog_configuration = MailhogConfiguration(host='http://5.63.153.31:5025')

    # Регистрация пользователя
    account = DmApiAccount(configuration=dm_api_configuration)
    mailhog = MailHogApi(configuration=mailhog_configuration)
    account_helper = AccountHelper(dm_api_account=account, mailhog_api=mailhog)
    login = f'gmavlyutova{random.randint(1000, 9999)}'
    email = f'{login}@mail.ru'
    password = '1234567890'

    token = account_helper.register_new_user(login=login, password=password, email=email)
    account_helper.activate_token(token=token)
