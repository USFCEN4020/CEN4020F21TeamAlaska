import os
import src.User as User
import src.database_access as Database

apiFilePath = "./src/API-Files/"


def studentInput(db: Database):
    if not os.path.exists('{}studentAccounts.txt'.format(apiFilePath)):
        return None
    file = open('{}studentAccounts.txt'.format(apiFilePath))
    students = []
    student = []
    for line in file:
        if line.strip() == '=====':
            students.append(student)
            student = []
            continue
        for item in line.split(' '):
            student.append(item.replace('\n', ''))

    # Insertion time, check for amount and do calculamations
    count = len(db.execute('SELECT * FROM users'))
    for i in range(0, 10 - count):
        if (i >= len(students)):
            break
        try:
            User.create_user(
                (students[i][0], students[i][3], students[i][1], students[i][2], 'standard'), db)
        except:
            pass
        # This will auto catch duplicate usernames so we dont need to check here.


def trainingInput(db: Database):
    if not os.path.exists('{}newtraining.txt'.format(apiFilePath)):
        return None
    file = open('{}newtraining.txt'.format(apiFilePath))
    trainings = []
    training = []
    for line in file:
        if line.strip() == '=====':
            trainings.append(training)
            training = []
            continue
        training.append(line.replace('\n', ''))
    # Function for inserting trainings will go here
    courses = db.execute("SELECT title FROM courses")
    for i in range(0, 10 - len(courses)):
        if (i >= len(trainings)):
            break
        if trainings[i][0] in str(courses):
            continue
        try:
            db.execute("INSERT INTO courses(title) VALUES(?)",
                       [trainings[i][0]])
        except:
            pass


def jobInput(db: Database):
    if not os.path.exists('{}newJobs.txt'.format(apiFilePath)):
        return None
    file = open('{}newJobs.txt'.format(apiFilePath))
    jobs = []
    job = []
    for line in file:
        if line.strip() == '=====':
            jobs.append(job)
            job = []
            continue
        job.append(line.replace('\n', ''))
    count = db.execute('SELECT title FROM jobs')
    for i in range(0, 10 - len(count)):
        if (i >= len(jobs)):
            break
        if jobs[i][0] in str(count):
            continue
        title = jobs[i][0]
        description = ''
        x = 1
        while(True):
            if jobs[i][x].strip() == '&&&':
                x += 1
                break
            description += jobs[i][x] + ' '
            x += 1
        description = description.rstrip()
        employer = jobs[i][x]
        x += 1
        name = jobs[i][x]
        x += 1
        location = jobs[i][x]
        x += 1
        salary = jobs[i][x]

        db.execute('INSERT INTO jobs(username, title, description, employer, location, salary) VALUES (?, ?, ?, ?, ?, ?)', [
                   name, title, description, employer, location, salary])


def jobOutput(db: Database):
    package = db.execute("SELECT * FROM jobs")
    #  title, a description, the employer, a location, and a salary.
    file = open('{}MyCollege_jobs.txt'.format(apiFilePath), 'w')
    output = ''
    for job in package:
        output += job[2] + '\n'
        output += job[3] + '\n'
        output += job[4] + '\n'
        output += job[5] + '\n'
        output += str(job[6]) + '\n'
        output += '=====\n'

    file.write(output)


def profileOutput(db: Database):
    file = open('{}MyCollege_profiles.txt'.format(apiFilePath), 'w')
    package = db.execute("SELECT * FROM profile")

    output = ''
    for profile in package:
        output += profile[0] + '\n'
        if profile[1]:
            output += profile[1] + '\n'  # Title
        if profile[2]:
            output += profile[2] + '\n'  # Major
        if profile[3]:
            output += profile[3] + '\n'  # Uni
        if profile[4]:
            output += profile[4] + '\n'  # About Me
        # Logic for getting experience if applicable, execute call here.
        res = db.execute(
            "SELECT * FROM job_experience WHERE username = ?", [profile[0]])
        for experience in res:
            output += experience[1] + '\n'
            output += experience[2] + '\n'
            output += experience[3] + '\n'
            output += experience[4] + '\n'
            output += experience[5] + '\n'
            output += experience[6] + '\n'
        if profile[5]:
            output += profile[5] + '\n'  # Education
        output += '=====\n'

    file.write(output)


def studentOutput(db: Database):
    file = open('{}MyCollege_users.txt'.format(apiFilePath), 'w')
    package = db.execute("SELECT username,tier FROM users")
    output = ""
    for user in package:
        output += user[0] + ' ' + user[1] + "\n"
    file.write(output)


def trainingOutput(db: Database):
    file = open('{}MyCollege_training.txt'.format(apiFilePath), 'w')
    package = db.execute("SELECT username FROM users")
    output = ""
    for user in package:
        output += user[0] + '\n'
        trainings = db.execute(
            "SELECT title FROM student_courses WHERE username = ? AND completed = True", [user[0]])
        for course in trainings:
            output += course[0] + '\n'
        output += '=====\n'
    file.write(output)


def appliedJobsOutput(db: Database):
    file = open('{}MyCollege_appliedJobs.txt'.format(apiFilePath), 'w')
    package = db.execute("SELECT title, job_id FROM jobs")
    output = ""
    for job in package:
        output += job[0] + '\n'
        applicants = db.execute(
            "SELECT * FROM user_applied_jobs WHERE job_id = ?", [job[1]])
        for user in applicants:
            output += user[0] + '\n'
            output += user[2] + '\n'
        output += "=====\n"

    file.write(output)


def savedJobsOutput(db: Database):
    file = open('{}MyCollege_savedJobs.txt'.format(apiFilePath), 'w')
    package = db.execute("SELECT username FROM users")
    output = ""
    for user in package:
        output += user[0] + '\n'
        savedJobs = db.execute(
            "SELECT job_id FROM user_interested_jobs WHERE username = ?", [user[0]])
        for job in savedJobs:
            jobName = db.execute(
                "SELECT title FROM jobs WHERE job_id = ?", [job[0]])
            output += jobName[0][0] + '\n'
        output += '=====\n'
    file.write(output)
