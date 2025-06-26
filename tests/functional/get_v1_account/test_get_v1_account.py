from datetime import datetime
from json import loads

from hamcrest import assert_that, \
    all_of, \
    has_property, \
    has_properties, \
    equal_to, \
    instance_of, \
    starts_with


def test_get_v1_account(
        account_helper
):
    account_helper.dm_api_account.account_api.get_v1_account()


def test_get_v1_account_auth(
        auth_account_helper
):
    response = auth_account_helper.dm_api_account.account_api.get_v1_account()
    assert_that(
        response, all_of(
            has_property(
                "resource", has_property(
                    "rating", has_properties(
                        {
                            "enabled": equal_to(True),
                            "quality": equal_to(0),
                            "quantity": equal_to(0)
                        }
                    )
                )
            ),
            has_property("resource", has_property("online", instance_of(datetime))),
            has_property("resource", has_property("login", starts_with("gmav")))
        )
    )
