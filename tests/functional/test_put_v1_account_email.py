from checkers.http_checkers import check_status_code_http


def test_put_v1_account_email(
        account_helper,
        prepare_user
):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    token = account_helper.register_new_user(login=login, password=password, email=email)
    account_helper.activate_token(token=token)
    account_helper.login_user(login=login, password=password)
    account_helper.update_email(login=login, password=password, email=email)
    with check_status_code_http(403, "User is inactive. Address the technical support for more details"):
        account_helper.login_user(login=login, password=password)
    token_2 = account_helper.get_token_by_email(login=login)
    account_helper.activate_token(token=token_2)
    response = account_helper.login_user(login=login, password=password)
    assert response.status_code == 200, "Токен не активирован"
