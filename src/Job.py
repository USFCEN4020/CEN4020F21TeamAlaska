from re import subn
from src.database_access import database_access

class Job:
    def __init__(self, id: int, username: str, title: str, description: str, employer: str, location: str, salary: float):
        self.id = id
        self.username = username
        self.title = title
        self.description = description
        self.employer = employer
        self.location = location
        self.salary = salary

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
            my_jobs.append(Job(job[0], job[1], job[2], job[3], job[4], job[5], job[6]))
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
        db.execute(delete_query_string, [id])