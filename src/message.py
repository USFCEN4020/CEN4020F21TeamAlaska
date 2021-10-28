from src.database_access import database_access

class Message:
    @staticmethod
    def send_message(sender: str, receiver: str, body: str, db: database_access):
        # the status is either sent or read
        sql_post_messages_string = '''
            INSERT INTO messages (sender, receiver, body) VALUES (?, ?, ?)
        '''
        res =  db.execute(sql_post_messages_string, [sender, receiver, body])

    @staticmethod
    def get_my_messages(receiver: str, db: database_access):
        sql_get_messages = '''
            SELECT * FROM messages WHERE receiver = ? ORDER BY time_sent
        '''
        res = db.execute(sql_get_messages, [receiver])
        return res