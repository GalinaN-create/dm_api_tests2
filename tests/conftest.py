import datetime
from collections import namedtuple
from json import loads

import pytest

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


@pytest.fixture(scope="session")
def mailhog_api():
    mailhog_configuration = MailhogConfiguration(host='http://5.63.153.31:5025')
    mailhog = MailHogApi(configuration=mailhog_configuration)
    return mailhog


@pytest.fixture(scope="session")
def account_api():
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051', disable_log=False)
    account = DmApiAccount(configuration=dm_api_configuration)
    return account


@pytest.fixture(scope="session")
def account_helper(
        account_api,
        mailhog_api
):
    account_helper = AccountHelper(dm_api_account=account_api, mailhog_api=mailhog_api)
    return account_helper


@pytest.fixture
def prepare_user():
    now = datetime.datetime.now()
    data = now.strftime("%d_%m_%Y_%H_%M_%S")
    login = f'gmavlyutova{data}'
    email = f'{login}@mail.ru'
    password = '1234567890'
    User = namedtuple('User', ['login', 'password', 'email'])
    user = User(login=login, password=password, email=email)
    return user