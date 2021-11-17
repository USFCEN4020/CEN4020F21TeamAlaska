import src.database_access
import src.User
import src.api

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

    f = open("{}studentAccounts.txt".format(apiFilePathTests), "w")
    for i in range(11): # generate 1 more than the allowed ammount
        f.write("darvelo{} daniel{} arvelo{}\n".format(i, i, i))
        f.write("Password1!\n")
        f.write("=====\n")

def test_student_accounts_input():
    src.api.studentInput(db)


    usernames = src.User.get_all_usernames("", db)

    # Test the number of students created
    count = len(usernames)
    assert count == 10

    # 
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
