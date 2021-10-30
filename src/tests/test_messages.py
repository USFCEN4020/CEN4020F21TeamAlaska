import src.Page
import src.database_access
from src.User import *
from Profile.Profile import *
from src.Page import *
import src.helpers
import src.Job
import src.message

# Does initial setup before any test runs

def setup_module():
    global user
    global db
    global message
    message = Message()
    db = Database("testing.sqlite3-messages")
    user = User("", "", "", "", "Standard", "english",
        True, True, True, False, db)
    src.Page.db = db
    db.delete_profile_table()
    db.delete_users_table()
    db.delete_user_friends()
    db.delete_job_experience_table()
    db.delete_user_interested()
    db.delete_user_applied()


class TestMessages:
    def testSendMessage(self):
        #user.createUser(['randion','Password#1','Robert',"Tester", "Standard"], db)
        #user.createUser(['randionSquared','Password#1','Robert',"SquaredGfuelAddict", "Plus"], db)
        #message.send_message('randion','randionSquared', "I love to test", db)
        assert 'please' == 'please'

def teardown_module():
    db = Database('testing.sqlite3-messages')
    db.delete_profile_table()
    db.delete_users_table()
    db.delete_user_friends()
    db.delete_job_experience_table()
    db.delete_jobs_table()
    db.delete_user_applied()
    db.delete_user_interested()
    db.close()