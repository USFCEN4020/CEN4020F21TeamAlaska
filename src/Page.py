import re
from src.database_access import database_access as Database
from src.JobExperience import *
from src.User import *
from src.PostedJob import PostedJob
from Profile.Profile import *
from src.helpers import validateMenuInput
db = Database("InCollege.sqlite3")


class Page:
    # each page will "render" the appropriate "form" or prompt
    def __init__(self):
        # current login info
        self.user = User("", "", "", "", "english",
                         True, True, True, False, db)
        # stack is to implement the navigation functionality
        self.page_stack = [0]
        # Numbered pages so they're easily added to the stack and then called
        self.index = {
            0: {
                "view": self.home_page
            },
            1: {
                "view": self.play_video_page
            },
            2: {
                "view": self.find_people_page
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
            },
            7: {
                "view": self.useful_links_page
            },
            8: {
                "view": self.general_page
            },
            9: {
                "view": self.important_links_page
            },
            10: {
                "view": self.privacy_page
            },
            11: {
                "view": self.guest_controls_page
            },
            12: {
                "view": self.language_page
            },
            13: {
                "view": self.option_switch_page
            },
            14: {
                "view": self.printUserProfile
            },
            15: {
                "view": self.editProfilePage
            },
            16: {
                "view": self.add_friend_page
            },
            17: {
                "view": self.myNetwork_page
            }
        }

    def home_page(self):
        # I want the home page to view different option depending on whether or not the user is authenticated
        if not self.user.authorized:
            c = -1
            print("Welcome to InCollege: *** Where you're no longer going to be broke ***\nAll of our broke students managed to find job!!!"
                  "\n\n1 - Play Video\n2 - People you may know\n3 - Register\n4 - Login\n5 - Useful Links\n6 - InCollege Important Links\n7 - Exit\nEnter a choice: ")
            c = validateMenuInput(7)
            if c == 1:
                self.page_stack.append(1)
                self.play_video_page()
            if c == 2:
                self.page_stack.append(2)
                self.find_people_page()
            if c == 3:
                self.page_stack.append(3)
                self.register_page()
            if c == 4:
                self.page_stack.append(4)
                self.login_page()
            if c == 5:
                self.page_stack.append(7)
                self.useful_links_page()
            if c == 6:
                self.page_stack.append(9)
                self.important_links_page()
            if c == 7:
                print("Thank you for using InCollege!")
                return 0
        else:
            # Preliminary pending friend request check, not a page.
            self.pendingFriendRequests(db)
            c = -1
            print(
                "1 - Search for a job\n2 - Find people you may know\n3 - learn a new skill\n4 - Useful Links\n5 - InCollege Important Links\n6 - Profile\n7 - Add Friend\n8 - Network\n9 - Exit\nEnter a choice: ")
            c = validateMenuInput(9)
            if c == 1:
                self.page_stack.append(5)
                self.post_job_page()
            if c == 2:
                self.page_stack.append(2)
                self.find_people_page()
            if c == 3:
                self.page_stack.append(6)
                self.skills_page()
            if c == 4:
                self.page_stack.append(7)
                self.useful_links_page()
            if c == 5:
                self.page_stack.append(9)
                self.important_links_page()
            if c == 6:
                self.page_stack.append(14)
                self.printUserProfile(self.user, db)
            if c == 7:
                self.page_stack.append(16)
                self.add_friend_page(db)
            if c == 8:
                self.page_stack.append(17)
                self.myNetwork_page()
            if c == 9:
                print("Thank you for using InCollege!")
                return 0

    def useful_links_page(self):
        # select from links
        choice = int(input(
            "1 - General\n2 - Browse InCollege\n3 - Business Solutions\n4 - Directories\n5 - Previous Page\nEnter a choice: "))

        # general
        if choice == 1:
            self.page_stack.append(8)
            self.general_page()

        # browse incollege
        if choice == 2:
            self.page_stack.append(-1)
            # FUNCTION TO BE ADDED IN FUTURE EPICS
            # MAKE SURE YOU ADD AN INDIVIDUAL BACK OPTION FOR THE FUNCTION INSERTED OR LEAVE THE ONE CURRENTLY IN PLACE
            print("Under construction")
            self.back_option()

        # business solutions
        if choice == 3:
            self.page_stack.append(-1)
            # FUNCTION TO BE ADDED IN FUTURE EPICS
            # MAKE SURE YOU ADD AN INDIVIDUAL BACK OPTION FOR THE FUNCTION INSERTED OR LEAVE THE ONE CURRENTLY IN PLACE
            print("Under construction")
            self.back_option()

        # directories
        if choice == 4:
            self.page_stack.append(-1)
            # FUNCTION TO BE ADDED IN FUTURE EPICS
            # MAKE SURE YOU ADD AN INDIVIDUAL BACK OPTION FOR THE FUNCTION INSERTED OR LEAVE THE ONE CURRENTLY IN PLACE
            print("Under construction")
            self.back_option()

        # previous page
        if choice == 5:
            self.back_page()

    def general_page(self):
        # select from links under the general page
        choice = int(input(
            "1 - Sign Up\n2 - Help Center\n3 - About\n4 - Press\n5 - Blog\n6 - Careers\n7 - Developers\n8 - Previous Page\nEnter a choice: "))

        # sign up/log in
        if choice == 1:
            logORreg = int(
                input("Do you already have an account?\n1 - Yes\n2 - No\nEnter a choice: "))
            if logORreg == 1:
                self.page_stack.append(4)
                self.login_page()
            if logORreg == 2:
                self.page_stack.append(3)
                self.register_page()

        # help center
        if choice == 2:
            self.page_stack.append(-1)
            print("We're here to help")
            self.back_option()

        # about
        if choice == 3:
            self.page_stack.append(-1)
            print("In College: Welcome to In College, the world's largest college student network with many users in many countries and territories worldwide")
            self.back_option()

        # press
        if choice == 4:
            self.page_stack.append(-1)
            print(
                "In College Pressroom: Stay on top of the latest news, updates, and reports")
            self.back_option()

        # blog
        if choice == 5:
            self.page_stack.append(-1)
            # FUNCTION TO BE ADDED IN FUTURE EPICS
            # MAKE SURE YOU ADD AN INDIVIDUAL BACK OPTION FOR THE FUNCTION INSERTED OR LEAVE THE ONE CURRENTLY IN PLACE
            print("Under construction")
            self.back_option()

        # careers
        if choice == 6:
            self.page_stack.append(-1)
            # FUNCTION TO BE ADDED IN FUTURE EPICS
            # MAKE SURE YOU ADD AN INDIVIDUAL BACK OPTION FOR THE FUNCTION INSERTED OR LEAVE THE ONE CURRENTLY IN PLACE
            print("Under construction")
            self.back_option()

        # developers
        if choice == 7:
            self.page_stack.append(-1)
            # FUNCTION TO BE ADDED IN FUTURE EPICS
            # MAKE SURE YOU ADD AN INDIVIDUAL BACK OPTION FOR THE FUNCTION INSERTED OR LEAVE THE ONE CURRENTLY IN PLACE
            print("Under construction")
            self.back_option()

        # previous page
        if choice == 8:
            self.back_page()

    def important_links_page(self):
        choice = int(input("1 - Copyright Notice\n2 - About\n3 - Accessibility\n4 - User Agreement\n5 - Privacy Policy"
                           "\n6 - Cookie Policy\n7 - Copyright Policy\n8 - Brand Policy\n9 - Languages\n10 - Previous Page\nEnter a choice: "))

        # copyright notice
        if choice == 1:
            self.page_stack.append(-1)
            print("(c) 2021 InCollege. All rights reserved")
            self.back_option()

        # about
        if choice == 2:
            self.page_stack.append(-1)
            print("InCollege is an application designed to allow college students to search and apply for jobs and connect with other students.")
            self.back_option()

        # accessibility
        if choice == 3:
            self.page_stack.append(-1)
            print("Here at InCollege we continue to develop our user experience. Keep an eye out for new accessibility features in the future.")
            self.back_option()

        # user agreement
        if choice == 4:
            self.page_stack.append(-1)
            print(
                "As a user of InCollege you give us the right to use any and all of your data for free.")
            self.back_option()

        # privacy policy
        if choice == 5:
            self.page_stack.append(10)
            self.privacy_page()

        # cookie policy
        if choice == 6:
            self.page_stack.append(-1)
            print("At the moment InCollege does not collect cookies.")
            self.back_option()

        # copyright policy
        if choice == 7:
            self.page_stack.append(-1)
            print("No image or information from this site may be reproduced or copied without written permission from the InCollege legal team.")
            self.back_option()

        # brand policy
        if choice == 8:
            self.page_stack.append(-1)
            print(
                "Our brand aims to bring the best talent to the workforce by connecting people.")
            self.back_option()

        # languages
        if choice == 9:
            self.page_stack.append(12)
            self.language_page()
            # self.back_page()

        # Previous Page
        if choice == 10:
            self.back_page()

    def play_video_page(self):
        print("Video is now playing...")
        # back_option prompts the user to enter 0 if they wanna go back
        self.back_option()

    def login_page(self):
        res = self.login()
        if res:
            self.user.authorize()
        # Once the user logs in, they get redirected to the home page
        self.page_stack.append(0)
        self.home_page()

    def register_page(self):
        res = self.register()
        if res:
            # the user is now authenticated, they'll view things slightly different
            self.user.authorize()
        # Once the user logs in, they get redirected to the home page
        self.page_stack.append(0)
        self.home_page()

    def find_people_page(self):
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
                    self.page_stack.append(3)
                    self.register_page()
                elif c == 2:
                    self.page_stack.append(4)
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
        if self.user.authorized:
            self.postjob()
            # this is to go back a level
            self.back_option()

    def skills_page(self):
        skill = input(
            '\n1 - JavaScript\n2 - Python\n3 - SQL Sever\n4 - MongoDB\n5 - Design Patterns\nEnter a choice: ')
        if skill:
            print('under construction')
        self.back_option()

    def language_page(self):
        print("Select a language:")
        language = input(
            '1 - English\n2 - Spanish\n3 - Previous Page\nEnter a choice: ')
        # Previous Page
        if language == '3':
            self.back_page()
        # Try to set language until valid input is entered
        try:
            self.user.set_language(language)
            print("Language set.\n")
            self.back_page()
        except ValueError as e:
            print("{} Please try again.".format(e))
            self.language_page()

    def option_switch_page(self) -> bool or None:
        switch = input("1 - On\n2 - Off\n3 - Previous Page\nEnter Choice: ")
        if switch == '1':
            return True
        elif switch == '2':
            return False
        else:
            return None

    def privacy_page(self):
        print("Here at InCollege we do not guarantee the security of your data.")
        privacy_option = int(
            input("1 - Guest Controls\n2 - Previous Page\nEnter a choice: "))
        # gues control
        if privacy_option == 1:
            self.page_stack.append(11)
            self.guest_controls_page()
        # Previous Page
        elif privacy_option == 2:
            self.back_page()

    def guest_controls_page(self):
        option = input(
            '\n1 - Email Notifications\n2 - SMS notifications\n3 - tareted ads\n4 - Previous Page\nEnter a choice: ')
        # Email notifications
        if option == '1':
            self.page_stack.append(13)
            switch = self.option_switch_page()
            if switch:
                self.user.set_email_notification(switch)
            else:
                self.back_page()
        # sms notifications
        elif option == '2':
            self.page_stack.append(13)
            switch = self.option_switch_page()
            if switch:
                self.user.set_sms_notification(switch)
            else:
                self.back_page()
        # targeted ads
        elif option == '3':
            self.page_stack.append(13)
            switch = self.option_switch_page()
            if switch:
                self.user.set_ad_notification(switch)
            else:
                self.back_page()
        # previous page
        elif option == '4':
            self.back_page()

    # goes up a level to the previous page
    def back_page(self, args=[]):
        # call the function for the previous page
        self.page_stack.pop()
        prev = self.page_stack[-1]
        self.index[prev]['view'](*args)

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
        if int(num_accounts) >= 10:
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

    ################ Profile Pages ##############
    # Creates profile
    def editProfilePage(self, profile: Profile, db: database_access):
        missingTxt = " (missing)"
        title = "1 - title"
        major = "2 - major"
        university_name = "3 - university name"
        about_me = "4 - about me"
        education = "5 - education"
        experience = "6 - add experience"
        back = "7 - Previous Page"
        incomplete = False
        if not profile.isComplete():
            incomplete = True
            print("You may not access your profile until you fill out every field (you may come back later and continue were you left off)")
            if profile.title == None:
                title += missingTxt
            if profile.major == None:
                major += missingTxt
            if profile.university_name == None:
                university_name += missingTxt
            if profile.about_me == None:
                about_me += missingTxt
            if profile.education == None:
                education += missingTxt

        menu_items = "Please select a field to edit:\n{}\n{}\n{}\n{}\n{}\n{}\n{}\nEnter Choice: ".format(
            title, major, university_name, about_me, education, experience, back)

        # display meny and get user input
        print(menu_items)
        c = validateMenuInput(7)

        # back
        if c == 7:
            if profile.isComplete():
                self.back_page([self.user, db])
            else:
                self.back_page()
            return
        # Title
        if c == 1:
            title_input = input("Enter your title: ")
            profile.set_title(title_input, db)
        # major
        elif c == 2:
            major_input = input("Enter your major: ")
            profile.set_major(major_input, db)
        # university name
        elif c == 3:
            university_name_input = input("Enter your university's name: ")
            profile.set_university_name(university_name_input, db)
        # about me
        elif c == 4:
            about_me_input = input("Enter your about me: ")
            profile.set_about_me(about_me_input, db)
        # education
        elif c == 5:
            education_input = input("Enter your education: ")
            profile.set_education(education_input, db)
        elif c == 6:
            experiences = getJobInformation(self.user.username, db)
            if len(experiences) < 3:
                self.addJobExperiencePage()
            else:
                print("Cannot add more than 3 experiences")
        # If the user just completed their profile, send them to profile screen
        if incomplete and profile.isComplete():
            self.printUserProfile(self.user, db)
            return

        if c in range(1, 7):
            self.editProfilePage(profile, db)

    def addJobExperiencePage(self):
        title = input("job title: ")
        employer = input("employer: ")
        date_start = input("start date (MM-DD-YYYY): ")
        date_end = input("end date (MM-DD-YYYY: ")
        location = input("location: ")
        description = input("description: ")
        experience = JobExperience(
            self.user.username, title, employer, date_start, date_end, location, description)
        experience.DbAddJobExperience(db)

    # Requires Database and User object, will print out full profile.
    def printUserProfile(self, user: User, db: database_access):

        profileInformation = getProfile(user.username, db)
        jobInformation = getJobInformation(user.username, db)
        if not profileInformation.isComplete():
            self.editProfilePage(profileInformation, db)
            return

        print_queue = []
        print_queue.append(user.firstname + ' ' +
                           user.lastname + '\'s Profile')
        print_queue.append('Title: ' + profileInformation.title)
        print_queue.append('Major: ' + profileInformation.major)
        print_queue.append('University: ' + profileInformation.university_name)
        print_queue.append('Information and Education:\n' +
                           profileInformation.about_me + ' ' + profileInformation.education)

        if len(jobInformation) > 0:
            print_queue.append('Job Experience')
            for job in jobInformation:
                print_queue.append('Title: ' + job.title)
                print_queue.append('Employer: ' + job.employer)
                print_queue.append('Date Started: ' + job.date_start)
                print_queue.append('Date Ended: ' + job.date_end)
                print_queue.append("Location: " + job.location)
                print_queue.append('Job Description: \n' + job.description)

        for item in print_queue:
            print(item + '\n')
        if user.username == self.user.username:
            print(
                "Please select an option below:\n1 - Edit Profile\n2 - Previous Page\nEnter Choice: ")
            c = validateMenuInput(2)
            if c == 1:
                self.page_stack.append(15)
                self.editProfilePage(profileInformation, db)
            elif c == 2:
                self.back_page()
        else:
            print("Please select an option below:\n1 - Previous Page\nEnter Choice: ")
            c = validateMenuInput(1)
            if c == 1:
                self.back_page()

    # show_my_network will lead here, print all friends.
    def myNetwork_page(self):
        print("Welcome to the your friends, where you hopefully have some.\n")
        sql_for_all_friends = '''
        SELECT * FROM user_friends WHERE username1 = ? or username2 = ? AND status = "Approved"
        '''
        res = db.execute(sql_for_all_friends, [
                         self.user.username, self.user.username])
        # Get usernames excluding self
        friendUsernames = set()
        for item in res:
            friendUsernames.add(item[0])
            friendUsernames.add(item[1])
        friendUsernames.remove(self.user.username)
        if not len(friendUsernames):
            print("Sorry you have no friends, your mother did warn you.")

        # set of friends with complete profiles
        hasProfile = []
        for friend in friendUsernames:
            profile = getProfile(friend, db)
            if profile.isComplete():
                hasProfile.append(profile)

        print("Select one of the users below to view profile.")
        menu = ""
        for i, profile in enumerate(hasProfile):
            menu += "{} - {}\n".format(i+1, profile.username)
        menu += "{} - Previous Page\nEnter a number: ".format(
            len(hasProfile)+1)

        print(menu)
        c = validateMenuInput(len(hasProfile) + 1)
        if c == len(hasProfile) + 1:
            self.back_page()
        elif (c > 0):
            user = get_user_by_username(hasProfile[c-1].username, db)
            self.page_stack.append(14)
            self.printUserProfile(user, db)
    # call this to check right when user logs in before main page, if our user is username2 that means its a request.

    def pendingFriendRequests(self, db):
        sql_for_pending_requests = '''
        SELECT * FROM user_friends as U WHERE U.username2 = ? AND U.status = "Pending"
        '''
        res = db.execute(sql_for_pending_requests, [self.user.username])
        if len(res):
            for request in res:
                requester = request[0]
                databaseStatusUpdate = ''
                while(True):  # This workflow remains untested.
                    # can query user table using this name to return the fname and lname here
                    print("Friend request from " + requester +
                          '. Enter 1 to accept or 2 to decline.\n')
                    userResponse = input()
                    if userResponse == '1':
                        databaseStatusUpdate = "Approved"
                        break
                    elif userResponse == '2':
                        databaseStatusUpdate = "Rejected"
                        break
                    else:
                        print("Please enter a valid response.")
                status_change_sql = '''
                UPDATE user_friends
                SET status = ?
                WHERE
                    username1 = ? AND username2 = ?
                '''
                args = [databaseStatusUpdate, requester, self.user.username]
                try:
                    db.execute(status_change_sql, args)
                    print("Successfully saved your changes!\n")
                except:
                    print("Failed to accept or reject request.\n")

    def add_friend_page(self):
        def getUserSelection(listUsers):
            i = 1
            print("Results:\n")
            for user in listUsers:
                if(user[0] == self.user.username):
                    listUsers.remove(user)
            for user in listUsers:
                print(str(i) + ': ' + ' Username: ' +
                      str(user[0]) + ' Firstname: ' + str(user[2] + ' Lastname: ' + str(user[3])))
                i = i + 1
            if i == 1:
                print("No Results were found using that Query.\n")
                return False
            while(True):
                answer = input(
                    '\nPlease input the number of the user to add as a friend, input "x" to cancel.')
                if ((answer.lower()) == 'x'):
                    return None
                else:
                    try:
                        answer = int(answer)
                        if answer > i - 1 or answer < 1:
                            print("Please enter a number in the shown range.")
                            continue
                        return listUsers[answer - 1][0]
                    except:
                        print("Please enter a valid whole number")

        def searchByLastName():
            name = input('Please input the lastname to search for:\n')
            search_by_lastname_sql = '''
            SELECT * FROM users WHERE lower(lastname) = lower(?)'''
            res = db.execute(search_by_lastname_sql, [name])
            if len(res):
                res = getUserSelection(res)
                if res:
                    return sendFriendRequest(res)
                else:
                    return False
            print("No results were found using that query.\n")
            return False

        def searchByUniversity():
            uni = input('Please input the University name to search for:\n')
            search_by_university_sql = '''
            SELECT * 
            FROM users 
            WHERE username IN (
                SELECT username
                FROM profile
                WHERE lower(university_name) = lower(?));
            '''
            res = db.execute(search_by_university_sql, [uni])
            if len(res):
                res = getUserSelection(res)
                if res:
                    return sendFriendRequest(res)
                else:
                    return False
            print('No results were found using that query.\n')
            return False

        def searchByMajor():
            major = input('Please input the Major to search for:\n')
            search_by_major_sql = '''
            SELECT * 
            FROM users 
            WHERE username IN (
                SELECT username
                FROM profile
                WHERE lower(major) = lower(?));
            '''
            res = db.execute(search_by_major_sql, [major])
            if len(res):
                res = getUserSelection(res)
                if res:
                    return sendFriendRequest(res)
                else:
                    return False
            print('No results were found using that query.\n')
            return False

        def sendFriendRequest(username):
            add_friend_sql = '''
            INSERT INTO user_friends VALUES (?,?,?)
            '''
            try:
                db.execute(add_friend_sql, [
                           self.user.username, username, 'Pending'])
                print("Friend Request Sent")
                return True
            except Exception as error:
                print('Friend Request Already Exists.')
                return False

        while(True):
            print("Would you like to search by:\n1 - Lastname\n2 - University\n3 - Major")
            answer = input()
            result = None
            if(answer == '1'):
                result = searchByLastName()
            elif(answer == '2'):
                result = searchByUniversity()
            elif(answer == '3'):
                result = searchByMajor()
            else:
                print("Please select a valid option.")
            if result is not None:
                if result:
                    break
                else:
                    cont = input(
                        "Would you like to search again?\nInput 1 to continue, anything else to quit")
                    if cont != '1':
                        break
        # add self to stack.
        self.home_page()
