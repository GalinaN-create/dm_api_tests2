from json import loads

from services.dm_api_account import DmApiAccount
from services.mailhog_api import MailHogApi


class AccountHelper:

    def __init__(
            self,
            dm_api_account: DmApiAccount,
            mailhog_api: MailHogApi
    ):
        self.dm_api_account = dm_api_account
        self.mailhog_api = mailhog_api

    def register_new_user(
            self,
            login: str,
            password: str,
            email: str
    ):

        json_data = {
            'login': login,
            'email': email,
            'password': password,
        }

        response = self.dm_api_account.account_api.post_v1_account(json_data=json_data)
        assert response.status_code == 201, "Пользователь не зарегистрирован, возможно уже существует"

        response = self.mailhog_api.mailhog_api.get_api_v2_messages()
        assert response.status_code == 200, "Письма не получены"

        token = self.get_token_by_login(login, response)
        assert token is not None, "Токен с этим пользователем не найден"
        return token

    def login_activate_user(
            self,
            login: str,
            password: str,
            remember_me: bool = True
    ):
        json_data = {
            'login': login,
            'password': password,
            'rememberMe': remember_me,
        }
        response = self.dm_api_account.login_api.post_v1_account_login(json_data=json_data)
        assert response.status_code == 200, "Токен не активирован"

    def login_no_activate_user(
            self,
            login: str,
            password: str,
            remember_me: bool = True
    ):
        json_data = {
            'login': login,
            'password': password,
            'rememberMe': remember_me,
        }
        response = self.dm_api_account.login_api.post_v1_account_login(json_data=json_data)
        assert response.status_code == 403, "Авторизовались без активации токена при смене почты, а не должны"

    def update_email(
            self,
            login: str,
            password: str,
            email_2: str
    ):
        new_email = {
            "login": login,
            "password": password,
            "email": email_2
        }
        response = self.dm_api_account.account_api.put_v1_account_email(json_data=new_email)
        assert response.status_code == 200, "Почта пользователя не изменена"

    def activate_token(
            self,
            token: str
    ):
        response = self.dm_api_account.account_api.put_v1_account_token(token=token)
        assert response.status_code == 200, "Пользователь не активирован"

    def get_token_by_email(
            self,
            login: str
            ):
        response = self.mailhog_api.mailhog_api.get_api_v2_messages()
        assert response.status_code == 200, "Письма не получены"

        # На почте находим токен по новому емейлу для подтверждения смены емейла

        token = self.get_token_by_login(login=login, response=response)
        assert token is not None, "Токен с этим пользователем не найден"
        return token


    @staticmethod
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
