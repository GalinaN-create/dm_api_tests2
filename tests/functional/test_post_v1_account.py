from datetime import datetime

import allure
import pytest
from hamcrest import assert_that, \
    starts_with

from checkers.http_checkers import check_status_code_http


@allure.title("Регистрация нового пользователя")
@pytest.mark.parametrize(
    'login, email, password', [
        ('g', 'gmav@mail.ru', '12345678Qwe!'),
        ('gmavlyutova', 'gmavmail.ru', '12345678Qwe!'),
        ('gmavlyutova', 'gmav@mail.ru', '1')
    ]
)
def test_post_v1_account(
        self,
        account_helper,
        login,
        email,
        password
):
    # login = prepare_user.login
    # password = prepare_user.password
    # email = prepare_user.email
    with check_status_code_http(400, 'Validation failed'):
        response = account_helper.register_new_user(login=login, email=email, password=password)
        today = datetime.now().strftime('%Y-%m-%d')
        assert_that(str(response.resource.registration), starts_with(today))
