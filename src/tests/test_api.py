import src.database_access
import src.User
import src.api
import src.PostedJob
import src.Course

from os.path import exists

# Does initial setup before any test runs

apiFilePathTests = "./src/API-Files/testing/"


def setup_module():
    # setup db
    global db
    db = src.database_access.database_access("testing.sqlite3")
    db.delete_profile_table()
    db.delete_users_table()
    db.delete_user_friends()
    db.delete_job_experience_table()
    db.delete_user_interested()
    db.delete_user_applied()
    db.delete_notifications()
    db.delete_courses()

    src.api.apiFilePath = apiFilePathTests

    # create test file for student input
    f = open("{}studentAccounts.txt".format(apiFilePathTests), "w")
    for i in range(11):  # generate 1 more than the allowed ammount
        f.write("darvelo{} daniel{} arvelo{}\n".format(i, i, i))
        f.write("Password1!\n")
        f.write("=====\n")

    # create test file for job input
    f = open("{}newJobs.txt".format(apiFilePathTests), "w")
    for i in range(11):
        f.write("title{}\n".format(i))
        f.write("This is my multi line description\nit continues down here\n&&&\n")
        f.write("posterName{}\n".format(i))
        f.write("employerName{}\n".format(i))
        f.write("location{}\n".format(i))
        f.write("{}\n".format(i*1000))
        f.write("=====\n")

    # Create test file for training input
    f = open("{}newtraining.txt".format(apiFilePathTests), "w")
    for i in range(5):
        f.write("title{}\n".format(i))
        f.write("=====\n")

def test_student_accounts_input():
    src.api.studentInput(db)

    usernames = src.User.get_all_usernames("", db)

    # Test the number of students created
    count = len(usernames)
    assert count == 10

    for i, username in enumerate(usernames):
        username = username[0]
        userExpected = src.User.User(
            "darvelo{}".format(i),
            "Password1!",
            "daniel{}".format(i),
            "arvelo{}".format(i),
            "standard",
            "english",
            True,
            True,
            True,
            None,
            True,
            db
        )
        userActual = src.User.get_user_by_username(username, db)
        assert userActual == userExpected


def test_job_input():
    src.api.jobInput(db)

    jobs = db.execute('SELECT * FROM jobs')
    assert len(jobs) == 10

    for i, job in enumerate(jobs):

        expected = (
            i+1,
            "employerName{}".format(i),
            "title{}".format(i),
            "This is my multi line description it continues down here",
            "posterName{}".format(i),
            "location{}".format(i),
            i*1000
        )

        assert job[0] == expected[0]
        assert job[1] == expected[1]
        assert job[2] == expected[2]
        assert job[3] == expected[3]
        assert job[4] == expected[4]
        assert job[5] == expected[5]


def test_training_input():
    src.api.trainingInput(db)

    trainings = src.Course.Course.getAllCourseTitles(db)

    assert len(trainings) == 5

    for i, training in enumerate(trainings):
        expected = "title{}".format(i)

        assert training[0] == expected


def test_user_output():
    src.api.studentOutput(db)

    # assert file was created
    filename = "{}MyCollege_users.txt".format(apiFilePathTests)
    assert exists(filename) == True

    usernames = src.User.get_all_usernames("", db)

    with open(filename) as f:
        lines = f.readlines()

        for i, line in enumerate(lines):
            assert line == "{} {}\n".format(usernames[i][0], "standard")


def test_training_output():
    src.api.trainingOutput(db)

    # assert file was created
    filename = "{}MyCollege_training.txt".format(apiFilePathTests)
    assert exists(filename) == True

    with open(filename) as f:
        lines = f.readlines()

        users = []
        setUser = True
        for line in lines:
            if setUser:
                user = line[:-1]
                users.append(user)
                setUser = False
            elif line == "=====\n":
                setUser = True
            else:
                assert src.Course.Course.getCourseStatus(
                    user, line[:-1], db)[0][0] == True

        # Check that all users are accounted for
        print(users)
        assert len(users) == len(src.User.get_all_usernames("", db))

def resetforNathanTest():
    db.delete_profile_table()
    db.delete_users_table()
    db.delete_user_friends()
    db.delete_job_experience_table()
    db.delete_user_interested()
    db.delete_user_applied()
    db.delete_notifications()
    db.delete_courses()
    
    # create test profile in database for profile output
    db.execute("INSERT INTO profile(username,title,major,university_name,about_me,education) VALUES(?,?,?,?,?,?)",['nathan1','title1','major1','uni1','mememe','eduroam'])

    # create test job in database for job output
    db.execute('INSERT INTO jobs(username, title, description, employer, location, salary) VALUES (?, ?, ?, ?, ?, ?)',['nathan1','tester','teststhings','anderson','usf', 2])

    # create test applied job in database for appliedjob output
    db.execute('INSERT INTO user_applied_jobs(username,job_id,reason,status) VALUES (?,?,?,?)',['nathan1',0,'because','yes'])

    # create test saved job in database for savedjob output
    db.execute('INSERT INTO user_interested_jobs(username,job_id) VALUES(?,?)',['nathan1',0])

    assert True

def test_profiles_output():
    src.api.profileOutput(db)

    filename = "{}MyCollege_profiles.txt".format(apiFilePathTests)
    assert exists(filename) ==  True

    with open(filename) as f:
        testfile = f.readlines()
        correctprofile = db.execute("SELECT * FROM profile")

        for i in range(6):
            assert testfile[i] == correctprofile[0][i] + '\n'


def test_job_output():
    src.api.jobOutput(db)

    filename = "{}MyCollege_jobs.txt".format(apiFilePathTests)
    assert exists(filename) ==  True

    with open(filename) as f:
        testfile = f.readlines()
        correctjob = db.execute("SELECT * FROM jobs")

        for i in range(2,6):
            assert testfile[i] == correctjob[0][i] + '\n'
        else:
            assert testfile[6] == str(correctjob[0][6]) + '\n'

def test_appliedjobs():
    src.api.appliedJobsOutput(db)

    filename = "{}MyCollege_appliedJobs.txt".format(apiFilePathTests)
    assert exists(filename) ==  True

    with open(filename) as f:
        testfile = f.readlines()
        correctjob = db.execute("SELECT title, job_id FROM jobs")
        correctappliedjob = db.execute("SELECT * FROM users_applied_jobs WHERE job_id = ?", [correctjob[1]])
        
        assert testfile[0] == correctjob[0][0] + '\n'
        assert testfile[1] == correctappliedjob[0][0] + '\n'
        assert testfile[2] == correctappliedjob[0][2] + '\n'
        

def test_savedjobs():
    src.api.savedJobsOutput(db)

    filename = "{}MyCollege_savedJobs.txt".format(apiFilePathTests)
    assert exists(filename) ==  True

    with open(filename) as f:
        testfile = f.readlines()
        correctuser = db.execute("SELECT username FROM users")
        correctsavedjobs = db.execute("SELECT job_id FROM user_interested_jobs WHERE username = ?", [correctuser[0]])
        correctjobname = db.execute("SELECT title FROM jobs WHERE job_id = ?", [correctsavedjobs[0]])
        
        assert testfile[0] == correctuser[0][0] + '\n'
        assert testfile[1] == correctjobname[0][0] + '\n'
                

def teardown_module():
    db.delete_profile_table()
    db.delete_users_table()
    db.delete_user_friends()
    db.delete_job_experience_table()
    db.delete_jobs_table()
    db.delete_user_applied()
    db.delete_user_interested()
    db.delete_notifications()
    db.delete_courses()
    db.close()
