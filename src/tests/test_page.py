import datetime

import src.Page
import src.database_access
from src.User import *
from Profile.Profile import *
from src.Page import *
import src.helpers
import src.Job
from src.Course import Course


# Does initial setup before any test runs
def setup_module():
    global db
    db = Database("testing.sqlite3")
    src.Page.db = db
    db.delete_profile_table()
    db.delete_users_table()
    db.delete_user_friends()
    db.delete_job_experience_table()
    db.delete_user_interested()
    db.delete_user_applied()
    db.delete_notifications()
    db.delete_courses()


def resetFunctions():
    src.Page.input = input
    src.Page.print = print
    src.helpers.input = input


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
        input_values = ['randion', 'Password#1', 'Robby', 'YbboR', '1']
        output = []

        def mock_input(s):
            output.append(s)
            return input_values.pop(0)
        src.helpers.input = mock_input
        src.Page.input = mock_input
        src.Page.print = lambda s: output.append(s)
        self.page.get_credentials(True)
        resetFunctions()
        assert output == [
            'Enter username: ',
            'Enter password: ',
            'Enter first name: ',
            'Enter last name: ',
            '1- Standard Tier\n2- Plus Tier\nEnter a choice: ',
            ''
        ]


class TestRegisterLogin:
    page = src.Page.Page()
    db_name = "testing.sqlite3"
    db = src.database_access.database_access(db_name)
    src.Page.db = db

    def testUserRegistration(self):
        input_values = ['randion', 'Password#1', 'Robby', 'Ybbor', '1']
        output = []

        def mock_input(s):
            return input_values.pop(0)
        src.Page.input = mock_input
        src.helpers.input = mock_input
        src.Page.print = lambda s: output.append(s)
        self.page.register()
        resetFunctions()
        print(output)
        assert output == ['1- Standard Tier\n2- Plus Tier\nEnter a choice: ',
                          'An account for randion was registered successfully']

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
            "You have successfully logged in\n",
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
        src.helpers.input = mock_input
        for i in range(0, 11):
            input_values = [
                'randion' + str(i), 'Password#1' + str(i), 'Robby' + str(i), 'Ybbor' + str(i), '1']
            self.page.register()
        resetFunctions()
        output = []
        input = ['TomSawyer', 'Passworrd#234', 'Tommy', "Sawyer", '2']

        def mock_input(s):
            output.append(s)
        src.Page.input = mock_input
        src.helpers.input = mock_input
        src.Page.print = lambda s: output.append(s)
        self.page.register()
        resetFunctions()
        assert output == [
            "All permitted accounts have been created, please come backlater\n"
        ]

    # def testDatabaseUserPrint(self):
    #     output = []
    #     src.database_access.print = lambda s: output.append(s)
    #     self.db.print_users()
    #     src.database_access.print = print
    #     expected = [("randion", "Password#1", "Robby",
    #                  "Ybbor", "standard", "english", 1, 1, 1)]
    #     for i in range(0, 9):
    #         expected.append((
    #             'randion' + str(i), 'Password#1' + str(i), 'Robby' + str(i), 'Ybbor' + str(i), "standard", "english", 1, 1, 1))

    #     assert output == expected

    def testCleanUp(self):  # Teardown
        self.db.delete_users_table()
        assert True == True


class TestProfileControls:
    def SetUp(self):
        credentials = ("testuser", "Password1!",
                       "Nathan", "Aldino", "standard")
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
                "Daniel", "Arvelo", "Standard"),
            ("marvelo", "Password1!", "Maniel", "Arvelo", "standard"),
            ("rarvelo", "Password1!", "Raniel", "Arvelo", "standard")
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
            "These are your friends:\n1 - marvelo\n2 - rarvelo\n",
            "Select one of the users below to view profile.",
            "1 - marvelo\n2 - Previous Page\nEnter a number: ",
        ]

    def testNoFriends(self):
        input_values = ['0']
        output = []
        credentials = ("garvelo", "Password1!",
                       "Ganiel", "Arvelo", "plus")
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
            "Select one of the options below: ",
            "1 - Previous Page\nEnter a number: "
        ]


