import pytest
import src.user_class
import src.database_access


def resetFunctions():
    src.user_class.input = input
    src.user_class.print = print


class TestIsPasswordSecure:
    page = src.user_class.Page()

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
    page = src.user_class.Page()

    def testLoginIO(self):
        input_values = ['randion', 'Password#1']
        output = []

        def mock_input(s):
            output.append(s)
            return input_values.pop(0)
        src.user_class.input = mock_input
        src.user_class.print = lambda s: output.append(s)
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
        src.user_class.input = mock_input
        src.user_class.print = lambda s: output.append(s)
        self.page.get_credentials(True)
        resetFunctions()
        assert output == [
            'Enter username: ',
            'Enter password: ',
            'Enter first name: ',
            'Enter last name: ',
        ]


class TestRegisterLogin:
    page = src.user_class.Page()
    db_name = "testing.sqlite3"
    db = src.database_access.database_access(db_name)
    src.user_class.db = db

    def testUserRegistration(self):
        input_values = ['randion', 'Password#1', 'Robby', 'Ybbor']
        output = []

        def mock_input(s):
            return input_values.pop(0)
        src.user_class.input = mock_input
        src.user_class.print = lambda s: output.append(s)
        self.page.register()
        resetFunctions()
        assert output == ["An account for randion was registered successfully"]

    def testUserLoginCorrect(self):
        input_values = ['randion', 'Password#1']
        output = []

        def mock_input(s):
            output.append(s)
            return input_values.pop(0)
        src.user_class.input = mock_input
        src.user_class.print = lambda s: output.append(s)
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
        src.user_class.input = mock_input
        src.user_class.print = lambda s: output.append(s)
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
        src.user_class.input = mock_input
        for i in range(0, 4):
            input_values = [
                'randion' + str(i), 'Password#1' + str(i), 'Robby' + str(i), 'Ybbor' + str(i)]
            self.page.register()
        resetFunctions()
        output = []
        input = ['TomSawyer', 'Passworrd#234', 'Tommy', "Sawyer"]

        def mock_input(s):
            output.append(s)
        src.user_class.input = mock_input
        src.user_class.print = lambda s: output.append(s)
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
            ('randion', 'Password#1', 'Robby', 'Ybbor'),
            ('randion0', 'Password#10', 'Robby0', 'Ybbor0'),
            ('randion1', 'Password#11', 'Robby1', 'Ybbor1'),
            ('randion2', 'Password#12', 'Robby2', 'Ybbor2'),
            ('randion3', 'Password#13', 'Robby3', 'Ybbor3')
        ]

    def testCleanUp(self):  # Teardown
        self.db.delete_users_table()
        self.db.close()
        assert True == True


class TestJobPosting():
    page = src.user_class.Page()
    page.user.username = "General Kenobi The Negotiator"
    db_name = "testing.sqlite3"
    db = src.database_access.database_access(db_name)
    src.user_class.db = db

    def testPostValidJob(self):
        input_values = ['Worm Farmer', 'Farming worms',
                        'WormsRUs', 'Bikini Bottom', '20000']
        output = []

        def mock_input(s):
            return input_values.pop(0)
        src.user_class.input = mock_input
        src.user_class.print = lambda s: output.append(s)
        self.page.postjob()
        resetFunctions()
        assert output == [
            "Thanks your job was posted! Returning to the previous menu..."
        ]

    def testPostInvalidJob(self):
        input_values = ['Worm Farmer0', 'Farming worms',
                        'WormsRUs', 'Bikini Bottom', 'Shmeckle', '20000']
        output = []

        def mock_input(s):
            output.append(s)
            return input_values.pop(0)
        src.user_class.input = mock_input
        src.user_class.print = lambda s: output.append(s)
        self.page.postjob()
        resetFunctions()
        assert output == [
            "Please enter the job's title: ",
            "Please enter a description of the job: ",
            "Who is the employer of the job? ",
            "Where is this job located? ",
            "Please estimate the salary of the job (only numbers): ",
            "Not a valid number. Try again.",
            "Please estimate the salary of the job (only numbers): ",
            "Thanks your job was posted! Returning to the previous menu..."
        ]

    def testJobPostLimit(self):
        for i in range(1, 4):
            input_values = [
                'Worm Farmer' + str(i), 'Farming worms', 'WormsRUs', 'Bikini Bottom', '20000']

            def mock_input(s):
                return input_values.pop(0)
            src.user_class.input = mock_input
            self.page.postjob()
        output = []
        input_values = ['Not going to post', 'Farming worms',
                        'WormsRUs', 'Bikini Bottom', '20000']

        def mock_input(s):
            return input_values.pop(0)
        src.user_class.input = mock_input
        src.user_class.print = lambda s: output.append(s)
        self.page.postjob()
        resetFunctions()
        assert output == [
            'There are already 5 jobs. Please try again later\n'
        ]

    def testDatabaseJobPrint(self):
        output = []
        src.database_access.print = lambda s: output.append(s)
        self.db.print_jobs()
        assert output == [('General Kenobi The Negotiator', 'Worm Farmer', 'Farming worms', 'WormsRUs', 'Bikini Bottom', 20000.0), ('General Kenobi The Negotiator', 'Worm Farmer0', 'Farming worms', 'WormsRUs', 'Bikini Bottom', 20000.0), ('General Kenobi The Negotiator', 'Worm Farmer1',
                                                                                                                                                                                                                                              'Farming worms', 'WormsRUs', 'Bikini Bottom', 20000.0), ('General Kenobi The Negotiator', 'Worm Farmer2', 'Farming worms', 'WormsRUs', 'Bikini Bottom', 20000.0), ('General Kenobi The Negotiator', 'Worm Farmer3', 'Farming worms', 'WormsRUs', 'Bikini Bottom', 20000.0)]
        src.database_access.print

    def testCleanUp(self):  # Teardown
        self.db.delete_jobs_table()
        self.db.close()
        assert True == True
