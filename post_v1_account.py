import pprint
from json import loads

import requests


def test_post_v1_account():
    # Регистрация пользователя

    login = 'gmavlyutova4'
    email = f'{login}@mail.ru'
    password = '1234567890'

    json_data = {
        'login': login,
        'email': email,
        'password': password,
    }

    response = requests.post(url='http://5.63.153.31:5051/v1/account', json=json_data)
    print(response.status_code)
    # print(response.json())
    assert response.status_code == 201, "Пользователь не зарегистрирован, возможно уже существует"

    # Получение писем с почты

    params = {
        'limit': '50',
    }

    response = requests.get(url='http://5.63.153.31:5025/api/v2/messages', params=params, verify=False)
    print(response.status_code)
    # pprint.pprint(response.json())

    assert response.status_code == 200, "Письма не получены"

    # Получение активационного токена

    token = None
    for item in response.json()['items']:
        data = loads(item['Content']['Body'])
        login_data = data['Login']
        if login_data == login:
            print(login_data)
            token = data['ConfirmationLinkUrl'].split('/')[4]
            print(token)

    assert token is not None, "Токен с этим пользователем не найден"

    # Активация пользователя

    response = requests.put(url=f'http://5.63.153.31:5051/v1/account/{token}')
    print(response.status_code)
    # print(response.json())

    assert response.status_code == 200, "Пользователь не активирован"

    # # Авторизация

    json_data = {
        'login': login,
        'password': password,
        'rememberMe': True,
    }

    response = requests.post(url='http://5.63.153.31:5051/v1/account/login', json=json_data)
    print(response.status_code)
    # print(response.json())
    assert response.status_code == 200, "Пользователь не авторизован"