class TestFriends:
    page = src.Page.Page()

    def testSetup(self):
        self.page.user = create_user(
            ("john", "Password1!", "John", "Smith", "standard"), db)
        create_user(("mary", "Password1!", "Mary", "Smith", "standard"), db)
        create_user(("eric", "Password1!", "eric", "smith", "standard"), db)

        mary = getProfile("mary", db)
        mary.set_about_me("test about me", db)
        mary.set_education("test education", db)
        mary.set_major("test major", db)
        mary.set_title("test title", db)
        mary.set_university_name("university123", db)

        eric = getProfile("eric", db)
        eric.set_about_me("test about me", db)
        eric.set_education("test education", db)
        eric.set_major("major123", db)
        eric.set_title("test title", db)
        eric.set_university_name("test university", db)

    # eric sends FR to john and gets accepted by john
    def testPendingRequest(self):
        db.execute('''INSERT INTO user_friends VALUES (?,?,?)''',
                   ['eric', self.page.user.username, 'Pending'])
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

    # searching for mary via university
    def testSearchUni(self):
        input = ["university123", "1"]
        output = []

        def mock_input(s):
            return input.pop(0)
        src.Page.input = mock_input
        src.Page.print = lambda s: output.append(s)
        self.page.searchByUniversity()
        resetFunctions()
        assert output == [
            'Results:\n', '1:  Username: mary Firstname: Mary Lastname: Smith', 'Friend Request Sent']

    # searching for mary via major
    def testSearchMajor(self):
        input = ["major123", "1"]
        output = []

        def mock_input(s):
            return input.pop(0)
        src.Page.input = mock_input
        src.Page.print = lambda s: output.append(s)
        self.page.searchByMajor()
        resetFunctions()
        assert output == [
            'Results:\n', '1:  Username: eric Firstname: eric Lastname: smith', 'Friend Request Sent']

    def delete_users(self):
        db.execute('''INSERT INTO user_friends VALUES (?,?,?)''',
                   ['dana', self.page.user.username, 'Pending'])
        self.page.delete_friend('dana', db)
        sql_for_all_friends = '''
        SELECT * FROM user_friends WHERE (username1 = ? AND username2 = ?) OR (username1 = ? AND username2 = ?)
        '''
        res = db.execute(sql_for_all_friends, [
                         self.user.username, 'dana', 'dana', self.user.username])
        assert res is None


