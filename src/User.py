class User:
    def __init__(self, username: str, password: str, firstname: str, lastname: str, authorized: bool):
        self.username = username
        self.password = password
        self.firstname = firstname
        self.lastname = lastname
        self.authorized = authorized  # To control the view

    def authorize(self):
        self.authorized = True
