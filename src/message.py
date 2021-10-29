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

    @staticmethod
    def delete_message(message_id: int, db: database_access):
        sql_delete_message = '''
            DELETE FROM messages WHERE message_id = ?
        '''
        db.execute(sql_delete_message, [message_id])
        check = 'SELECT COUNT(*) FROM messages WHERE message_id = ?'
        # checking if the delete was successful
        res = db.execute(check, [message_id])
        return True if res[0][0] == 0 else False