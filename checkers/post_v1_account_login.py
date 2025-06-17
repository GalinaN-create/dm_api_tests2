from datetime import datetime

from hamcrest import assert_that, \
    all_of, \
    has_property, \
    has_properties, \
    equal_to, \
    instance_of, \
    starts_with


class PostV1AccountLogin:

    def check_response_values(
            response
    ):
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
