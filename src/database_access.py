import sqlite3


class database_access:
    # constructor establsihes connection and creates tables
    def __init__(self, db_name):
        self.db = sqlite3.connect(
            db_name,  detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES)

        sql_create_users_table = ''' CREATE TABLE IF NOT EXISTS users (
            username text PRIMARY KEY,
            password text NOT NULL,
            firstname TEXT NOT NULL,
            lastname TEXT NOT NULL,
            tier TEXT NOT NULL,
            language text NOT NULL,
            email_notification BOOLEAN NOT NULL,
            sms_notification BOOLEAN NOT NULL,
            ad_notification BOOLEAN NOT NULL,
            last_login TIMESTAMP NOT NULL
        )
        '''
        sql_create_jobs_table = ''' CREATE TABLE IF NOT EXISTS jobs (
            job_id integer PRIMARY KEY AUTOINCREMENT,
            username text NOT NULL,
            title text NOT NULL,
            description text NOT NULL,
            employer text NOT NULL,
            location text NOT NULL,
            salary real NOT NULL
        )
        '''
        sql_create_profile_table = '''
        CREATE TABLE IF NOT EXISTS profile (
            username text NOT NULL,
            title text,
            major text,
            university_name text,
            about_me text,
            education text,
            PRIMARY KEY(username,title),
            FOREIGN KEY (username) REFERENCES users (username)
            )
        '''
        sql_create_user_job_experience_table = '''
            CREATE TABLE IF NOT EXISTS job_experience (
            username text NOT NULL,
            title text,
            employer text,
            date_start text,
            date_end text,
            location text,
            description text,
            PRIMARY KEY(username,title),
            FOREIGN KEY (username) REFERENCES users (username)
            )
        '''
        # Pending, Approved, Rejected are the 3 statuses we should care about.
        sql_create_user_friend_relation = '''
            CREATE TABLE IF NOT EXISTS user_friends (
            username1 text NOT NULL,
            username2 text NOT NULL,
            status text NOT NULL,
            PRIMARY KEY(username1, username2),
            FOREIGN KEY (username1) REFERENCES users (username),
            FOREIGN KEY (username2) REFERENCES users (username)
            )
        '''

        sql_create_user_interested_job = '''
            CREATE TABLE IF NOT EXISTS user_interested_jobs (
            username text NOT NULL,
            job_id integer NOT NULL,
            PRIMARY KEY (username, job_id),
            FOREIGN KEY (username) REFERENCES users (username),
            FOREIGN KEY (job_id) REFERENCES jobs (job_id)
            )
        '''

        sql_create_user_applied_job = '''
            CREATE TABLE IF NOT EXISTS user_applied_jobs (
            username text NOT NULL,
            job_id integer NOT NULL,
            reason TEXT NOT NULL,
            status text NOT NULL,
            PRIMARY KEY (username),
            FOREIGN KEY (username) REFERENCES users (username),
            FOREIGN KEY (job_id) REFERENCES jobs (job_id)
            )
        '''
        sql_create_messages_table = '''
            CREATE TABLE IF NOT EXISTS messages (
                message_id INTEGER PRIMARY KEY AUTOINCREMENT,
                sender TEXT NOT NULL,
                receiver TEXT NOT NULL,
                body TEXT NOT NULL,
                status TEXT DEFAULT 'sent' NOT NULL,
                time_sent TIMESTAMP DEFAULT CURRENT_TIMESTAMP NOT NULL,
                FOREIGN KEY (sender) REFERENCES users (username),
                FOREIGN KEY (receiver) REFERENCES users (username)
            )
        '''
        sql_create_notifications_table = '''
            CREATE TABLE IF NOT EXISTS notifications (
                username text NOT NULL,
                content text NOT NULL
            )
        '''
        sql_create_course_table = '''
            CREATE TABLE IF NOT EXISTS courses (
                title text NOT NULL
            )
        '''
        # courses assosiated to a student
        sql_create_student_courses_table = '''
            CREATE TABLE IF NOT EXISTS student_courses (
                username text NOT NULL,
                title text NOT NULL,
                completed BOOLEAN NOT NULL
            )
        '''
        c = self.db.cursor()
        c.execute(sql_create_users_table)
        c.execute(sql_create_jobs_table)
        c.execute(sql_create_profile_table)
        c.execute(sql_create_user_job_experience_table)
        c.execute(sql_create_user_friend_relation)
        c.execute(sql_create_user_interested_job)
        c.execute(sql_create_user_applied_job)
        c.execute(sql_create_messages_table)
        c.execute(sql_create_notifications_table)
        c.execute(sql_create_course_table)
        c.execute(sql_create_student_courses_table)

        # Add default courses
        existingCoursesSQL = "SELECT title FROM courses;"
        existingCourses = self.db.execute(existingCoursesSQL).fetchall()
        if existingCourses == []:
            defaultCourses = [
                "How to use InCollege learning",
                "Train the trainer",
                "Gamification of learning",
                "Understanding the Architectural Design Process",
                "Project Management Simplified"
            ]
            addNewCourseSQL = "INSERT INTO courses VALUES (?);"
            for course in defaultCourses:
                self.db.execute(addNewCourseSQL, [course])

        self.db.commit()

    # To select and print all tables
    def print_users(self):
        c = self.db.cursor()
        c.execute('SELECT * FROM users')
        # view all selected records
        data = c.fetchall()
        for row in data:
            print(row)

    def print_jobs(self):
        c = self.db.cursor()
        c.execute('SELECT * FROM jobs')
        # view all selected jobs
        data = c.fetchall()
        for row in data:
            print(row)

    def print_profile(self):
        c = self.db.cursor()
        c.execute('SELECT * FROM profile')
        # view all selected records
        data = c.fetchall()
        for row in data:
            print(row)

    def print_job_experience(self):
        c = self.db.cursor()
        c.execute('SELECT * FROM job_experience')
        # view all selected job experience
        data = c.fetchall()
        for row in data:
            print(row)

    def print_all_friend_relations(self):
        c = self.db.cursor()
        c.execute('SELECT * FROM user_friends')
        # view all selected friends
        data = c.fetchall()
        for row in data:
            print(row)

    def print_all_interested_jobs(self):
        c = self.db.cursor()
        c.execute('SELECT * FROM user_interested_jobs')
        # view all selected
        data = c.fetchall()
        for row in data:
            print(row)

    def print_all_applied_jobs(self):
        c = self.db.cursor()
        c.execute('SELECT * FROM user_applied_jobs')
        # view all selected
        data = c.fetchall()
        for row in data:
            print(row)

    # if you want to clear the table(s)
    def delete_users_table(self):
        c = self.db.cursor()
        sql = 'DELETE FROM users'
        c.execute(sql)
        self.db.commit()

    def delete_profile_table(self):
        c = self.db.cursor()
        sql = 'DELETE FROM profile'
        c.execute(sql)
        self.db.commit()

    def delete_job_experience_table(self):
        c = self.db.cursor()
        sql = 'DELETE FROM job_experience'
        c.execute(sql)
        self.db.commit()

    def delete_jobs_table(self):
        c = self.db.cursor()
        sql = 'DROP TABLE jobs'
        c.execute(sql)
        self.db.commit()

    def delete_user_friends(self):
        c = self.db.cursor()
        sql = 'DELETE FROM user_friends'
        c.execute(sql)
        self.db.commit()

    def delete_user_applied(self):
        c = self.db.cursor()
        sql = 'DELETE FROM user_applied_jobs'
        c.execute(sql)
        self.db.commit()

    def delete_user_interested(self):
        c = self.db.cursor()
        sql = 'DELETE FROM user_interested_jobs'
        c.execute(sql)
        self.db.commit()

    def delete_messages(self):
        c = self.db.cursor()
        sql = 'DELETE FROM messages'
        c.execute(sql)
        self.db.commit()

    def delete_notifications(self):
        c = self.db.cursor()
        sql = 'DELETE FROM notifications'
        c.execute(sql)
        self.db.commit()

    def delete_courses(self):
        c = self.db.cursor()
        sql = 'DELETE FROM courses'
        c.execute(sql)
        self.db.commit()

    def delete_student_courses(self):
        c = self.db.cursor()
        sql = 'DELETE FROM student_courses'
        c.execute(sql)
        self.db.commit()

    def execute(self, sql, params=[]):
        c = self.db.cursor()
        c.execute(sql, params)
        self.db.commit()

        return c.fetchall()

    def commit(self):
        self.db.commit()

    def close(self):
        self.db.close()
