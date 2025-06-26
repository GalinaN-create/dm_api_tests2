import allure

from clients.http.dm_api_account.models.login_credentials import LoginCredentials
from clients.http.dm_api_account.models.user_envelope import UserEnvelope
from packages.restclient.client import RestClient


class LoginApi(RestClient):

    def post_v1_account_login(
            self,
            login_credentials=LoginCredentials,
            validate_response=True
    ):
        """
        Authenticate via credentials
        :param json_data:
        :return:
        """
        response = self.post(
            path=f'/v1/account/login',
            json=login_credentials.model_dump(exclude_none=True, by_alias=True)
        )
        if validate_response:
            return UserEnvelope(**response.json())
        return response

    @allure.step("Выход из системы под текущим пользователем")
    def delete_v1_account_login(
            self,
            **kwargs
    ):
        """

        Logout as current user
        :param json_data:
        :return:
        """
        response = self.delete(
            path=f'/v1/account/login',
            **kwargs
        )
        return response

    @allure.step("Выход из системы со всех устройств")
    def delete_v1_account_login_all(
            self,
            **kwargs
    ):
        """
        Logout from every device
        :param json_data:
        :return:
        """
        response = self.delete(
            path=f'/v1/account/login/all',
            **kwargs
        )
        return response
