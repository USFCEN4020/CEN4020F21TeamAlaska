import src.Page
import src.database_access
from src.User import *
from Profile.Profile import *
from src.Page import *
import src.helpers


# Does initial setup before any test runs
def setup_module():
    global db
    db = Database("testing.sqlite3")
    src.Page.db = db
    db.delete_profile_table()
    db.delete_users_table()
    db.delete_user_friends()
    db.delete_job_experience_table()
    db.delete_jobs_table()


def resetFunctions():
    src.Page.input = input
    src.Page.print = print


class TestIsPasswordSecure:
    page = src.Page.Page()

    def test_password_character_limit_lower(self):
        assert self.page.is_password_secure("P2$s") == False
        assert self.page.is_password_secure("") == False
        assert self.page.is_password_secure("P2$swor") == False  # 7 chars
        assert self.page.is_password_secure("P2$sword") == True  # 8 chars
        assert self.page.is_password_secure("P2$sword12") == True

    def test_password_character_limit_upper(self):
        assert self.page.is_password_secure("P2$swordTooLong123") == False
        assert self.page.is_password_secure(
            "Pa$sword12345") == False  # 13 chars
        assert self.page.is_password_secure("Pa$sword1234") == True  # 12 chars
        assert self.page.is_password_secure("Pa$sword123") == True

    def test_password_contains_capital(self):
        assert self.page.is_password_secure("password1#") == False
        assert self.page.is_password_secure("Password1#") == True

        assert self.page.is_password_secure("1$c456789") == False
        assert self.page.is_password_secure("A$c456789") == True

    def test_password_contains_lowercase(self):
        assert self.page.is_password_secure("PASSWORD1#") == False
        assert self.page.is_password_secure("PASSWORd1#") == True

        assert self.page.is_password_secure("1$C456789") == False
        assert self.page.is_password_secure("a$C456789") == True

    def test_password_contains_number(self):
        assert self.page.is_password_secure("Password$$") == False
        assert self.page.is_password_secure("Password1$") == True

    def test_password_contains_special(self):
        assert self.page.is_password_secure("Password12") == False
        assert self.page.is_password_secure("Password1#") == True


class TestGetCredentials:
    page = src.Page.Page()

    def testLoginIO(self):
        input_values = ['randion', 'Password#1']
        output = []

        def mock_input(s):
            output.append(s)
            return input_values.pop(0)
        src.Page.input = mock_input
        src.Page.print = lambda s: output.append(s)
        self.page.get_credentials(False)
        resetFunctions()
        assert output == [
            'Enter username: ',
            'Enter password: ',
        ]

    def testRegisterIO(self):
        input_values = ['randion', 'Password#1', 'Robby', 'YbboR']
        output = []

        def mock_input(s):
            output.append(s)
            return input_values.pop(0)
        src.Page.input = mock_input
        src.Page.print = lambda s: output.append(s)
        self.page.get_credentials(True)
        resetFunctions()
        assert output == [
            'Enter username: ',
            'Enter password: ',
            'Enter first name: ',
            'Enter last name: ',
        ]


