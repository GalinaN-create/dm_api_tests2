import pytest

from checkers.http_checkers import check_status_code_http
# from conftest import prepare_user


@pytest.mark.parametrize('login, email, password', [
    ('g', 'gmav@mail.ru', '12345678Qwe!'),
    ('gmavlyutova', 'gmavmail.ru', '12345678Qwe!'),
    ('gmavlyutova', 'gmav@mail.ru', '1')
])
def test_post_v1_account(
        account_helper,
        login,
        email,
        password
):
    # login = prepare_user.login
    # password = prepare_user.password
    # email = prepare_user.email
    with check_status_code_http(400, 'Validation failed'):
        account_helper.register_new_user(login=login, email=email, password=password)
