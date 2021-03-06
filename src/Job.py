from re import subn
from src.database_access import database_access
from src.Notification import Notification


class Job:
    def __init__(self, id: int, username: str, title: str, description: str, employer: str, location: str, salary: float):
        self.id = id
        self.username = username
        self.title = title
        self.description = description
        self.employer = employer
        self.location = location
        self.salary = salary

    def __eq__(self, other):
        return self.id == other.id and self.username == other.username and self.title == other.title and self.description == other.description and self.employer == other.employer and self.location == other.location and self.salary == other.salary

    @staticmethod
    def get_job_by_id(id: int, db: database_access):
        jobQueryString = '''
            SELECT *
            FROM jobs
            WHERE job_id = ?
            '''
        job = db.execute(jobQueryString, [id])
        if job:
            job = job[0]
            return Job(job[0], job[1], job[2], job[3], job[4], job[5], job[6])
        else:
            return False

    @staticmethod
    def get_my_postings(user: str, db: database_access):
        jobQueryString = '''
            SELECT *
            FROM jobs
            WHERE username = ?
        '''
        my_jobs = list()
        jobs = db.execute(jobQueryString, [user])
        for job in jobs:
            my_jobs.append(Job(job[0], job[1], job[2],
                               job[3], job[4], job[5], job[6]))
        return my_jobs

    def print_full_job(self):
        print(
            f'\n*{self.title} Job Posting*\n' +
            f'Job Description: {self.description}\n' +
            f'Location: {self.location}\n' +
            f'Expected Salary: {self.salary}\n' +
            f'Posted By: {self.employer}'
        )

    @staticmethod
    def delete_job(id: int, db: database_access):
        delete_query_string = '''
            DELETE FROM jobs WHERE job_id = ?
        '''
        # alert all applicants that the job has been deleted
        deletedjob = db.execute('SELECT * FROM jobs WHERE job_id = ?', [id])
        content = "A job that you applied, " + \
            deletedjob[0][2] + " for has been deleted"

        allusers = db.execute(
            'SELECT * FROM user_applied_jobs WHERE job_id = ?', [id])
        for user in allusers:
            Notification.add_notification(user[0], content, db)

        # delete job
        check_string = 'SELECT COUNT(*) FROM jobs WHERE job_id = ?;'
        db.execute(delete_query_string, [id])
        # checking if the delete was successful
        res = db.execute(check_string, [id])
        return True if res[0][0] == 0 else False

    @staticmethod
    def apply_job(username, job_id, reason, db: database_access):
        apply_job_sql = '''
        INSERT INTO user_applied_jobs VALUES (?,?,?,?)
        '''
        db.execute(apply_job_sql, [username, job_id, reason, 'Applied'])

    @staticmethod
    def add_interested(username, job_id, db: database_access):
        interested_job_sql = '''
        INSERT INTO user_interested_jobs VALUES (?,?)
        '''
        db.execute(interested_job_sql, [username, job_id])

    @staticmethod
    def get_applied_jobs(username, db):
        applied_jobs_sql = '''
        SELECT job_id from user_applied_jobs WHERE username = ?'''
        res = db.execute(applied_jobs_sql, [username])
        if res:
            out = []
            for element in res:
                out.append(Job.get_job_by_id(element[0], db))
            return out
        return False

    @staticmethod
    def get_interested_jobs(username, db):
        applied_jobs_sql = '''
        SELECT job_id from user_interested_jobs WHERE username = ?'''
        res = db.execute(applied_jobs_sql, [username])
        if res:
            out = []
            for element in res:
                out.append(Job.get_job_by_id(element[0], db))
            return out
        return False
