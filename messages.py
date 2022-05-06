from db import db

def create_message(message, group_id, sender_id):
        sql = """INSERT INTO messages (sender_id, group_id, content)
                VALUES (:sender_id, :group_id, :content)"""
        db.session.execute(sql, {"sender_id":sender_id, "group_id":group_id, "content":message})
        db.session.commit()

def get_group_messages(group_id):
    sql = """SELECT U.username, M.content FROM messages M, users U
        WHERE M.group_id=:group_id AND U.id = M.sender_id
        ORDER BY M.id"""
    return db.session.execute(sql, {"group_id":group_id}).fetchall()

