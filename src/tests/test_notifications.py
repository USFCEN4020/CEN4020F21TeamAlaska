import src.Page
import src.database_access as Database
import src.Notification as Notification
from src.User import *
from Profile.Profile import *
from src.Page import *
import src.helpers
import src.Job
import src.message


def resetFunctions():
    src.Page.input = input
    src.Page.print = print


class Test_notifications():
    db = Database("testing.sqlite3-notifications")
    page = src.Page.Page()
    page.user.username = "Jirudi"
    page.user.authorized = True
    src.Page.db = db
    create_user(('Jirudi', 'Dana123$', 'dana', "jirudi", "standard"), db)

    def test_post_job_notification(self):
        temp = ['Awesome Dev', 'Dev Job', 'Me', 'Here', '100000']
        title = temp[0]
        output = []

        def mock_input(s):
            return temp.pop(0)
        src.Page.input = mock_input
        src.Page.print = lambda s: output.append(s)
        self.page.postjob()
        resetFunctions()

        sql = 'SELECT * FROM notifications WHERE username = ?'
        expected_res = ("Jirudi", "A new job, " + title + " has been posted")
        res = self.db.execute(sql, [self.page.user.username])[0]
        assert res == expected_res

    def test_profile_notification(self):
        output = []
        src.Page.print = lambda s: output.append(s)
        self.page.notifyCreateProfile()
        assert output == ["Don't forget to create a profile.\n"]

    def test_jobs_applied(self):
        output = []
        src.Page.print = lambda s: output.append(s)
        self.page.notify_jobs_applied()
        assert output == ["You have currently applied for 0 jobs"]

    def test_notify_messages(self):
        sql_post_messages_string = '''
            INSERT INTO messages (sender, receiver, body) VALUES (?, ?, ?)
        '''
        self.db.execute(sql_post_messages_string, [
                        "foo", self.page.user.username, "Hello World!"])
        output = []
        src.Page.print = lambda s: output.append(s)
        self.page.notifyMessage(self.db)
        assert output == [
            "You have 1 new messages! Go to the messages tab to view."]


def teardown_module():
    db = Database('testing.sqlite3-notifications')
    db.delete_notifications()
    db.delete_jobs_table()
    db.delete_users_table()
    db.delete_messages()
    db.close()
    assert True == True
