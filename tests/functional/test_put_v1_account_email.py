def test_put_v1_account_email(
        account_helper,
        prepare_user
):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email
    email_2 = prepare_user.email_2

    token = account_helper.register_new_user(login=login, password=password, email=email)
    account_helper.activate_token(token=token)
    account_helper.login_activate_user(login=login, password=password)
    account_helper.update_email(login=login, password=password, email_2=email_2)
    response = account_helper.login_activate_user(login=login, password=password)
    assert response.status_code == 403, "Авторизовались без активации токена при смене почты, а не должны"
    token_2 = account_helper.get_token_by_email(login=login)
    account_helper.activate_token(token=token_2)
    response = account_helper.login_activate_user(login=login, password=password)
    assert response.status_code == 200, "Токен не активирован"
