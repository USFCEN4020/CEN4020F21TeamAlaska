from typing import List

from src.database_access import database_access


class JobExperience:
    def __init__(self, username: str, title: str, employer: str, date_start: str, date_end: str, location: str, description: str):
        self.username = username
        self.title = title
        self.employer = employer
        self.date_start = date_start
        self.date_end = date_end
        self.location = location
        self.description = description

    def __eq__(self, other):
        if isinstance(self, other.__class__):
            return self.username == other.username and self.title == other.title and self.employer == other.employer and self.date_start == other.date_start and self.date_end == other.date_end and self.location == other.location and self.description == other.description
        return False

    def DbAddJobExperience(self, db: database_access) -> None:
        sql = "INSERT INTO job_experience VALUES (?,?,?,?,?,?,?)"
        params = [
            self.username,
            self.title,
            self.employer,
            self.date_start,
            self.date_end,
            self.location,
            self.description
        ]
        db.execute(sql, params)


def getJobInformation(username: str, db: database_access) -> List[JobExperience]:
    jobQueryString = '''
        SELECT *
        FROM job_experience
        WHERE username = ?
        '''
    jobInformation = db.execute(jobQueryString, [username])
    experiences = list()
    for job in jobInformation:
        experiences.append(JobExperience(
            job[0], job[1], job[2], job[3], job[4], job[5], job[6]))

    return experiences
