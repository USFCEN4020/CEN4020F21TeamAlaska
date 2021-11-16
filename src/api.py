import os
import src.User as User
import src.database_access as Database
db = Database.database_access('InCollege.sqlite3')

def studentInput(db: Database):
    if not os.path.exists('./src/API-Files/studentAccounts.txt'):
        return None
    file = open('./src/API-Files/studentAccounts.txt')
    students = []
    student = []
    for line in file:
        if line.strip() == '=====':
            students.append(student)
            student = []
            continue
        for item in line.split(' '):
            student.append(item.replace('\n',''))
    
    # Insertion time, check for amount and do calculamations
    count = len(db.execute('SELECT * FROM jobs'))
    for i in range(0,10 - count):
        if (i >= len(students)):
            break
        User.create_user((students[i][0], students[i][3], students[i][1], students[i][2] ,'standard'))
        # This will auto catch duplicate usernames so we dont need to check here.
    
def trainingInput(db: Database):
    if not os.path.exists('./src/API-Files/newtraining.txt'):
        return None
    file = open('./src/API-Files/newtraining.txt')
    trainings = []
    training = []
    for line in file:
        if line.strip() == '=====':
            trainings.append(training)
            training = []
            continue
        training.append(line.replace('\n',''))
    print(trainings)
    # Function for inserting trainings will go here

def jobInput(db: Database):
    if not os.path.exists('./src/API-Files/newJobs.txt'):
        return None
    file = open('./src/API-Files/newJobs.txt')
    jobs = []
    job = []
    for line in file:
        if line.strip() == '=====':
            jobs.append(job)
            job = []
            continue
        job.append(line.replace('\n',''))
    count = db.execute('SELECT * FROM jobs')
    for i in range(0, 10 - count):
        if (i >= len(jobs)):
            break
        title = jobs[i][0]
        description = ''
        x = 1
        while(True):
            if jobs[i][x].strip() == '&&&':
                x += 1
                break
            description += jobs[i][x] + ' '
            x += 1
        employer = jobs[i][x]
        x+=1
        name = jobs[i][x]
        x+=1
        location = jobs[i][x]
        x+=1
        salary = jobs[i][x]

        db.execute('INSERT INTO jobs(username, title, description, employer, location, salary) VALUES (?, ?, ?, ?, ?, ?)', [name, title, description, employer, location, salary])

    print(jobs)

def jobOutput(db: Database):
    package = db.execute("SELECT * FROM jobs")
    #  title, a description, the employer, a location, and a salary.
    file = open('./src/API-Files/MyCollege_jobs.txt', 'w')
    output = ''
    for job in package:
        output += job[2] + '\n'
        output += job[3] + '\n'
        output += job[4] + '\n'
        output += job[5] + '\n'
        output += str(job[6]) + '\n'
        output += '====='

    file.write(output)

def profileOutput(db: Database):
    file = open('./src/API-Files/MyCollege_profiles.txt', 'w')
    package = db.execute("SELECT * FROM profile")
    
    output = ''
    for profile in package:
        output += profile[1] + '\n' # Title
        output += profile[2] + '\n' # Major
        output += profile[3] + '\n' # Uni
        output += profile[4] + '\n' # About Me
        # Logic for getting experience if applicable, execute call here.
        res = db.execute("SELECT * FROM job_experience WHERE username = ?",[profile[0]])
        for experience in res:
            output += experience[1] + '\n'
            output += experience[2] + '\n'
            output += experience[3] + '\n'
            output += experience[4] + '\n'
            output += experience[5] + '\n'
            output += experience[6] + '\n'
        output += profile[5] + '\n' # Education
        output += '====='

    file.write(output)
    
profileOutput(db)

def studentOutput(db: Database):
    print("Cant wait")

def trainingOutput(db: Database):
    print("Lets go")

def appliedJobsOutput(db: Database):
    print("YEE HAW")

def savedJobsOutput(db: Database):
    print("WOO")

