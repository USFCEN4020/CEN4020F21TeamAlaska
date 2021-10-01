from src.database_access import database_access as Database

class User:
    def __init__(
        self,
        username: str,
        password: str,
        firstname: str,
        lastname: str,
        language: str,
        email_notification: bool,
        sms_notification: bool,
        ad_notification: bool,
        authorized: bool,
        db: Database
    ):
        self.username = username
        self.password = password
        self.firstname = firstname
        self.lastname = lastname
        self.language = language
        self.email_notification = email_notification
        self.sms_notification = sms_notification
        self.ad_notification = ad_notification
        self.db = db
        self.authorized = authorized  # To control the view

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.username == other.username and self.password == other.password and self.firstname == other.firstname and self.lastname == other.lastname and self.language == other.language and self.email_notification == other.email_notification and self.sms_notification == other.sms_notification and self.ad_notification == other.ad_notification and self.authorized == other.authorized
        return False

    def authorize(self):
        self.authorized = True

    def set_email_notification(self, email_notification: bool):
        self.email_notification = email_notification
        sql = 'UPDATE users SET email_notification = ? WHERE username = ?'
        self.db.execute(sql, [email_notification, self.username])

    def set_sms_notification(self, sms_notification: bool):
        self.sms_notification = sms_notification
        sql = 'UPDATE users SET sms_notification = ? WHERE username = ?'
        self.db.execute(sql, [sms_notification, self.username])

    def set_ad_notification(self, ad_notification: bool):
        self.ad_notification = ad_notification
        sql = 'UPDATE users SET ad_notification = ? WHERE username = ?'
        self.db.execute(sql, [ad_notification, self.username])

    def set_language(self, language: int):
        languageStr = ""
        if language == 1:
            languageStr = "english"
        elif language == 2:
            languageStr = "spanish"
        else:
            raise ValueError("language not supported")
        self.language = languageStr
        sql = 'UPDATE users SET language = ? WHERE username = ?'
        self.db.execute(sql, [languageStr, self.username])


def get_user_by_login(username: str, password: str, db: Database) -> User:
    find_user = 'SELECT * FROM users WHERE username = ? AND password = ?'
    res = db.execute(find_user, (username, password))
    if res:
        res = res[0]
        return User(res[0], res[1], res[2], res[3], res[4], res[5], res[6], res[7], True, db)
    else:
        return None


# Creates a user in the databsae
# credentials: [username, password, firstname, lastname]
def create_user(credentials: tuple, db: Database) -> User:
    default_language = "english"
    db.execute("INSERT INTO users VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
               credentials + (default_language, True, True, True))
    return User(credentials[0], credentials[1], credentials[2],
                credentials[3], default_language, True, True, True, True, db)
