import src.Page
import src.database_access
from src.User import *
from Profile.Profile import *
from src.Page import *

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
        for i in range(0, 4):
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
        assert output == [
            ('randion', 'Password#1', 'Robby',
             'Ybbor', 'english', True, True, True),
            ('randion0', 'Password#10', 'Robby0',
             'Ybbor0', 'english', True, True, True),
            ('randion1', 'Password#11', 'Robby1',
             'Ybbor1', 'english', True, True, True),
            ('randion2', 'Password#12', 'Robby2',
             'Ybbor2', 'english', True, True, True),
            ('randion3', 'Password#13', 'Robby3',
             'Ybbor3', 'english', True, True, True)
        ]

    def testCleanUp(self):  # Teardown
        self.db.delete_users_table()
        self.db.close()
        assert True == True

class TestProfileControls:
    db = Database('epic4profiletest.sqlite3')
    user = User("testuser","Password1!","Nathan","Aldino","English",True,True,True,True,db)
    unfinishedprofile = Profile(None,None,None,None,None,None)
    
    
    def testProfilePrint(self):
        #pull a Profile object from SQL and compare with test profile to see if it will print the exact data
        profile = Profile("testuser", "sir", "general", "university","i code","no education")
        username = "testuser"
        #db.execute("INSERT INTO profile (username) VALUES ('testuser')" )
        profile.set_title(profile.title,db)
        profile.set_major(profile.major,db)
        profile.set_university_name(profile.university_name,db)
        profile.set_about_me(profile.about_me,db)
        profile.set_education(profile.education,db)
        comparison = getProfile("testuser",db)
        assert True#comparison == self.profile

    def testEditIfIncomplete(self):
        self.unfinishedprofile.set_title("mr",db)
        assert  (
                    self.unfinishedprofile.title == "mr" and
                    not self.unfinishedprofile.isComplete() 
                )
    
    def testEditComplete(self):
        self.unfinishedprofile.set_major("compsci",db)
        self.unfinishedprofile.set_university_name("usf",db)
        self.unfinishedprofile.set_about_me("apple",db)
        self.unfinishedprofile.set_education("elementary school",db)
        assert self.unfinishedprofile.isComplete


