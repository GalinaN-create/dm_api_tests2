from datetime import datetime

from hamcrest import assert_that, \
    has_property, \
    equal_to, \
    all_of, \
    instance_of, \
    starts_with, \
    has_properties


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
    # return response
    assert_that(
        response, all_of(
            has_property(
                "resource", has_property("login", starts_with("gmavlyutova"))
            ),
            has_property("resource", has_property("registration", instance_of(datetime))),
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
                )
        )
    )
