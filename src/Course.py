from src.database_access import database_access


class Course:
    def __init__():
        pass

    # Returns the status a user has on a course or None
    @staticmethod
    def getCourseStatus(username: str, title: str, db: database_access) -> bool:
        sql = "SELECT completed FROM student_courses WHERE username = ? AND title = ?;"
        return db.execute(sql, [username, title])

    @staticmethod
    def getAllCourseTitles(db: database_access) -> list:
        sql = "SELECT title FROM courses;"
        return db.execute(sql)

    @staticmethod
    def setCourseStatus(username: str, title: str, completed: bool, db: database_access) -> None:
        courseRegistedSQL = "SELECT * FROM student_courses WHERE username = ? AND title = ?"
        result = db.execute(courseRegistedSQL, [username, title])
        sql = ""
        # Create entry if user has never taken the course
        if result == []:
            sql = "INSERT INTO student_courses VALUES (?,?,?)"
            db.execute(sql, [username, title, completed])
        else:  # update course status if student has taken the course before
            sql = "UPDATE student_courses SET completed = ? WHERE username = ? AND title = ?"
            db.execute(sql, [completed, username, title])
