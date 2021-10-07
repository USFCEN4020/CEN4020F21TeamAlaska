from src.User import User
from src.database_access import database_access


class Profile:
    def __init__(self, username: str, title: str, major: str, university_name: str, about_me: str, education: str):
        self.username = username,
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
        return Profile("", "", "", "", "", "")


# Requires Database and User object, will print out full profile.
def printUserProfile(user: User, db: database_access):
    jobQueryString = '''
    SELECT *
    FROM job_experience
    WHERE username = ?
    '''
    profileInformation = getProfile(user.username, db)
    jobInformation = db.execute(jobQueryString, [user.username])
    if len(profileInformation) < 1:
        return -1

    print_queue = []
    print_queue.append(user.firstname + ' ' + user.lastname + '\'s Profile')
    print_queue.append('Title: ' + profileInformation.title)
    print_queue.append('Major: ' + profileInformation.major)
    print_queue.append('University: ' + profileInformation.university_name)
    print_queue.append('Information and Education\n' +
                       profileInformation.about_me + ' ' + profileInformation.education)

    if len(jobInformation) > 0:
        print_queue.append('Job Experience')
        for job in jobInformation:
            print_queue.append('Title: ' + job[0])
            print_queue.append('Employer: ' + job[1])
            print_queue.append('Date Started: ' + job[2])
            print_queue.append('Date Ended: ' + job[3])
            print_queue.append("Location: " + job[4])
            print_queue.append('Job Description: \n' + job[5])

    for item in print_queue:
        print(item + '\n')
