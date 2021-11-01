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
    global db
    global message
    message = Message()
    db = Database("testing.sqlite3-messages")
    src.Page.db = db
    db.delete_profile_table()
    db.delete_users_table()
    db.delete_user_friends()
    db.delete_job_experience_table()
    db.delete_user_interested()
    db.delete_user_applied()


class TestMessages:
    def setUp(self):
        # create_user(('randion','Password#1','Robert',"Tester", "standard"), db)
        # create_user(('randionSquared','Password#1','Robert',"SquaredGfuelAddict", "plus"), db)
        pass

    def testSendMessageNonFriendPlus(self):
        create_user(('randion','Password#1','Robert',"Tester", "standard"), db)
        u2 = create_user(('randionSquared','Password#1','Robert',"SquaredGfuelAddict", "plus"), db)

        page = src.Page.Page()
        page.user = u2
        # src.Page.back_option = lambda s: output.append('Done {}'.format(s))
        # page.back_option = lambda s: output.append('Done {}'.format(s))
        output = []
        input = ["2","1","1","1"]
        def mock_input(s):
            return input.pop(0)
        src.Page.print = lambda s: output.append(s)
        src.Page.input = mock_input
        src.helpers.input = mock_input
        page.messages_page()
        
        assert output == [
            "1 - Inbox\n2 - Send a message\n0 - Back to previous\nEnter a choice: ",
            "1 - randion",
        ]
    #        message.send_message('randion','randionSquared', "I love to test", db)
    def testSendMessage(self):
        print('qait')

def teardown_module():
    db = Database('testing.sqlite3-messages')
    db.delete_profile_table()
    db.delete_users_table()
    db.delete_user_friends()
    db.delete_job_experience_table()
    db.delete_jobs_table()
    db.delete_user_applied()
    db.delete_user_interested()
    db.delete_messages()
    db.close()