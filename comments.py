from db import db

def get_post_comments(post_id):
    sql = """SELECT U.username, C.comment, C.id AS comment_id, C.commenter_id AS user_id 
            FROM comments C, users U
            WHERE C.post_id=:post_id AND U.id = C.commenter_id AND C.visible = 1
            ORDER BY C.id"""
    return db.session.execute(sql, {"post_id":post_id}).fetchall()

def create_new_comment(commenter_id, post_id, comment):
    try:
        sql = """INSERT INTO comments (commenter_id, post_id, comment, visible) 
                VALUES (:commenter_id, :post_id, :comment, 1)"""
        db.session.execute(sql, {"commenter_id":commenter_id, "post_id":post_id, "comment":comment})
        db.session.commit()
    except:
        return False

    return True

def delete_comment(comment_id):
    sql = """UPDATE comments
            SET comment='deleted', visible='2'
            WHERE id=:comment_id"""
    db.session.execute(sql, {"comment_id":comment_id})
    db.session.commit()