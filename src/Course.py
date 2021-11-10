from database_access import database_access


class Course:
    def __init__():
        pass

    # Returns the status a user has on a course or None
    @staticmethod
    def getCourseStatus(username: str, title: str, db: database_access):
        sql = "SELECT status FROM student_courses WHERE username = ? AND title = ?;"
        return db.execute(sql, [username, title])[0]

    @staticmethod
    def getAllCourseTitles(db: database_access):
        sql = "SELECT title FROM courses;"
        return db.execute(sql)
