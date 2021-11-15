import src.database_access
import src.Page
import src.PostedJob
import src.Job


def resetFunctions():
    src.Page.input = input
    src.Page.print = print


class TestJobPosting():
    page = src.Page.Page()
    page.user.username = "General Kenobi The Negotiator"
    db_name = "testing.sqlite3"
    db = src.database_access.database_access(db_name)
    src.Page.db = db

    def clearTables(self):
        self.db.delete_user_applied()
        self.db.delete_user_interested()

    def testPostValidJob(self):
        input_values = ['Worm Farmer', 'Farming worms',
                        'WormsRUs', 'Bikini Bottom', '20000']
        output = []

        def mock_input(s):
            return input_values.pop(0)
        src.Page.input = mock_input
        src.Page.print = lambda s: output.append(s)
        self.page.postjob()
        resetFunctions()
        assert output == [
            "Thanks your job was posted! Returning to the previous menu..."
        ]

    def testPostInvalidJob(self):
        input_values = ['Worm Farmer0', 'Farming worms',
                        'WormsRUs', 'Bikini Bottom', 'Shmeckle', '20000']
        output = []

        def mock_input(s):
            output.append(s)
            return input_values.pop(0)
        src.Page.input = mock_input
        src.Page.print = lambda s: output.append(s)
        self.page.postjob()
        resetFunctions()
        assert output == [
            "Please enter the job's title: ",
            "Please enter a description of the job: ",
            "Who is the employer of the job? ",
            "Where is this job located? ",
            "Please estimate the salary of the job (only numbers): ",
            "Not a valid number. Try again.",
            "Please estimate the salary of the job (only numbers): ",
            "Thanks your job was posted! Returning to the previous menu..."
        ]

    def testJobPostLimit(self):
        for i in range(1, 10):
            input_values = [
                'Worm Farmer' + str(i), 'Farming worms', 'WormsRUs', 'Bikini Bottom', '20000']

            def mock_input(s):
                return input_values.pop(0)
            src.Page.input = mock_input
            self.page.postjob()
        output = []
        input_values = ['Not going to post', 'Farming worms',
                        'WormsRUs', 'Bikini Bottom', '20000']

        def mock_input(s):
            return input_values.pop(0)
        src.Page.input = mock_input
        src.Page.print = lambda s: output.append(s)
        self.page.postjob()
        resetFunctions()
        assert output == [
            'There are already 10 jobs. Please try again later\n'
        ]

    def testDatabaseJobPrint(self):
        output = []
        src.database_access.print = lambda s: output.append(s)
        self.db.print_jobs()
        print(output)
        assert output == [(1, 'General Kenobi The Negotiator', 'Worm Farmer', 'Farming worms', 'WormsRUs', 'Bikini Bottom', 20000.0), (2, 'General Kenobi The Negotiator', 'Worm Farmer0', 'Farming worms', 'WormsRUs', 'Bikini Bottom', 20000.0), (3, 'General Kenobi The Negotiator', 'Worm Farmer1', 'Farming worms', 'WormsRUs', 'Bikini Bottom', 20000.0), (4, 'General Kenobi The Negotiator', 'Worm Farmer2', 'Farming worms', 'WormsRUs', 'Bikini Bottom', 20000.0), (5, 'General Kenobi The Negotiator', 'Worm Farmer3', 'Farming worms', 'WormsRUs', 'Bikini Bottom', 20000.0),
                          (6, 'General Kenobi The Negotiator', 'Worm Farmer4', 'Farming worms', 'WormsRUs', 'Bikini Bottom', 20000.0), (7, 'General Kenobi The Negotiator', 'Worm Farmer5', 'Farming worms', 'WormsRUs', 'Bikini Bottom', 20000.0), (8, 'General Kenobi The Negotiator', 'Worm Farmer6', 'Farming worms', 'WormsRUs', 'Bikini Bottom', 20000.0), (9, 'General Kenobi The Negotiator', 'Worm Farmer7', 'Farming worms', 'WormsRUs', 'Bikini Bottom', 20000.0), (10, 'General Kenobi The Negotiator', 'Worm Farmer8', 'Farming worms', 'WormsRUs', 'Bikini Bottom', 20000.0)]
        resetFunctions()

    def test_get_job_by_id(self):
        expected = src.Job.Job(1, 'General Kenobi The Negotiator', 'Worm Farmer',
                               'Farming worms', 'WormsRUs', 'Bikini Bottom', 20000.0)
        actual = src.Job.Job.get_job_by_id(1, self.db)

        assert expected == actual

        # Test job does not exist
        expected = False
        actual = actual = src.Job.Job.get_job_by_id(-1, self.db)
        assert expected == actual

    def test_get_my_postings(self):
        # Test user with jobs
        expected = [src.Job.Job(1, 'General Kenobi The Negotiator', 'Worm Farmer', 'Farming worms', 'WormsRUs', 'Bikini Bottom', 20000.0), src.Job.Job(2, 'General Kenobi The Negotiator', 'Worm Farmer0', 'Farming worms', 'WormsRUs', 'Bikini Bottom', 20000.0), src.Job.Job(3, 'General Kenobi The Negotiator', 'Worm Farmer1', 'Farming worms', 'WormsRUs', 'Bikini Bottom', 20000.0), src.Job.Job(4, 'General Kenobi The Negotiator', 'Worm Farmer2', 'Farming worms', 'WormsRUs', 'Bikini Bottom', 20000.0), src.Job.Job(5, 'General Kenobi The Negotiator', 'Worm Farmer3', 'Farming worms', 'WormsRUs', 'Bikini Bottom', 20000.0),
                    src.Job.Job(6, 'General Kenobi The Negotiator', 'Worm Farmer4', 'Farming worms', 'WormsRUs', 'Bikini Bottom', 20000.0), src.Job.Job(7, 'General Kenobi The Negotiator', 'Worm Farmer5', 'Farming worms', 'WormsRUs', 'Bikini Bottom', 20000.0), src.Job.Job(8, 'General Kenobi The Negotiator', 'Worm Farmer6', 'Farming worms', 'WormsRUs', 'Bikini Bottom', 20000.0), src.Job.Job(9, 'General Kenobi The Negotiator', 'Worm Farmer7', 'Farming worms', 'WormsRUs', 'Bikini Bottom', 20000.0), src.Job.Job(10, 'General Kenobi The Negotiator', 'Worm Farmer8', 'Farming worms', 'WormsRUs', 'Bikini Bottom', 20000.0)]
        actual = src.Job.Job.get_my_postings(
            "General Kenobi The Negotiator", self.db)
        assert expected == actual

        # Test user does not exist
        actual = src.Job.Job.get_my_postings("NonExistentUser", self.db)
        assert actual == []

    def test_print_full_job(self):
        job = src.Job.Job(1, 'General Kenobi The Negotiator', 'Worm Farmer',
                          'Farming worms', 'WormsRUs', 'Bikini Bottom', 20000.0)
        output = []
        src.Job.print = lambda s: output.append(s)
        job.print_full_job()

        expected = ['\n*Worm Farmer Job Posting*\n' +
                    'Job Description: Farming worms\n' +
                    'Location: Bikini Bottom\n' +
                    'Expected Salary: 20000.0\n' +
                    'Posted By: WormsRUs']
        assert output == expected

    def test_delete_job(self):
        expected = [src.Job.Job(2, 'General Kenobi The Negotiator', 'Worm Farmer0', 'Farming worms', 'WormsRUs', 'Bikini Bottom', 20000.0), src.Job.Job(3, 'General Kenobi The Negotiator', 'Worm Farmer1', 'Farming worms', 'WormsRUs', 'Bikini Bottom', 20000.0), src.Job.Job(4, 'General Kenobi The Negotiator', 'Worm Farmer2', 'Farming worms', 'WormsRUs', 'Bikini Bottom', 20000.0), src.Job.Job(5, 'General Kenobi The Negotiator', 'Worm Farmer3', 'Farming worms', 'WormsRUs', 'Bikini Bottom', 20000.0),
                    src.Job.Job(6, 'General Kenobi The Negotiator', 'Worm Farmer4', 'Farming worms', 'WormsRUs', 'Bikini Bottom', 20000.0), src.Job.Job(7, 'General Kenobi The Negotiator', 'Worm Farmer5', 'Farming worms', 'WormsRUs', 'Bikini Bottom', 20000.0), src.Job.Job(8, 'General Kenobi The Negotiator', 'Worm Farmer6', 'Farming worms', 'WormsRUs', 'Bikini Bottom', 20000.0), src.Job.Job(9, 'General Kenobi The Negotiator', 'Worm Farmer7', 'Farming worms', 'WormsRUs', 'Bikini Bottom', 20000.0), src.Job.Job(10, 'General Kenobi The Negotiator', 'Worm Farmer8', 'Farming worms', 'WormsRUs', 'Bikini Bottom', 20000.0)]
        assert src.Job.Job.delete_job(1, self.db) == True

        actual = src.Job.Job.get_my_postings(
            'General Kenobi The Negotiator', self.db)
        assert actual == expected

    def test_apply_job(self):
        # Test no applied jobs
        assert src.Job.Job.get_applied_jobs("darvelo", self.db) == False

        # Test applied job has new item
        src.Job.Job.apply_job("darvelo", 2, self.db)
        assert src.Job.Job.get_applied_jobs("darvelo", self.db) == [
            src.Job.Job.get_job_by_id(2, self.db)]

    def test_add_interested(self):
        # Test no interested jobs
        assert src.Job.Job.get_interested_jobs("darvelo", self.db) == False
        # Test interested job has new item
        src.Job.Job.add_interested("darvelo", 3, self.db)
        assert src.Job.Job.get_interested_jobs(
            "darvelo", self.db) == [src.Job.Job.get_job_by_id(3, self.db)]

    def testCleanUp(self):  # Teardown
        self.db.delete_jobs_table()
        self.db.delete_user_applied()
        self.db.delete_user_interested()
        # self.db.close()
        assert True == True
