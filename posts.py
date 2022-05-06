from db import db


def get_posts_index():
    sql = """SELECT P.id, U.username, P.title, COUNT(R) as likes 
            FROM 
            users U LEFT JOIN posts P ON U.id = P.poster_id 
            LEFT JOIN ratings R ON P.id = R.post_id
            GROUP BY P.id, U.username, P.title"""
    return db.session.execute(sql).fetchall()

def search_for_posts(search_term):
    sql = """SELECT P.id, U.username, P.title, COUNT(R) as likes 
            FROM 
            users U LEFT JOIN posts P ON U.id = P.poster_id 
            LEFT JOIN ratings R ON P.id = R.post_id
            WHERE P.title LIKE :search_term
            GROUP BY P.id, U.username, P.title"""
    return db.session.execute(sql, {"search_term":'%' + search_term + '%'}).fetchall()


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
    sql = """SELECT P.title, P.body, U.username, COUNT(R) as likes
            FROM 
            users U, posts P
            LEFT JOIN ratings R ON P.id = R.post_id
            WHERE P.id=:id
            GROUP BY P.title, P.body, U.username"""
    result = db.session.execute(sql, {"id":id}).fetchone()

    return result
