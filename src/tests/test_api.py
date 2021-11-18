import src.database_access
import src.User
import src.api
import src.PostedJob

# Does initial setup before any test runs


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

    apiFilePathTests = "./src/API-Files/testing/"
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

        print(job)
        assert job[0] == expected[0]
        assert job[1] == expected[1]
        assert job[2] == expected[2]
        assert job[3] == expected[3]
        assert job[4] == expected[4]
        assert job[5] == expected[5]


def teardown_module():
    db.delete_profile_table()
    db.delete_users_table()
    db.delete_user_friends()
    db.delete_job_experience_table()
    db.delete_jobs_table()
    db.delete_user_applied()
    db.delete_user_interested()
    db.delete_notifications()
    db.close()
