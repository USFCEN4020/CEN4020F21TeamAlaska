from src.User import User
from src.database_access import database_access
from src.helpers import validateMenuInput


class Profile:
    def __init__(self, username: str, title: str, major: str, university_name: str, about_me: str, education: str):
        self.username = username
        self.title = title
        self.major = major
        self.university_name = university_name
        self.about_me = about_me
        self.education = education

    def set_title(self, title: str, db: database_access):
        self.title = title
        sql = 'UPDATE profile SET title = ? WHERE username = ?'
        db.execute(sql, [title, self.username])

    def set_major(self, major: str, db: database_access):
        self.major = major.title()
        sql = 'UPDATE profile SET major = ? WHERE username = ?'
        db.execute(sql, [self.major, self.username])

    def set_university_name(self, university_name: str, db: database_access):
        self.university_name = university_name.title()
        sql = 'UPDATE profile SET university_name = ? WHERE username = ?'
        db.execute(sql, [self.university_name, self.username])

    def set_about_me(self, about_me: str, db: database_access):
        self.about_me = about_me
        sql = 'UPDATE profile SET about_me = ? WHERE username = ?'
        db.execute(sql, [about_me, self.username])

    def set_education(self, education: str, db: database_access):
        self.education = education
        sql = 'UPDATE profile SET education = ? WHERE username = ?'
        db.execute(sql, [education, self.username])

    def isComplete(self) -> bool:
        return (
            self.username != None and
            self.title != None and
            self.major != None and
            self.university_name != None and
            self.about_me != None and
            self.education != None
        )


def getProfile(username: str, db: database_access) -> Profile:
    profileQueryString = '''
    SELECT *
    FROM profile
    WHERE username = ?
    '''
    profileInformation = db.execute(profileQueryString, [username])
    if profileInformation:
        return Profile(
            username,
            profileInformation[0][1],
            profileInformation[0][2],
            profileInformation[0][3],
            profileInformation[0][4],
            profileInformation[0][5],
        )
    else:
        createProfileSQL = '''
        INSERT INTO profile
        VALUES (?,?,?,?,?,?)
        '''
        db.execute(createProfileSQL, [username, None, None, None, None, None])
        return Profile(username, None, None, None, None, None)