class TestJobPages:
    page = src.Page.Page()
    page.user = User("darvelo", "", "", "", "standard", "", "",
                     "", "", datetime.datetime.now(), True, db)

    def test_job_page_view_job_no_jobs(self):
        input_Page = ['1']
        input_helpers = ['2']
        output = []

        def mock_input_Page(s):
            return input_Page.pop(0)
        src.Page.input = mock_input_Page

        def mock_input_helpers(s):
            return input_helpers.pop(0)
        src.helpers.input = mock_input_helpers

        src.Page.print = lambda s: output.append(s)

        self.page.post_job_page()

        assert output == [
            "You have currently applied for 0 jobs",
            '1 - Post a New Job\n2 - View Jobs\n3 - My Postings\n4 - View applications\n5 - View interested\n6 - Previous page\nEnter a choice: ',
            "sorry, no jobs for you"
        ]

    def test_job_page_view_job(self):
        # -- Setup - create jobs, users --
        input_Page = ['Worm Farmer', 'Farming worms',
                      'WormsRUs', 'Bikini Bottom', '20000']
        output = []

        def mock_input_Page(s):
            return input_Page.pop(0)
        src.Page.input = mock_input_Page

        def mock_input_helpers(s):
            return input_helpers.pop(0)
        src.helpers.input = mock_input_helpers

        self.page.postjob()

        input_Page = ['Worm Farmer 2', 'Farming worms 2',
                      'WormsRUs 2', 'Bikini Bottom 2', '20000']
        self.page.postjob()

        # -- end setup --
        input_Page = ['1', '-1', '-1']
        input_helpers = ['2']

        src.Page.print = lambda s: output.append(s)

        self.page.post_job_page()

        resetFunctions()

        assert output == [
            "You have currently applied for 0 jobs",
            '1 - Post a New Job\n2 - View Jobs\n3 - My Postings\n4 - View applications\n5 - View interested\n6 - Previous page\nEnter a choice: ',
            "Available Jobs:",
            "1 - Worm Farmer",
            "2 - Worm Farmer 2"
        ]
        # -- TEST Job does not exist --
        input_Page = ['-1', '1']
        input_helpers = ['2']
        output = []
        src.Page.input = mock_input_Page
        src.helpers.input = mock_input_helpers
        src.Page.print = lambda s: output.append(s)

        self.page.post_job_page()
        resetFunctions()

        assert output == [
            "You have currently applied for 0 jobs",
            '1 - Post a New Job\n2 - View Jobs\n3 - My Postings\n4 - View applications\n5 - View interested\n6 - Previous page\nEnter a choice: ',
            "Available Jobs:",
            "1 - Worm Farmer",
            "2 - Worm Farmer 2",
            "Job does not exist"
        ]

    def test_job_page_view_my_postings(self):
        # -- Setup --

        def mock_input_Page(s):
            return input_Page.pop(0)
        src.Page.input = mock_input_Page

        def mock_input_helpers(s):
            return input_helpers.pop(0)
        src.helpers.input = mock_input_helpers

        # -- end setup --
        input_Page = ['0']
        input_helpers = ['3', '2']
        output = []

        src.Page.print = lambda s: output.append(s)

        self.page.post_job_page()

        assert output == [
            "You have currently applied for 0 jobs",
            '1 - Post a New Job\n2 - View Jobs\n3 - My Postings\n4 - View applications\n5 - View interested\n6 - Previous page\nEnter a choice: ',
            '\nMy Postings:',
            'Job ID: 1, Title: Worm Farmer',
            'Job ID: 2, Title: Worm Farmer 2',
            '\n1 - Delete Job\n2 - Previous page\nEnter a choice: ',
        ]

    def test_view_applications(self):
        # -- Setup --
        def mock_input_helpers(s):
            return input_helpers.pop(0)
        src.helpers.input = mock_input_helpers

        src.Job.Job.apply_job("darvelo", 1, "some reason", db)

        # -- end setup --
        input_helpers = ['4']
        output = []

        src.Page.print = lambda s: output.append(s)

        self.page.post_job_page()

        resetFunctions()

        assert output == [
            "You have currently applied for 1 jobs",
            '1 - Post a New Job\n2 - View Jobs\n3 - My Postings\n4 - View applications\n5 - View interested\n6 - Previous page\nEnter a choice: ',
            '\n',
            '\n',
        ]

    def test_view_interested_none(self):
        # -- Setup --
        def mock_input_helpers(s):
            return input_helpers.pop(0)
        src.helpers.input = mock_input_helpers

        # -- end setup --
        input_helpers = ['5']
        output = []

        src.Page.print = lambda s: output.append(s)

        self.page.post_job_page()

        resetFunctions()

        assert output == [
            "You have currently applied for 1 jobs",
            '1 - Post a New Job\n2 - View Jobs\n3 - My Postings\n4 - View applications\n5 - View interested\n6 - Previous page\nEnter a choice: ',
            "You are not interested in any jobs currently.\n"
        ]

    def test_view_interested(self):
        # -- Setup --
        def mock_input_helpers(s):
            return input_helpers.pop(0)
        src.helpers.input = mock_input_helpers

        src.Job.Job.add_interested("darvelo", 2, db)

        # -- end setup --
        input_helpers = ['5']
        output = []

        src.Page.print = lambda s: output.append(s)

        self.page.post_job_page()

        resetFunctions()

        assert output == [
            "You have currently applied for 1 jobs",
            '1 - Post a New Job\n2 - View Jobs\n3 - My Postings\n4 - View applications\n5 - View interested\n6 - Previous page\nEnter a choice: ',
        ]

    def test_job_page_delete_posting(self):
        # -- Setup --
        def mock_input_Page(s):
            return input_Page.pop(0)
        src.Page.input = mock_input_Page

        def mock_input_helpers(s):
            return input_helpers.pop(0)
        src.helpers.input = mock_input_helpers

        # -- end setup --
        input_Page = ['0']
        input_helpers = ['3', '1', '1']
        output = []

        src.Page.print = lambda s: output.append(s)

        self.page.post_job_page()

        resetFunctions()

        assert output == [
            "You have currently applied for 1 jobs",
            '1 - Post a New Job\n2 - View Jobs\n3 - My Postings\n4 - View applications\n5 - View interested\n6 - Previous page\nEnter a choice: ',
            '\nMy Postings:',
            'Job ID: 1, Title: Worm Farmer',
            'Job ID: 2, Title: Worm Farmer 2',
            '\n1 - Delete Job\n2 - Previous page\nEnter a choice: ',
            'Enter the Job ID to Delete: ',
            'Job successfully deleted'
        ]

    def test_job_page_view_my_postings_Zero(self):
        # -- Setup --
        self.page.user = User("NonExistentUser", "", "",
                              "", "", "", "", "", "", None, True, db)

        def mock_input_Page(s):
            return input_Page.pop(0)
        src.Page.input = mock_input_Page

        def mock_input_helpers(s):
            return input_helpers.pop(0)
        src.helpers.input = mock_input_helpers

        # -- end setup --
        input_Page = ['0']
        input_helpers = ['3']
        output = []

        src.Page.print = lambda s: output.append(s)

        self.page.post_job_page()

        resetFunctions()
        assert output == [
            "You have currently applied for 0 jobs",
            '1 - Post a New Job\n2 - View Jobs\n3 - My Postings\n4 - View applications\n5 - View interested\n6 - Previous page\nEnter a choice: ',
            "You don't have any postings at the moment",
        ]


