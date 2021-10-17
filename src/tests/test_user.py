import pytest
from src.User import *


# To use db instance, pass data as a parameter to the test
# then you can use the data dictionary inside your test
@pytest.fixture(scope='module')
def data():
    # Setup
    db_name = "testing.sqlite3"
    db = Database(db_name)
    # in case an error breaks the code before the Teardown is reached.
    db.delete_users_table()
    # Initializes a user object in the db before any test runs
    credentials = ("darvelo", "password1!", "daniel", "arvelo")
    user = create_user(credentials, db)

    data = {"user": user, "db": db}
    yield data

    # Deletes user from db after all tests run
    db.delete_users_table()
    db.close()


def test_get_user_by_login(data):
    expected = User("darvelo", "password1!", "daniel", "arvelo", "english",
                    True, True, True, True, data["db"])
    actual = get_user_by_login(
        expected.username, expected.password, expected.db)
    assert actual == expected


def test_get_user_by_username(data):
    expected = User("darvelo", "password1!", "daniel", "arvelo", "english",
                    True, True, True, True, data["db"])

    actual = get_user_by_username(expected.username, expected.db)

    assert actual == expected


def test_create_user(data):
    expected = User("randion", "Password1!", "robert", "andion", "english",
                    True, True, True, True, data["db"])

    credentials = ("randion", "Password1!", "robert", "andion")
    actual = create_user(credentials, data["db"])

    assert actual == expected

    actual = get_user_by_login(
        expected.username, expected.password, expected.db)
    assert actual == expected


def test_authorize(data):
    user = User("", "", "", "", "", False, False, False, False, data["db"])
    # test before (input is False)
    assert user.authorized == False
    user.authorize()

    # test after
    assert user.authorized == True
    user.authorize()

    # test if input is True
    assert user.authorized == True


def test_set_email_notification(data):
    sql = 'SELECT email_notification FROM users WHERE username = ?'
    user = data["user"]
    assert user.email_notification == True

    # test object changed
    user.set_email_notification(False)
    assert user.email_notification == False

    # test database changed
    email_notification = data["db"].execute(sql, [user.username])[0][0]
    assert email_notification == False

    user.set_email_notification(True)
    assert user.email_notification == True

    email_notification = data["db"].execute(sql, [user.username])[0][0]
    assert email_notification == True


def test_set_sms_notification(data):
    sql = 'SELECT sms_notification FROM users WHERE username = ?'
    user = data["user"]
    assert user.sms_notification == True

    user.set_sms_notification(False)
    assert user.sms_notification == False

    sms_notification = data["db"].execute(sql, [user.username])[0][0]
    assert sms_notification == False

    user.set_sms_notification(True)
    assert user.sms_notification == True

    sms_notification = data["db"].execute(sql, [user.username])[0][0]
    assert sms_notification == True


def test_set_ad_notification(data):
    sql = 'SELECT ad_notification FROM users WHERE username = ?'
    user = data["user"]
    assert user.ad_notification == True

    user.set_ad_notification(False)
    assert user.ad_notification == False

    ad_notification = data["db"].execute(sql, [user.username])[0][0]
    assert ad_notification == False

    user.set_ad_notification(True)
    assert user.ad_notification == True

    ad_notification = data["db"].execute(sql, [user.username])[0][0]
    assert ad_notification == True


def test_set_language(data):
    sql = 'SELECT language FROM users WHERE username = ?'
    user = data["user"]

    user.set_language('1')
    language = data["db"].execute(sql, [user.username])[0][0]
    assert language == 'english'

    user.set_language('2')
    language = data["db"].execute(sql, [user.username])[0][0]
    assert language == 'spanish'

    with pytest.raises(ValueError):
        user.set_language('fo')
