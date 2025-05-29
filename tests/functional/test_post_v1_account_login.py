# from json import loads
#
# import structlog
#
# from dm_api_account.apis.account_api import AccountApi
# from dm_api_account.apis.login_api import LoginApi
# from helpers.account_helper import AccountHelper
# from mailhog_api.apis.mailhog_api import MailhogApi
# from restclient.configuration import Configuration as DmApiConfiguration
# from restclient.configuration import Configuration as MailhogConfiguration
# import random
# from services.mailhog_api import MailHogApi
# from services.dm_api_account import DmApiAccount
#
# structlog.configure(
#     processors=[
#         structlog.processors.JSONRenderer(
#             indent=4,
#             ensure_ascii=True,
#             sort_keys=True
#         )
#     ]
# )


def test_post_v1_account_login(
        account_helper,
        prepare_user
        ):
    login = prepare_user.login
    password = prepare_user.password
    email = prepare_user.email

    token = account_helper.register_new_user(login=login, password=password, email=email)
    account_helper.activate_token(token=token)
    account_helper.login_activate_user(login=login, password=password)
