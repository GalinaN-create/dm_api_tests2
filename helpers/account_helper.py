from json import loads

import allure

from clients.http.dm_api_account.models.change_email import ChangeEmail
from clients.http.dm_api_account.models.change_password import ChangePassword
from clients.http.dm_api_account.models.login_credentials import LoginCredentials
from clients.http.dm_api_account.models.registration import Registration
from clients.http.dm_api_account.models.reset_password import ResetPassword
from services.dm_api_account import DmApiAccount
from services.mailhog_api import MailHogApi


def retry_if_result_none(
        result
):
    """Return True if we should retry (in this case when result is None), False otherwise"""
    return result is None


def retrier(
        function
):
    def wrapper(
            *args,
            **kwargs
    ):
        token = None
        count = 0
        while token is None:
            print(f'Попытка получения токена - {count}')
            token = function(*args, **kwargs)
            count += 1
            if count == 5:
                raise AssertionError("Превышено количество попыток получения токена")
        return token

    return wrapper


class AccountHelper:

    def __init__(
            self,
            dm_api_account: DmApiAccount,
            mailhog_api: MailHogApi
    ):
        self.dm_api_account = dm_api_account
        self.mailhog_api = mailhog_api

    def auth_client(
            self,
            login: str,
            password: str,
            validate_response=False
    ):
        login_credentials = LoginCredentials(
            login=login,
            password=password,
            remember_me=True
        )
        response = self.dm_api_account.login_api.post_v1_account_login(
            login_credentials=login_credentials, validate_response=validate_response
        )
        token = {
            "x-dm-auth-token": response.headers["x-dm-auth-token"]
        }
        self.dm_api_account.account_api.set_headers(token)
        self.dm_api_account.login_api.set_headers(token)

    def auth_new_client(
            self,
            login: str,
            password: str,
            email: str
    ):
        token_email = self.register_new_user(login=login, password=password, email=email)
        self.activate_token(token=token_email)
        self.auth_client(login=login, password=password)

    @allure.step("Регистрация нового пользователя")
    def register_new_user(
            self,
            login: str,
            password: str,
            email: str
    ):
        registration = Registration(
            login=login,
            email=email,
            password=password
        )

        response = self.dm_api_account.account_api.post_v1_account(registration=registration)
        assert response.status_code == 201, "Пользователь не зарегистрирован, возможно уже существует"

        token = self.get_token_by_login(login)
        assert token is not None, "Токен с этим пользователем не найден"
        return token

    @allure.step("Авторизация пользователя")
    def login_user(
            self,
            login: str,
            password: str,
            remember_me: bool = True,
            validate_response=False,
            validate_headers=False
    ):
        login_credentials = LoginCredentials(
            login=login,
            password=password,
            remember_me=remember_me
        )

        response = self.dm_api_account.login_api.post_v1_account_login(
            login_credentials=login_credentials, validate_response=validate_response
        )
        if validate_headers:
            assert response.headers["x-dm-auth-token"], 'Проблема с токеном'
        return response

    @allure.step("Изменение почты пользователя")
    def update_email(
            self,
            login: str,
            password: str,
            email: str
    ):
        change_email = ChangeEmail(
            login=login,
            password=password,
            email=f'!{email}'
        )
        response = self.dm_api_account.account_api.put_v1_account_email(change_email=change_email)
        assert response.status_code == 200, "Почта пользователя не изменена"

    @allure.step("Активация токена")
    def activate_token(
            self,
            token: str,
            validate_response=False
    ):
        response = self.dm_api_account.account_api.put_v1_account_token(
            token=token, validate_response=validate_response
        )

    @allure.step("Получение токена после изменения почты")
    def get_token_by_email(
            self,
            login: str
    ):
        # На почте находим токен по новому емейлу для подтверждения смены емейла

        token = self.get_token_by_login(login=login)
        assert token is not None, "Токен с этим пользователем не найден"
        return token

    @allure.step("Изменение пароля")
    def change_password(
            self,
            login: str,
            old_password: str,
            new_password: str,
            email: str
    ):
        reset_password = ResetPassword(
            login=login,
            email=email
        )

        self.dm_api_account.account_api.post_v1_account_password(reset_password=reset_password)
        token = self.get_token_by_login(login=login)
        change_password = ChangePassword(
            login=login,
            token=token,
            oldPassword=old_password,
            newPassword=new_password
        )
        response = self.dm_api_account.account_api.put_v1_account_password(change_password=change_password)
        return response

    @allure.step("Получение токена по логину")
    @retrier
    def get_token_by_login(
            self,
            login
    ):
        response = self.mailhog_api.mailhog_api.get_api_v2_messages()
        assert response.status_code == 200, "Письма не получены"
        token = None
        for item in response.json()['items']:
            data = loads(item['Content']['Body'])
            login_data = data['Login']
            if login_data == login and 'ConfirmationLinkUri' in data:
                token = data['ConfirmationLinkUri'].split('/')[-1]
            elif login_data == login and 'ConfirmationLinkUrl' in data:
                token = data['ConfirmationLinkUrl'].split('/')[-1]
            return token
        return None
