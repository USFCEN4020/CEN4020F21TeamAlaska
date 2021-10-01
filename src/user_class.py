from enum import Enum
import enum
import re
from src.database_access import database_access as Database
from src.User import *
db = Database("InCollege.sqlite3")


# class to store a job
class PostedJob():
    def __init__(name, title, description, employer, location, salary):
        name = name
        title = title
        description = description
        employer = employer
        location = location
        salary = salary


class Page:
    # each page will "render" the appropriate "form" or prompt
    def __init__(self):
        # current login info
        self.user = User("", "", "", "", "english",
                         True, True, True, False, db)
        # stack is to implement the navigation functionality
        self.page_stack = []
        # Numbered pages so they're easily added to the stack and then called
        self.index = {
            0: {
                "view": self.home_page
            },
            1: {
                "view": self.play_video
            },
            2: {
                "view": self.find_people
            },
            3: {
                "view": self.register_page
            },
            4: {
                "view": self.login_page
            },
            5: {
                "view": self.post_job_page
            },
            6: {
                "view": self.skills_page
            }
        }

    def home_page(self):
        self.page_stack.append(0)
        # I want the home page to view different option depending on whether or not the user is authenticated
        if not self.user.authorized:
            c = int(input("Welcome to InCollege: *** Where you're no longer going to be broke ***\nAll of our broke students managed to find job!!!\n\n1 - Play Video\n2 - People you may know\n3 - Register\n4 - Login\nEnter a choice: "))
            if c == 1:
                self.play_video()
            if c == 2:
                self.find_people()
            if c == 3:
                self.register_page()
            if c == 4:
                self.login_page()
        else:
            c = int(input(
                "1 - Search for a job\n2 - Find people you may know\n3 - learn a new skill\nEnter a choice: "))
            if c == 1:
                self.post_job_page()
            if c == 2:
                self.find_people()
            if c == 3:
                self.skills_page()

    def play_video(self):
        self.page_stack.append(1)
        print("Video is now playing...")
        # back_option prompts the user to enter 0 if they wanna go back
        self.back_option()

    def login_page(self):
        self.page_stack.append(4)
        res = self.login()
        if res:
            self.user.authorize()
        # Once the user logs in, they get redirected to the home page
        self.home_page()

    def register_page(self):
        self.page_stack.append(3)
        res = self.register()
        if res:
            # the user is now authenticated, they'll view things slightly different
            self.user.authorize()
        # Once the user logs in, they get redirected to the home page
        self.home_page()

    def find_people(self):
        self.page_stack.append(2)
        fname = input("Enter your friend's firstname: ")
        lname = input("Enter your friend's lastname: ")
        find_friend = (
            'SELECT * FROM users WHERE firstname = ? AND lastname = ?')
        # the friend input is searched for in the db
        res = db.execute(find_friend, (fname, lname))
        # if the friend exits in our database
        if res:
            print("They are a part of the InCollege system")
            # if the user hasn't logged in, they'll view the below options
            if not self.user.authorized:
                c = int(
                    input("Would you like to join?\n1-Regiser\n2-Login\n0 - To go back: "))
                if c == 1:
                    self.register_page()
                elif c == 2:
                    self.login_page()
                elif c == 0:
                    self.back_page()
        else:
            # your friend is imaginary and doesn't exist
            print("They are not yet a part of the InCollege system yet")
            self.back_option()

    # function to post a job to the database, returns true if successful, false otherwise
    def postjob(self):
        # check if there are more than 5 jobs
        numjobs = len(db.execute('SELECT * FROM jobs'))
        if(numjobs >= 5):
            print("There are already 5 jobs. Please try again later\n")
            return False

        else:
            temp = PostedJob
            temp.name = self.user.username
            temp.title = input("Please enter the job's title: ")
            temp.description = input("Please enter a description of the job: ")
            temp.employer = input("Who is the employer of the job? ")
            temp.location = input("Where is this job located? ")
            while True:
                try:
                    temp.salary = float(
                        input("Please estimate the salary of the job (only numbers): "))
                    break
                except Exception:
                    print("Not a valid number. Try again.")

            # insert object member values into database
            db.execute('INSERT INTO jobs VALUES (?, ?, ?, ?, ?, ?)', [
                       temp.name, temp.title, temp.description, temp.employer, temp.location, temp.salary])

            print("Thanks your job was posted! Returning to the previous menu...")
            return True

    def post_job_page(self):
        self.page_stack.append(5)
        if self.user.authorized:
            self.postjob()
            # this is to go back a level
            self.back_option()

    def skills_page(self):
        self.page_stack.append(6)
        skill = input(
            '\n1 - JavaScript\n2 - Python\n3 - SQL Sever\n4 - MongoDB\n5 - Design Patterns\nEnter a choice: ')
        if skill:
            print('under construction')
        self.back_option()

    # goes up a level to the previous page
    def back_page(self):
        # call the function for the previous page
        self.page_stack.pop()
        prev = self.page_stack[-1]
        self.index[prev]['view']()

    def back_option(self):
        c = input("0 - To go back: ")
        if c == '0':
            self.back_page()

    ################ OLD FUNCTIONS ##############
    def get_credentials(self, register: False):
        # returns the credentials. Called either in login() or register()
        user = input('Enter username: ')
        password = input('Enter password: ')
        if register:
            firstname = input("Enter first name: ")
            lastname = input("Enter last name: ")
            return (user, password, firstname, lastname)
        return (user, password)

    def login(self):
        while True:
            cred = self.get_credentials(False)
            # checks if the credentials exist in the users table
            user = get_user_by_login(cred[0], cred[1], db)
            if user:
                self.user = user
                print('You have successfully logged in\n')
                return True
            else:
                print('Incorrect username / password, please try again\n')
                return False

    def register(self):
        # checking the number of accounts already registered
        num_accounts = len(db.execute('SELECT * FROM users'))
        if int(num_accounts) >= 5:
            print("All permitted accounts have been created, please come backlater\n")
        else:
            # if a new user is allowed to register, it prompts them to enter credentials
            cred = self.get_credentials(True)
            # the below function returns a boolean as to whether or not the password is secure
            satisfies = self.is_password_secure(cred[1])
            if satisfies:
                # posting data to the database
                self.user = create_user(cred, db)
                print("An account for " +
                      cred[0] + " was registered successfully")
                return True
            else:
                print('Weak Password')
                return False

    def is_password_secure(self, pw):
        reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%^()*#?&])[A-Za-z\d@$!#%^()*?&]{8,12}$"
        pattern = re.compile(reg)
        res = re.match(pattern, pw)
        return res != None
