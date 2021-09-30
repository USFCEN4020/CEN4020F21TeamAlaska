from src.database_access import database_access as Database
db = Database("InCollege.sqlite3")


class User:
    def __init__(self, username: str, password: str, firstname: str, lastname: str, authorized: bool, email_notification: bool, sms_notification: bool, ad_notification: bool):
        self.username = username
        self.password = password
        self.firstname = firstname
        self.lastname = lastname
        self.email_notification = email_notification
        self.sms_notification = sms_notification
        self.ad_notification = ad_notification
        self.authorized = authorized  # To control the view

    def authorize(self):
        self.authorized = True

    def set_email_notification(self, email_notification: bool):
        self.email_notification = email_notification
        sql = 'UPDATE users SET email_notification = ? WHERE username = ?'
        db.execute(sql, [email_notification, self.username])

    def set_sms_notification(self, sms_notification: bool):
        self.sms_notification
        sql = 'UPDATE users SET sms_notification = ? WHERE username = ?'
        db.execute(sql, [sms_notification, self.username])

    def set_ad_notification(self, ad_notification: bool):
        self.ad_notification
        sql = 'UPDATE users SET ad_notification = ? WHERE username = ?'
        db.execute(sql, [ad_notification, self.username])


def get_user_by_login(username: str, password: str) -> User:
    find_user = (
        'SELECT * FROM users WHERE username = ? AND password = ?')
    res = db.execute(find_user, (username, password))
    if res:
        res = res[0]
        return User(res[0], res[1], res[2], res[3], res[4], res[5], res[6], True)
    else:
        return None
