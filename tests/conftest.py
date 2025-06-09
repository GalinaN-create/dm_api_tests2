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


@pytest.fixture()
def mailhog_api():
    mailhog_configuration = MailhogConfiguration(host='http://5.63.153.31:5025')
    mailhog = MailHogApi(configuration=mailhog_configuration)
    return mailhog


@pytest.fixture()
def account_api():
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051', disable_log=False)
    account = DmApiAccount(configuration=dm_api_configuration)
    return account


@pytest.fixture()
def account_helper(
        account_api,
        mailhog_api
):
    account_helper = AccountHelper(dm_api_account=account_api, mailhog_api=mailhog_api)
    return account_helper


@pytest.fixture()
def auth_account_helper(
        mailhog_api,
        prepare_user
):
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051', disable_log=False)
    account = DmApiAccount(configuration=dm_api_configuration)
    account_helper = AccountHelper(dm_api_account=account, mailhog_api=mailhog_api)
    account_helper.auth_client(login="gmav", password="1234567890")
    return account_helper


@pytest.fixture()
def auth_new_account_helper(
        mailhog_api,
        prepare_user
):
    dm_api_configuration = DmApiConfiguration(host='http://5.63.153.31:5051', disable_log=False)
    account = DmApiAccount(configuration=dm_api_configuration)
    account_helper = AccountHelper(dm_api_account=account, mailhog_api=mailhog_api)
    token = account_helper.auth_new_client(
        login=prepare_user.login, password=prepare_user.password, email=prepare_user.email
        )

    return account_helper, token


@pytest.fixture()
def prepare_user():
    now = datetime.datetime.now()
    data = now.strftime("%d_%m_%Y_%H_%M_%S_%f")[:-3]
    login = f'gmavlyutova{data}'
    email = f'{login}@mail.ru'
    password = '1234567890'
    new_password = f'{password}!'
    User = namedtuple('User', ['login', 'password', 'email', 'old_password', 'new_password'])
    user = User(
        login=login, password=password, old_password=password, email=email, new_password=new_password
        )
    return user
