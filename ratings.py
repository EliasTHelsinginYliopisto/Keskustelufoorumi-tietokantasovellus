from db import db

def create_rating_on_post(rater_id, post_id):
    sql = """SELECT COUNT(*) FROM ratings WHERE
            rater_id=:rater_id AND post_id=:post_id"""
    result = db.session.execute(sql, {"rater_id":rater_id, "post_id":post_id}).fetchone()
    if result[0] == 1:
        sql = """DELETE FROM ratings WHERE
            rater_id=:rater_id AND post_id=:post_id"""
        db.session.execute(sql, {"rater_id":rater_id, "post_id":post_id})
        db.session.commit()
        return True
    else:
        sql = """INSERT INTO ratings (rater_id, post_id)
                VALUES (:rater_id, :post_id)"""
        db.session.execute(sql, {"rater_id":rater_id, "post_id":post_id})
        db.session.commit()
        return True
    

def create_rating_on_comment(rater_id, comment_id):
    sql = """INSERT INTO ratings (rater_id, comment_id)
            VALUES (:rater_id, :comment_id)"""
    db.session.execute(sql, {"rater_id":rater_id, "comment_id":comment_id})
    db.session.commit()

def count_votes_on_post(post_id):
    sql = """SELECT COUNT(*) as total,
            FROM ratings WHERE post_id=:post_id"""
    result = db.session.execute(sql, {"post_id":post_id}).fetchone()
    return result

def count_votes_on_comment(comment_id):
    sql = """SELECT COUNT(*) as total,
            FROM ratings WHERE comment_id=:comment_id"""
    result = db.session.execute(sql, {"post_id":comment_id}).fetchone()
    return result
