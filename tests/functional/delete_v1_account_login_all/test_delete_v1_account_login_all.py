def test_delete_v1_account_login_all(
        account_helper
):
    json_data = {
        "message": "Good bye!"
    }
    account_helper.dm_api_account.login_api.delete_v1_account_login_all(json_data=json_data)