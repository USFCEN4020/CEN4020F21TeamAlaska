from src.database_access import database_access


class Notification:
    def __init__(self, username: str, content: str):
        self.username = username
        self.content = content

    @staticmethod
    def get_notifications(username: str, db: database_access):
        sql = 'SELECT * FROM notifications WHERE username = ?'
        return db.execute(sql, [username])

    @staticmethod
    def add_notification(username: str, content: str, db: database_access):
        sql = 'INSERT INTO notifications VALUES (?, ?)'
        db.execute(sql, [username, content])

    @staticmethod
    def delete_notifications(username: str, db: database_access):
        sql = 'DELETE FROM notifications WHERE username = ?'
        db.execute(sql, [username])
