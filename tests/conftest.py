import os

from swagger_coverage_py.reporter import CoverageReporter
import datetime
from collections import namedtuple
from pathlib import Path
from vyper import v

import pytest

from helpers.account_helper import AccountHelper
import structlog
from packages.restclient.configuration import Configuration as DmApiConfiguration
from packages.restclient.configuration import Configuration as MailhogConfiguration
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

options = (
    'service.dm_api_account',
    'service.mailhog_api',
    'user.login',
    'user.password',
    'telegram.chat_id',
    'telegram.token'
)


@pytest.fixture(scope="session", autouse=True)
def setup_swagger_coverage():
    reporter = CoverageReporter(api_name="dm-api-account", host="http://5.63.153.31:5051")
    reporter.setup("/swagger/Account/swagger.json")

    yield
    reporter.generate_report()
    reporter.cleanup_input_files()


# Функция, устанавливающая конфиг - фикстура для запуска перед тестом и получения аргументов из pytest
@pytest.fixture(scope="session", autouse=True)
def set_config(
        request
):
    config = Path(__file__).joinpath("../../").joinpath("config")
    config_name = request.config.getoption("--env")
    v.set_config_name(config_name)
    v.add_config_path(config)
    v.read_in_config()
    for option in options:
        v.set(f"{option}", request.config.getoption(f"--{option}"))
    os.environ["TELEGRAM_BOT_CHAT_ID"] = v.get('telegram.chat_id')
    os.environ["TELEGRAM_BOT_ACCESS_TOKEN"] = v.get('telegram.token')
    request.config.stash['telegram-notifier-addfields']['enviroments'] = config_name
    request.config.stash['telegram-notifier-addfields']['report'] = "https://galinan-create.github.io/dm_api_tests2/"


# Вычитываем все опции в конкретный объект vyper-config, которые хотим сохранить в переменной окружения pytest
def pytest_addoption(
        parser
):
    parser.addoption("--env", action="store", default="stg", help="run stg")

    for option in options:
        parser.addoption(f"--{option}", action="store", default=None)


@pytest.fixture()
def mailhog_api():
    mailhog_configuration = MailhogConfiguration(host=v.get("service.mailhog_api"), disable_log=False)
    mailhog = MailHogApi(configuration=mailhog_configuration)
    return mailhog


@pytest.fixture()
def account_api():
    dm_api_configuration = DmApiConfiguration(host=v.get("service.dm_api_account"), disable_log=False)
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
    dm_api_configuration = DmApiConfiguration(host=v.get("service.dm_api_account"), disable_log=False)
    account = DmApiAccount(configuration=dm_api_configuration)
    account_helper = AccountHelper(dm_api_account=account, mailhog_api=mailhog_api)
    account_helper.auth_client(login=v.get("user.login"), password=v.get("user.password"))
    return account_helper


@pytest.fixture()
def auth_new_account_helper(
        mailhog_api,
        prepare_user
):
    dm_api_configuration = DmApiConfiguration(host=v.get("service.dm_api_account"), disable_log=False)
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
    password = v.get("user.password")
    new_password = f'{password}!'
    User = namedtuple('User', ['login', 'password', 'email', 'old_password', 'new_password'])
    user = User(
        login=login, password=password, old_password=password, email=email, new_password=new_password
    )
    return user