class TestRegisterLogin:
    page = src.Page.Page()
    db_name = "testing.sqlite3"
    db = src.database_access.database_access(db_name)
    src.Page.db = db

    def testUserRegistration(self):
        input_values = ['randion', 'Password#1', 'Robby', 'Ybbor']
        output = []

        def mock_input(s):
            return input_values.pop(0)
        src.Page.input = mock_input
        src.Page.print = lambda s: output.append(s)
        self.page.register()
        resetFunctions()
        assert output == ["An account for randion was registered successfully"]

    def testUserLoginCorrect(self):
        input_values = ['randion', 'Password#1']
        output = []

        def mock_input(s):
            output.append(s)
            return input_values.pop(0)
        src.Page.input = mock_input
        src.Page.print = lambda s: output.append(s)
        self.page.login()
        resetFunctions()
        assert output == [
            'Enter username: ',
            'Enter password: ',
            "You have successfully logged in\n"
        ]

    def testUserLoginIncorrect(self):
        input_values = ['randion', 'Password#']
        output = []

        def mock_input(s):
            output.append(s)
            return input_values.pop(0)
        src.Page.input = mock_input
        src.Page.print = lambda s: output.append(s)
        self.page.login()
        resetFunctions()
        assert output == [
            'Enter username: ',
            'Enter password: ',
            "Incorrect username / password, please try again\n"
        ]

    def testUserRegistrationLimit(self):
        def mock_input(s):
            return input_values.pop(0)
        src.Page.input = mock_input
        for i in range(0, 11):
            input_values = [
                'randion' + str(i), 'Password#1' + str(i), 'Robby' + str(i), 'Ybbor' + str(i)]
            self.page.register()
        resetFunctions()
        output = []
        input = ['TomSawyer', 'Passworrd#234', 'Tommy', "Sawyer"]

        def mock_input(s):
            output.append(s)
        src.Page.input = mock_input
        src.Page.print = lambda s: output.append(s)
        self.page.register()
        resetFunctions()
        assert output == [
            "All permitted accounts have been created, please come backlater\n"
        ]

    def testDatabaseUserPrint(self):
        output = []
        src.database_access.print = lambda s: output.append(s)
        self.db.print_users()
        src.database_access.print = print
        expected = [("randion", "Password#1", "Robby",
                     "Ybbor", "english", 1, 1, 1)]
        for i in range(0, 9):
            expected.append((
                'randion' + str(i), 'Password#1' + str(i), 'Robby' + str(i), 'Ybbor' + str(i), "english", 1, 1, 1))

        assert output == expected

    def testCleanUp(self):  # Teardown
        self.db.delete_users_table()
        assert True == True


class TestProfileControls:
    def SetUp(self):
        credentials = ("testuser", "Password1!",
                       "Nathan", "Aldino")
        create_user(credentials, db)

    def testProfilePrint(self):
        profile = Profile("testuser", "sir", "general",
                          "university", "i code", "no education")
        getProfile("testuser", db)
        profile.set_title(profile.title, db)
        profile.set_major(profile.major, db)
        profile.set_university_name(profile.university_name, db)
        profile.set_about_me(profile.about_me, db)
        profile.set_education(profile.education, db)
        comparison = getProfile("testuser", db)
        print("\n\n\n\n")
        print(comparison.title)
        assert profile == comparison

    def testJobExperiencePrint(self):
        testjobexp = JobExperience(
            "testuser", "publix1", "publix", "today", "tomrrow", "here", "cashier")
        testjobexp.DbAddJobExperience(db)
        alljobs = getJobInformation("testuser", db)
        assert alljobs[0] == testjobexp

    def testEditIfIncomplete(self):
        unfinishedprofile = Profile(None, None, None, None, None, None)
        unfinishedprofile.set_title("mr", db)
        assert (
            unfinishedprofile.title == "mr" and
            not unfinishedprofile.isComplete()
        )

    def testEditComplete(self):
        unfinishedprofile = Profile("user", None, None, None, None, None)
        unfinishedprofile.set_title("title", db)
        unfinishedprofile.set_major("compsci", db)
        unfinishedprofile.set_university_name("usf", db)
        unfinishedprofile.set_about_me("apple", db)
        unfinishedprofile.set_education("elementary school", db)
        assert unfinishedprofile.isComplete()

    def CleanUp(self):
        db.delete_profile_table()
        db.delete_users_table()
        db.delete_job_experience_table()


