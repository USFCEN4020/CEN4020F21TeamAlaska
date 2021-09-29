import sqlite3


class database_access:
    # constructor establsihes connection and creates tables
    def __init__(self, db_name):
        self.db = sqlite3.connect(db_name)

        sql_create_users_table = ''' CREATE TABLE IF NOT EXISTS users (
            username text PRIMARY KEY,
            password text NOT NULL,
            firstname TEXT NOT NULL,
            lastname TEXT NOT NULL
        )
    '''
        sql_create_jobs_table = ''' CREATE TABLE IF NOT EXISTS jobs (
            username text NOT NULL,
            title text NOT NULL,
            description text NOT NULL,
            employer text NOT NULL,
            location text NOT NULL,
            salary real NOT NULL,
            PRIMARY KEY(username,title)
        )
    '''

        c = self.db.cursor()
        c.execute(sql_create_users_table)
        c.execute(sql_create_jobs_table)
        self.db.commit()

    # To select and print all tables
    def print_users(self):
        c = self.db.cursor()
        c.execute('SELECT * FROM users')
        # view all selected records
        data = c.fetchall()
        for row in data:
            print(row)

    def print_jobs(self):
        c = self.db.cursor()
        c.execute('SELECT * FROM jobs')
        # view all selected jobs
        data = c.fetchall()
        for row in data:
            print(row)

    # if you want to clear the table(s)
    def delete_users_table(self):
        c = self.db.cursor()
        sql = 'DELETE FROM users'
        c.execute(sql)
        self.db.commit()

    def delete_jobs_table(self):
        c = self.db.cursor()
        sql = 'DELETE FROM jobs'
        c.execute(sql)
        self.db.commit()

    def execute(self, sql, params=[]):
        c = self.db.cursor()
        c.execute(sql, params)
        self.db.commit()

        return c.fetchall()

    def commit(self):
        self.db.commit()

    def close(self):
        self.db.close()
