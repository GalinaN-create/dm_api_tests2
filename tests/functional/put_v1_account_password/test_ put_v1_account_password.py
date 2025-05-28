def test_put_v1_account_password(
        auth_new_account_get_token_reset_password,
        account_helper,
        prepare_user
):

    account_helper.update_password(
        login=prepare_user.login, old_password=prepare_user.password, new_password=prepare_user.new_password,
        email=prepare_user.email
        )