class TestTrainingPage:
    page = src.Page.Page()

    def trainingandeducation(self):
        input = ['1']
        output = []

        def mock_input(s):
            return input.pop(0)
        src.Page.input = mock_input
        src.page.print = lambda s: output.append(s)
        self.page.training_page
        resetFunctions()
        assert output == [
            "1 - Training and Education\n2 - IT Help Desk\n3 - Business Analysis and Strategy\n4 - Security\n5 - Go back",
            "1 - Learn Python\n2 - Learn React\n3 - Public Speaking 101\n4 - SCRUM basics",
            "Under Construction."
        ]

    def ITandsecurity(self):
        input = ['2']
        output = []

        def mock_input(s):
            return input.pop(0)
        src.Page.input = mock_input
        src.page.print = lambda s: output.append(s)
        self.page.training_page
        resetFunctions()
        assert output == [
            "1 - Training and Education\n2 - IT Help Desk\n3 - Business Analysis and Strategy\n4 - Security\n5 - Go back",
            "Coming soon!"
        ]

    def business(self):
        input = ['3', '4']
        output = []

        def mock_input(s):
            return input.pop(0)
        src.Page.input = mock_input
        src.page.print = lambda s: output.append(s)
        self.page.training_page
        resetFunctions()
        assert output == [
            "1 - Training and Education\n2 - IT Help Desk\n3 - Business Analysis and Strategy\n4 - Security\n5 - Go back",
            "1 - How to use InCollege learning\n2 - Train the trainer\n3 - Gamification of learning\n4 - Not seeing what you're looking for? Sign in to see all 7,609 results.",
            'Enter username: ',
        ]

    def incollegetraining(self):
        input = []
        output = []

        def mock_input(s):
            return input.pop(0)
        src.Page.input = mock_input
        src.page.print = lambda s: output.append(s)
        self.page.in_college_learning_page
        resetFunctions()
        assert output == [
            "Pick any of the courses below to enroll:\n",
            "1 - How to use InCollege learning\n2 - Train the trainer\n3 - Gamification of learning\n4 - Understanding the Architectural Design Process\n5 - Project Management Simplified\n6 - Go Back"
        ]

    def test_add_courses(self):
        Course.setCourseStatus(self.page.user.username,
                               "Software Dev", False, db)
        queryString = "SELECT * FROM student_courses WHERE username = ? AND title = ?"
        res = db.execute(
            queryString, [self.page.user.username, "Software Dev"])
        assert len(res) > 0

    def test_update_status(self):
        Course.setCourseStatus(self.page.user.username,
                               "Software Engineer", False, db)
        Course.setCourseStatus(self.page.user.username,
                               "Software Engineer", True, db)
        queryString = "SELECT * FROM student_courses WHERE username = ? AND title = ?"
        res = db.execute(
            queryString, [self.page.user.username, "Software Engineer"])
        assert res[0][2] == True

# Runs after every test in this file has finished running


def teardown_module():
    db = Database('testing.sqlite3')
    db.delete_profile_table()
    db.delete_users_table()
    db.delete_user_friends()
    db.delete_job_experience_table()
    db.delete_jobs_table()
    db.delete_user_applied()
    db.delete_user_interested()
    db.delete_notifications()
    db.close()
