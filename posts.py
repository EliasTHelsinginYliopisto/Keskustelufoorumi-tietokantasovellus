from db import db


def get_posts_index():
    sql = "SELECT id, poster_name, title FROM posts"
    return db.session.execute(sql).fetchall()

def create_new_post(title, body, poster_name):
    sql = """INSERT INTO posts (title, body, poster_name)
             VALUES (:title, :body, :poster_name)"""
    post_id = db.session.execute(sql, {"title":title, "body":body, "poster_name":poster_name})
    db.session.commit()
    return post_id

def get_post_content(post_id):
    sql = """SELECT title, body, poster_name
            FROM posts"""
    return db.session.execute(sql).fetchone()