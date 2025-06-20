from datetime import datetime

import allure

from checkers.post_v1_account_login import PostV1AccountLogin


@allure.title("Регистрация и авторизация пользователя")
def test_post_v1_account_login(
        account_helper,
        prepare_user
):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    token = account_helper.register_new_user(login=login, password=password, email=email)
    account_helper.activate_token(token=token)
    response = account_helper.login_user(login=login, password=password, validate_response=True)
    PostV1AccountLogin.check_response_values(response)
