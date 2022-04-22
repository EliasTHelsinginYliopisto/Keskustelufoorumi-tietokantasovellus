from db import db


def get_posts_index():
    sql = """SELECT P.id, U.username, P.title FROM posts P, users U
            WHERE U.id = P.poster_id"""
    return db.session.execute(sql).fetchall()

def create_new_post(title, body, poster_id):
    try:
        sql = """INSERT INTO posts (title, body, poster_id)
                VALUES (:title, :body, :poster_id) RETURNING id"""
        result = db.session.execute(sql, {"title":title, "body":body, "poster_id":poster_id})
        post_id = result.fetchone()[0]
        db.session.commit()
        return post_id
    except:
        return False

def get_post_content(post_id):
    id = post_id
    sql = """SELECT P.title, P.body, U.username
            FROM posts P, users U  WHERE P.id=:id"""
    result = db.session.execute(sql, {"id":id}).fetchone()

    return result
