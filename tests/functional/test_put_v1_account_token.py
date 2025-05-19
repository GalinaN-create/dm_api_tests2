from json import loads

from dm_api_account.apis.account_api import AccountApi
from mailhog_api.apis.mailhog_api import MailhogApi
import structlog
from restclient.configuration import Configuration as DmApiConfiguration
from restclient.configuration import Configuration as MailhogConfiguration
import random

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
    account_api = AccountApi(dm_api_configuration)
    mailhog_api = MailhogApi(mailhog_configuration)
    login = f'gmavlyutova{random.randint(1000, 9999)}'
    email = f'{login}@mail.ru'
    password = '1234567890'

    # Регистрация пользователя

    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }

    response = account_api.post_v1_account(json_data=json_data)
    assert response.status_code == 201, "Пользователь не зарегистрирован, возможно уже существует"

    # Получение писем с почты

    response = mailhog_api.get_api_v2_messages()
    assert response.status_code == 200, "Письма не получены"

    # Получение активационного токена

    token = get_token_by_login(login, response)
    assert token is not None, "Токен с этим пользователем не найден"

    # Активация пользователя

    response = account_api.put_v1_account_token(token=token)
    assert response.status_code == 200, "Пользователь не активирован"


def get_token_by_login(
        login,
        response
):
    token = None
    for item in response.json()['items']:
        data = loads(item['Content']['Body'])
        login_data = data['Login']
        if login_data == login:
            token = data['ConfirmationLinkUrl'].split('/')[4]
        return token
    return None
