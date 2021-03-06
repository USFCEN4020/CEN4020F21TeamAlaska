import re
from src.Course import Course
from src.Job import Job
from src.database_access import database_access as Database
from src.JobExperience import *
from src.User import *
from src.PostedJob import PostedJob
from Profile.Profile import *
from src.message import *
from src.helpers import validateMenuInput
from src.Notification import *
import src.api as RSquared
db = Database("InCollege.sqlite3")
RSquared.jobInput(db)
RSquared.studentInput(db)
RSquared.trainingInput(db)
RSquared.appliedJobsOutput(db)
RSquared.profileOutput(db)
RSquared.savedJobsOutput(db)
RSquared.studentOutput(db)
RSquared.trainingOutput(db)
RSquared.jobOutput(db)

class Page:
    # each page will "render" the appropriate "form" or prompt
    def __init__(self):
        # current login info
        self.user = User("", "", "", "", "", "english",
                         True, True, True, False, None, db)
        # stack is to implement the navigation functionality
        self.page_stack = [0]
        # Numbered pages so they're easily added to the stack and then called
        self.index = {
            -1: {
                "view": self.getOutOfTest
            },
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
            },
            18: {
                "view": self.friend_profile_page
            },
            19: {
                "view": self.messages_page
            },
            20: {
                "view": self.training_page
            },
            21: {
                "view": self.in_college_learning_page
            }
        }

    def home_page(self):
        # I want the home page to view different option depending on whether or not the user is authenticated
        if not self.user.authorized:
            c = -1
            print("Welcome to InCollege: *** Where you're no longer going to be broke ***\nAll of our broke students managed to find job!!!"
                  "\n\n1 - Play Video\n2 - People you may know\n3 - Register\n4 - Login\n5 - Useful Links\n6 - InCollege Important Links\n7 - Training\n8 - Exit\nEnter a choice: ")
            c = validateMenuInput(8)
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
                self.page_stack.append(20)
                self.training_page()
            if c == 8:
                print("Thank you for using InCollege!")
                return 0
        else:
            # Preliminary pending friend request check, not a page.
            self.pendingFriendRequests(db)
            # Show if new messages are in inbox, "new message" is defined as messages not read yet
            self.notifyMessage(db)
            # Notify a user if they haven't created a profile
            self.notifyCreateProfile()

            c = -1
            print(
                "1 - Job Menu\n2 - Find people you may know\n3 - learn a new skill\n4 - Useful Links\n5 - InCollege Important Links\n6 - Profile\n7 - Add Friend\n8 - Network\n9 - Messages\n10 - InCollege Learning\n0 - Exit\nEnter a choice: ")
            c = validateMenuInput(11)
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
                self.add_friend_page()
            if c == 8:
                self.page_stack.append(17)
                self.myNetwork_page()
            if c == 9:
                self.page_stack.append(19)
                self.messages_page()
            if c == 10:
                self.page_stack.append(21)
                self.in_college_learning_page()
            if c == 0:
                print("Thank you for using InCollege!")
                return 0

    def training_page(self):
        print("1 - Training and Education\n2 - IT Help Desk\n3 - Business Analysis and Strategy\n4 - Security\n5 - Go back")
        response = validateMenuInput(5)
        if response == 1:
            print(
                "1 - Learn Python\n2 - Learn React\n3 - Public Speaking 101\n4 - SCRUM basics")
            response = validateMenuInput(4)
            print("Under Construction.")
            self.back_option()
        if response == 2 or 4:
            print("Coming soon!")
            self.back_option()
        if response == 3:
            print("1 - How to use InCollege learning\n2 - Train the trainer\n3 - Gamification of learning\n4 - Not seeing what you're looking for? Sign in to see all 7,609 results.")
            response == validateMenuInput(4)
            print("Please Login")
            self.login_page()
        if response == 5:
            self.back_option()

    # Marking of taken courses will be needed thus the workflow will change a bit.
    def in_college_learning_page(self):
        courses = Course.getAllCourseTitles(db)
        menu = "Pick any of the courses below to enroll:\n"
        for i, course in enumerate(courses):
            menu += "{} - {}".format(i+1, course[0])
            completed = Course.getCourseStatus(
                self.user.username, course[0], db)
            if completed:
                menu += " (COMPLETED)"
            menu += "\n"
        menu += "{} - Go Back".format(len(courses) + 1)
        print(menu)
        response = validateMenuInput(len(courses) + 1)
        if response == len(courses) + 1:
            self.back_page()
        else:
            completed = Course.getCourseStatus(
                self.user.username, courses[response - 1][0], db)
            # Student has not taken course
            if not completed:
                print("You have now completed this training.")
                Course.setCourseStatus(
                    self.user.username, courses[response - 1][0], True, db)
                RSquared.trainingOutput(db)
            else:
                print(
                    "You have already taken this course, do you want to take it again?\n1 - yes\n2 - no")
                retakeCourseResponse = validateMenuInput(2)
                if retakeCourseResponse == 1:
                    print("You have now completed this training")
                else:
                    print("Course Cancelled")
            self.in_college_learning_page()

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
        jobs = db.execute('SELECT * FROM jobs')
        if(len(jobs) >= 10):
            print("There are already 10 jobs. Please try again later\n")
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
            db.execute('INSERT INTO jobs(username, title, description, employer, location, salary) VALUES (?, ?, ?, ?, ?, ?)', [
                temp.name, temp.title, temp.description, temp.employer, temp.location, temp.salary])

            # set alert all users that a new job has been posted
            allusers = db.execute('SELECT * FROM users')
            content = "A new job, " + temp.title + " has been posted"
            for user in allusers:
                Notification.add_notification(user[0], content, db)

            print("Thanks your job was posted! Returning to the previous menu...")
            return True

    def notify_jobs_applied(self):
        appliedJobs = Job.get_applied_jobs(self.user.username, db)
        appliedJobsNumber = 0 if not appliedJobs else len(appliedJobs)
        print("You have currently applied for {} jobs".format(appliedJobsNumber))

    def post_job_page(self):
        if self.user.authorized:
            # Tell student how many jobs they have applied for
            self.notify_jobs_applied()

            print(
                '1 - Post a New Job\n2 - View Jobs\n3 - My Postings\n4 - View applications\n5 - View interested\n6 - Previous page\nEnter a choice: ')
            c = validateMenuInput(6)
            # posting a new job
            if c == 1:
                self.page_stack.append(-1)
                self.postjob()
                self.back_option()
            # going back
            elif c == 6:
                self.back_page()
            # view all jobs
            elif c == 2:
                self.page_stack.append(-1)
                # VIEWING ALREADY EXISTING JOBS
                jobs = db.execute('SELECT job_id, title FROM jobs')
                if not jobs:
                    print('sorry, no jobs for you')
                    self.back_option()
                else:
                    obj = {}
                    print('Available Jobs:')
                    for job in jobs:
                        obj[job[0]] = job[1]
                        print(f'{job[0]} - {job[1]}')
                    c3 = int(input("Choose the job you'd like to view: "))
                    job = Job.get_job_by_id(c3, db)
                    if job:
                        job.print_full_job()
                        favIntOther = input(
                            "\n1 - Apply\n2 - Interested\nAny Other key - Go Back")
                        if favIntOther == '1':
                            reason = input("Please enter your qualifications for this job or why you fit the position.\n")
                            Job.apply_job(self.user.username, job.id, reason, db)
                            RSquared.appliedJobsOutput(db)
                        elif favIntOther == '2':
                            Job.add_interested(self.user.username, job.id, db)
                            RSquared.savedJobsOutput(db)
                    else:
                        print('Job does not exist')
                    self.back_option()

            # my job postings
            elif c == 3:
                self.page_stack.append(-1)
                my_jobs = Job.get_my_postings(self.user.username, db)
                if not my_jobs:
                    print("You don't have any postings at the moment")
                    self.back_option()
                else:
                    print('\nMy Postings:')
                    for job in my_jobs:
                        # job.print_full_job()
                        print(f'Job ID: {job.id}, Title: {job.title}')
                    print('\n1 - Delete Job\n2 - Previous page\nEnter a choice: ')
                    c2 = validateMenuInput(2)
                    # DELETING MY JOB
                    if c2 == 1:
                        max = db.execute(
                            'SELECT MAX(job_id) FROM jobs', [])[0][0]
                        # max = max[0][0] if max else 0
                        print("Enter the Job ID to Delete: ")
                        c_job_to_delete = validateMenuInput(max)
                        result = Job.delete_job(int(c_job_to_delete), db)
                        if(result):
                            print('Job successfully deleted')
                        else:
                            print('Invalid Job ID')
                        self.back_option()
                    elif c2 == 2:
                        self.back_page()
            elif c == 4:
                self.page_stack.append(-1)
                jobs = Job.get_applied_jobs(self.user.username, db)
                if jobs != False:
                    for job in jobs:
                        print('\n')
                        job.print_full_job()
                        print('\n')
                self.back_page()

            elif c == 5:
                self.page_stack.append(-1)
                jobs = Job.get_interested_jobs(self.user.username, db)
                if jobs != False:
                    for job in jobs:
                        job.print_full_job()
                else:
                    print("You are not interested in any jobs currently.\n")
                self.back_page()

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

    # MESSAGES
    def messages_page(self):
        # cur_user = self.user.username
        print("1 - Inbox\n2 - Send a message\n0 - Back to previous\nEnter a choice: ")
        c = validateMenuInput(2)
        if c == 0:
            self.back_page()
        if c == 1:
            self.page_stack.append(-1)
            # viewing the messages
            messages = Message.get_my_messages(self.user.username, db)
            i = 1
            while len(messages) != 0:
                for message in messages:
                    print(
                        i+f'Status:{message[4].capitalize()} {message[1]}: {message[3][0:10]}')
                choice = input(
                    "Choose a message to read. Or choose 0 to leave inbox")
                if choice == 0:
                    break
                else:
                    self.view_message(messages, choice, self)
            self.back_option()
        if c == 2:
            self.page_stack.append(-1)
            people_to_message = []
            if self.user.tier == "standard":
                # get friends
                people_to_message = self.get_friends()
            if self.user.tier == "plus":
                # get all users except self
                people_to_message = get_all_usernames(self.user.username, db)
            for idx, person in enumerate(people_to_message):
                print(f'{idx + 1} - {person[0]}')
            c_person = validateMenuInput(len(people_to_message))
            recipient = people_to_message[c_person - 1][0]
            msg = input(f'Your message to {recipient}: ')
            Message.send_message(self.user.username, recipient, msg, db)
            self.back_option()
    ###
    # message viewer

    def view_message(messages, selection, self):
        # update message from sent to read
        sql_update = '''
            UPDATE messages SET status = 'read' WHERE message_id = ?
        '''
        db.execute(sql_update, messages[selection][0])

        # print message
        print(f'{messages[selection][1]}: {messages[selection][3]}')

        # options to reply, delete, or go back to inbox
        choice = input("\n\n1 - Reply\n2 - Delete\n3 - Return to Inbox")
        if choice == 1:
            people_to_message = []
            if self.user.tier == "standard":
                # get friends
                people_to_message = self.get_friends()
            if self.user.tier == "plus":
                # get all users except self
                people_to_message = get_all_usernames(self.user.username, db)
            for idx, person in enumerate(people_to_message):
                print(f'{idx} - {person[0]}')
            c_person = validateMenuInput(len(people_to_message))
            recipient = people_to_message[c_person][0]
            msg = input(f'Your message to {recipient}: ')
            Message.send_message(self.user.username, recipient, msg, db)

            print("Message sent. Returning to Inbox...\n")
        if choice == 2:
            Message.delete_message(messages[selection][0])
            messages.remove(selection)

            print("Message removed. Returning to Inbox...\n")
        if choice == 3:
            print("Returning to Inbox...\n")
    # pulls from database to see which messages are available

    def notifyMessage(self, db):
        sql_count_messasges = '''
            SELECT COUNT(*) FROM messages WHERE receiver = ? AND status = 'sent'
        '''
        numMessage = db.execute(sql_count_messasges, [
                                self.user.username])[0][0]
        if(numMessage >= 1):
            print("You have " + str(numMessage) +
                  " new messages! Go to the messages tab to view.")

    def notifyCreateProfile(self):
        if self.user.authorized:
            profile = getProfile(self.user.username, db)
            if not profile.isComplete():
                print("Don't forget to create a profile.\n")

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
            print("1- Standard Tier\n2- Plus Tier\nEnter a choice: ")
            tier = validateMenuInput(2)
            tier = "plus" if tier == 2 else "standard"
            if tier == "plus":
                fo = input(
                    'Total = $10\nEnter Credit Card Information (anything):')
                print("Thanks for your subscription!")
            return (user, password, firstname, lastname, tier)
        return (user, password)

    def login(self):
        while True:
            cred = self.get_credentials(False)
            # checks if the credentials exist in the users table
            user = get_user_by_login(cred[0], cred[1], db)
            if user:
                self.user = user
                print('You have successfully logged in\n')
                if (datetime.datetime.now() - user.last_login).days > 7:
                    print(
                        "Remember -- you're going to want to have a job when you graduate. Make sure that you start to apply for jobs today!")
                user.set_last_login()

                # print every notification for a user, then delete
                notifications = Notification.get_notifications(
                    self.user.username, db)
                for notification in notifications:
                    print(notification[1] + "\n")
                Notification.delete_notifications(self.user.username, db)
                return True
            else:
                print('Incorrect username / password, please try again\n')
                return False

    def register(self):
        # checking the number of accounts already registered
        accounts = db.execute('SELECT * FROM users')
        num_accounts = len(accounts)
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
                RSquared.studentOutput(db)

                # Notify every existing user about new account
                msg = "{} {} has joined InCollege".format(
                    self.user.firstname, self.user.lastname)
                for account in accounts:
                    Notification.add_notification(account[0], msg, db)
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
            RSquared.profileOutput(db)
        # major
        elif c == 2:
            major_input = input("Enter your major: ")
            profile.set_major(major_input, db)
            RSquared.profileOutput(db)
        # university name
        elif c == 3:
            university_name_input = input("Enter your university's name: ")
            profile.set_university_name(university_name_input, db)
            RSquared.profileOutput(db)
        # about me
        elif c == 4:
            about_me_input = input("Enter your about me: ")
            profile.set_about_me(about_me_input, db)
            RSquared.profileOutput(db)
        # education
        elif c == 5:
            education_input = input("Enter your education: ")
            profile.set_education(education_input, db)
            RSquared.profileOutput(db)
        elif c == 6:
            experiences = getJobInformation(self.user.username, db)
            if len(experiences) < 3:
                self.addJobExperiencePage()
                RSquared.profileOutput(db)
            else:
                print("Cannot add more than 3 experiences")
        # If the user just completed their profile, send them to profile screen
        if incomplete and profile.isComplete():
            self.printUserProfile(self.user, db)
            return

        if c in range(1, 7):
            self.editProfilePage(profile, db)
            RSquared.profileOutput(db)

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
        res = self.get_friends(db)
        friendUsernames = set()
        # pending is being added
        for item in res:
            friendUsernames.add(item[0])
            friendUsernames.add(item[1])
        try:
            friendUsernames.remove(self.user.username)
        except:
            pass
        hasProfile = []
        if not len(friendUsernames):
            print("Sorry you have no friends, your mother did warn you.")
            print("Select one of the options below: ")
        else:
            # set of friends with complete profiles
            for friend in friendUsernames:
                profile = getProfile(friend, db)
                if profile.username != self.user.username and profile.isComplete():
                    hasProfile.append(profile)

            sortedSet = list(friendUsernames)
            sortedSet.sort()
            friendMenu = "These are your friends:\n"
            for i, username in enumerate(sortedSet):
                if username != self.user.username:
                    friendMenu += "{} - {}\n".format(i+1, username)
            print(friendMenu)

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
        elif c > 0:
            user = get_user_by_username(hasProfile[c-1].username, db)
            self.page_stack.append(18)
            self.friend_profile_page(user, db)

    def get_friends(self, db):
        sql_for_all_friends = '''
        SELECT * FROM user_friends WHERE (username1 = ? or username2 = ?) AND status = "Approved"
        '''
        res = db.execute(sql_for_all_friends, [
                         self.user.username, self.user.username])
        return res

    def friend_profile_page(self, user, db):
        profileInformation = getProfile(user.username, db)
        jobInformation = getJobInformation(user.username, db)
        print_queue = []
        print_queue.append(user.firstname + ' ' +
                           user.lastname + '\'s Profile')
        if profileInformation.title != None:
            print_queue.append('Title: ' + profileInformation.title)
        if profileInformation.major != None:
            print_queue.append('Major: ' + profileInformation.major)
        if profileInformation.university_name != None:
            print_queue.append(
                'University: ' + profileInformation.university_name)
        if profileInformation.education != None:
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
        print("Please select an option below:\n1 - Delete Friend\n2 - Previous Page\nEnter Choice: ")
        c = validateMenuInput(2)
        if c == 1:
            self.delete_friend(user, db)
            self.back_page()
        if c == 2:
            self.back_page()

    def delete_friend(self, user, db):
        delete_friend_sql_query = '''
            DELETE FROM user_friends WHERE (username1 = ? AND username2 = ?) or (username1 = ? AND username2 = ?)
        '''
        res = db.execute(delete_friend_sql_query, [
                         self.user.username, user.username, user.username, self.user.username])

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
                    userResponse = input("")
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
        while(True):
            print("Would you like to search by:\n1 - Lastname\n2 - University\n3 - Major")
            answer = input("")
            result = None
            if(answer == '1'):
                result = self.searchByLastName()
            elif(answer == '2'):
                result = self.searchByUniversity()
            elif(answer == '3'):
                result = self.searchByMajor()
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

    def getUserSelection(self, listUsers):
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

    def searchByLastName(self):
        name = input('Please input the lastname to search for:\n')
        search_by_lastname_sql = '''
        SELECT * FROM users WHERE lower(lastname) = lower(?)'''
        res = db.execute(search_by_lastname_sql, [name])
        if len(res):
            res = self.getUserSelection(res)
            if res:
                return self.sendFriendRequest(res)
            else:
                return False
        print("No results were found using that query.\n")
        return False

    def searchByUniversity(self):
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
            res = self.getUserSelection(res)
            if res:
                return self.sendFriendRequest(res)
            else:
                return False
        print('No results were found using that query.\n')
        return False

    def searchByMajor(self):
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
            res = self.getUserSelection(res)
            if res:
                return self.sendFriendRequest(res)
            else:
                return False
        print('No results were found using that query.\n')
        return False

    def sendFriendRequest(self, username):
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

    def getOutOfTest(self):
        pass
