import allure


@allure.title("Выход их аккаунта со всех устройств")
def test_delete_v1_account_login_all(
        auth_account_helper
):
    auth_account_helper.dm_api_account.login_api.delete_v1_account_login_all()
