def test_addition():

    assert 2 + 2 == 4


def test_subtraction():

    assert 10 - 5 == 5


def test_multiplication():

    assert 5 * 5 == 25


def test_division():

    assert 10 / 2 == 5


def test_string_validation():

    username = "admin"

    assert username == "admin"


def test_list_contains_value():

    users = [
        "admin",
        "tester",
        "developer"
    ]

    assert "tester" in users


def test_login_password():

    password = "1234"

    assert len(password) >= 4


def test_email_format():

    email = "user@example.com"

    assert "@" in email


def test_positive_number():

    number = 100

    assert number > 0


def test_boundary_value():

    value = 100

    assert value <= 100
