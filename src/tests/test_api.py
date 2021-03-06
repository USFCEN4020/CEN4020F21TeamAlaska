import Profile.Profile
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
        assert len(users) == len(src.User.get_all_usernames("", db))

# def resetforNathanTest():
#     db.delete_profile_table()
#     db.delete_users_table()
#     db.delete_user_friends()
#     db.delete_job_experience_table()
#     db.delete_user_interested()
#     db.delete_user_applied()
#     db.delete_notifications()
#     db.delete_courses()

#     # create test profile in database for profile output
#     db.execute("INSERT INTO profile(username,title,major,university_name,about_me,education) VALUES(?,?,?,?,?,?)",['nathan1','title1','major1','uni1','mememe','eduroam'])

#     # create test job in database for job output
#     db.execute('INSERT INTO jobs(username, title, description, employer, location, salary) VALUES (?, ?, ?, ?, ?, ?)',['nathan1','tester','teststhings','anderson','usf', 2])

#     # create test applied job in database for appliedjob output
#     db.execute('INSERT INTO user_applied_jobs(username,job_id,reason,status) VALUES (?,?,?,?)',['nathan1',0,'because','yes'])

#     # create test saved job in database for savedjob output
#     db.execute('INSERT INTO user_interested_jobs(username,job_id) VALUES(?,?)',['nathan1',0])

#     assert True


def test_profiles_output():
    # create profiles
    usernames = src.User.get_all_usernames("", db)
    for i, username in enumerate(usernames):
        values = [username[0], "title{}".format(i), "major{}".format(
            i), "university{}".format(i), "about{}".format(i), "education{}".format(i)]
        db.execute("INSERT INTO profile VALUES (?, ?, ?, ?, ?, ?)", values)

    src.api.profileOutput(db)

    filename = "{}MyCollege_profiles.txt".format(apiFilePathTests)
    assert exists(filename) == True

    with open(filename) as f:
        testfile = f.readlines()

        setUser = True
        user = None
        profileIDX = 0
        for i, line in enumerate(testfile):
            if setUser:
                user = db.execute(
                    "SELECT * FROM profile WHERE username = ?", [line[:-1]])[0]
                setUser = False
                profileIDX = 0
            elif line == "=====\n":
                setUser = True
            else:
                profileIDX += 1
                assert line[:-1] == user[profileIDX]


def test_job_output():
    src.api.jobOutput(db)

    filename = "{}MyCollege_jobs.txt".format(apiFilePathTests)
    assert exists(filename) == True

    with open(filename) as f:
        testfile = f.readlines()
        jobs = db.execute("SELECT * FROM jobs")

        # TODO: this uses the poster name, not the employer name
        jobIdx = 0
        elemIdx = 2
        for line in testfile:
            if line == "=====\n":
                jobIdx += 1
                elemIdx = 2
            else:
                assert line[:-1] == str(jobs[jobIdx][elemIdx])
                elemIdx += 1


def test_appliedjobs():
    # create applied jobs
    for i in range(5):
        db.execute('INSERT INTO user_applied_jobs(username,job_id,reason,status) VALUES (?,?,?,?)', [
                   'nathan{}'.format(i), i, 'because', 'yes'])
        db.execute('INSERT INTO user_applied_jobs(username,job_id,reason,status) VALUES (?,?,?,?)', [
                   'darvelo{}'.format(i), i, 'because', 'yes'])
    src.api.appliedJobsOutput(db)

    filename = "{}MyCollege_appliedJobs.txt".format(apiFilePathTests)
    assert exists(filename) == True

    with open(filename) as f:
        testfile = f.readlines()
        getJob = True
        userIdx = 0
        elemIdx = 0
        for line in testfile:
            if getJob:
                job = db.execute(
                    "SELECT title, UJ.username, reason FROM user_applied_jobs UJ, jobs J WHERE J.title = ? AND UJ.job_id = J.job_id", [line[:-1]])
                getJob = False
            elif line == "=====\n":
                elemIdx = 0
                getJob = True
                userIdx = 0
            else:
                assert line[:-1] == job[userIdx][elemIdx % 2 + 1]
                if elemIdx % 2 + 1 == 2:
                    userIdx += 1
                elemIdx += 1


def test_savedjobs():
    # save jobs
    for i in range(1, 5):
        db.execute('INSERT INTO user_interested_jobs VALUES(?,?)', [
                   'darvelo{}'.format(i+1), i])
        db.execute('INSERT INTO user_interested_jobs VALUES(?,?)', [
                   'darvelo1', i])
    src.api.savedJobsOutput(db)

    filename = "{}MyCollege_savedJobs.txt".format(apiFilePathTests)
    assert exists(filename) == True

    with open(filename) as f:
        testfile = f.readlines()

        newUser = True
        idx = 0
        for line in testfile:
            if newUser:
                savedJobs = db.execute(
                    "SELECT title FROM user_interested_jobs UI, jobs J WHERE UI.username = ? AND UI.job_id = J.job_id", [line[:-1]])
                print(savedJobs)
                newUser = False
            elif line == "=====\n":
                newUser = True
                idx = 0
            else:
                assert line[:-1] == savedJobs[idx][0]
                idx += 1


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
