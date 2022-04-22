from db import db

def get_post_comments(post_id):
    sql = """SELECT U.username, C.comment FROM comments C, users U
            WHERE C.post_id=:post_id AND U.id = C.commenter_id
            ORDER BY C.id"""
    return db.session.execute(sql, {"post_id":post_id}).fetchall()

def create_new_comment(commenter_id, post_id, comment):
    try:
        sql = """INSERT INTO comments (commenter_id, post_id, comment) 
                VALUES (:commenter_id, :post_id, :comment)"""
        db.session.execute(sql, {"commenter_id":commenter_id, "post_id":post_id, "comment":comment})
        print("muttei tähän?")
        db.session.commit()
    except:
        print("2")
        return False

    return True