class TestNetworkPage:
    page = src.Page.Page()

    def testSetUp(self):
        users = [
            ("darvelo", "Password1!",
                "Daniel", "Arvelo"),
            ("marvelo", "Password1!", "Maniel", "Arvelo"),
            ("rarvelo", "Password1!", "Raniel", "Arvelo")
        ]
        for i in range(len(users)):
            user = create_user(users[i], db)
            if user.username == users[0][0]:
                self.page.user = user
            else:
                # make friends with first user
                sql = '''
        INSERT INTO user_friends VALUES (?,?,?)
        '''
                db.execute(sql, [self.page.user.username,
                                 users[i][0], 'Approved'])
            # Create profiles for all but last user
            if i != len(users) - 1:
                profile = getProfile(users[i][0], db)
                profile.set_about_me("test about me {}".format(i), db)
                profile.set_education("test education {}".format(i), db)
                profile.set_major("test major {}".format(i), db)
                profile.set_title("test title {}".format(i), db)
                profile.set_university_name("test university {}".format(i), db)

    def testMissingProfile(self):
        input_values = ['0']
        output = []

        self.page.user = get_user_by_username("darvelo", db)

        def mock_input(s):
            return input_values.pop(0)
        src.helpers.input = mock_input
        src.Page.print = lambda s: output.append(s)
        self.page.myNetwork_page()
        resetFunctions()
        assert output == [
            "Welcome to the your friends, where you hopefully have some.\n",
            "Select one of the users below to view profile.",
            "1 - marvelo\n2 - Previous Page\nEnter a number: ",
        ]

    def testNoFriends(self):
        input_values = ['0']
        output = []
        credentials = ("garvelo", "Password1!",
                       "Ganiel", "Arvelo")
        self.page.user = create_user(credentials, db)

        def mock_input(s):
            return input_values.pop(0)
        src.helpers.input = mock_input
        src.Page.print = lambda s: output.append(s)
        self.page.myNetwork_page()
        resetFunctions()
        assert output == [
            "Welcome to the your friends, where you hopefully have some.\n",
            "Sorry you have no friends, your mother did warn you.",
            "1 - Previous Page\nEnter a number: "
        ]

class TestFriends:
    page = src.Page.Page()
    
    def testSetup(self):
        self.page.user = create_user(("john","Password1!","John","Smith"),db)
        create_user(("mary","Password1!", "Mary","Smith"),db)
        create_user(("eric","Password1!","eric","smith"),db)
        
        mary = getProfile("mary",db)
        mary.set_about_me("test about me", db)
        mary.set_education("test education", db)
        mary.set_major("test major", db)
        mary.set_title("test title", db)
        mary.set_university_name("university123", db)
        
        eric = getProfile("eric",db)
        eric.set_about_me("test about me", db)
        eric.set_education("test education", db)
        eric.set_major("major123", db)
        eric.set_title("test title", db)
        eric.set_university_name("test university", db)

    #eric sends FR to john and gets accepted by john
    def testPendingRequest(self):
        db.execute('''INSERT INTO user_friends VALUES (?,?,?)''', ['eric', self.page.user.username , 'Pending'])
        input = ["1"]
        output = []
        def mock_input(s):
            return input.pop(0)
        src.Page.input = mock_input
        src.Page.print = lambda s: output.append(s)
        self.page.pendingFriendRequests(db)
        resetFunctions()
        assert output == [
            "Friend request from eric. Enter 1 to accept or 2 to decline.\n",
            "Successfully saved your changes!\n"
        ]
    
    #searching for mary via university
    def testSearchUni(self):
        input = ["university123","1"]
        output = []
        def mock_input(s):
            return input.pop(0)
        src.Page.input = mock_input
        src.Page.print = lambda s: output.append(s)
        self.page.searchByUniversity()
        resetFunctions()
        assert output == ['Results:\n', '1:  Username: mary Firstname: Mary Lastname: Smith', 'Friend Request Sent']
    
    # searching for mary via major
    def testSearchMajor(self):
        input = ["major123","1"]
        output = []
        def mock_input(s):
            return input.pop(0)
        src.Page.input = mock_input
        src.Page.print = lambda s: output.append(s)
        self.page.searchByMajor()
        resetFunctions()
        assert output == ['Results:\n', '1:  Username: eric Firstname: eric Lastname: smith', 'Friend Request Sent']

    def delete_users(self):
        db.execute('''INSERT INTO user_friends VALUES (?,?,?)''', ['dana', self.page.user.username , 'Pending'])
        self.page.delete_friend('dana', db)
        sql_for_all_friends = '''
        SELECT * FROM user_friends WHERE (username1 = ? AND username2 = ?) OR (username1 = ? AND username2 = ?)
        '''
        res = db.execute(sql_for_all_friends, [self.user.username, 'dana', 'dana', self.user.username])
        assert res is None


# Runs after every test in this file has finished running
def teardown_module():
    db = Database('testing.sqlite3')
    db.delete_profile_table()
    db.delete_users_table()
    db.delete_user_friends()
    db.delete_job_experience_table()
    db.delete_jobs_table()
    db.close()
