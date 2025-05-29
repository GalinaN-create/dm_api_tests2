def test_delete_v1_account_login(
        account_helper
):
    json_data = {
        "message": "string"
    }
    account_helper.dm_api_account.login_api.delete_v1_account_login(json_data=json_data)
