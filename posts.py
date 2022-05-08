from db import db


def get_posts_index():
    sql = """SELECT P.id, U.username, P.title, U.id as userid, COUNT(R) as likes 
            FROM 
            users U LEFT JOIN posts P ON U.id = P.poster_id 
            LEFT JOIN ratings R ON P.id = R.post_id
            WHERE P.visible = 1
            GROUP BY P.id, U.username, P.title, U.id"""
    return db.session.execute(sql).fetchall()

def get_my_posts(user_id):
    sql = """SELECT P.id, U.username, P.title, P.visible, COUNT(R) as likes 
            FROM 
            users U LEFT JOIN posts P ON U.id = P.poster_id 
            LEFT JOIN ratings R ON P.id = R.post_id
            WHERE P.poster_id=:user_id AND NOT P.visible = 2
            GROUP BY P.id, U.username, P.title"""
    return db.session.execute(sql, {"user_id":user_id}).fetchall()

def search_for_posts(search_term):
    sql = """SELECT P.id, U.username, P.title, COUNT(R) as likes 
            FROM 
            users U LEFT JOIN posts P ON U.id = P.poster_id 
            LEFT JOIN ratings R ON P.id = R.post_id
            WHERE P.title LIKE :search_term AND P.visible = 1
            GROUP BY P.id, U.username, P.title"""
    return db.session.execute(sql, {"search_term":'%' + search_term + '%'}).fetchall()


def create_new_post(title, body, poster_id):
    try:
        sql = """INSERT INTO posts (title, body, poster_id, visible)
                VALUES (:title, :body, :poster_id, 1) RETURNING id"""
        result = db.session.execute(sql, {"title":title, "body":body, "poster_id":poster_id})
        post_id = result.fetchone()[0]
        db.session.commit()
        return post_id
    except:
        return False

def get_post_content(post_id):
    id = post_id
    sql = """SELECT P.title, P.body, U.username, U.id as userid, COUNT(R) as likes
            FROM 
            users U LEFT JOIN posts P ON U.id = P.poster_id
            LEFT JOIN ratings R ON P.id = R.post_id
            WHERE P.id=:id
            GROUP BY P.title, P.body, U.username, U.id"""
    result = db.session.execute(sql, {"id":id}).fetchone()

    return result

def edit_post(post_id, body):
    sql = """UPDATE posts SET body=:body WHERE id=:post_id"""
    db.session.execute(sql, {"body":body, "post_id":post_id})
    db.session.commit()

def toggle_post_visibility(post_id):
    sql = """SELECT visible FROM posts where id=:post_id"""
    result = db.session.execute(sql, {"post_id":post_id}).fetchone()
    if result[0] == 1:
        sql = """UPDATE posts SET visible=0 WHERE id=:post_id"""
        db.session.execute(sql, {"post_id":post_id})
        db.session.commit()
    else:
        sql = """UPDATE posts SET visible=1 WHERE id=:post_id"""
        db.session.execute(sql, {"post_id":post_id})
        db.session.commit()

def delete_post(post_id):
    sql = """UPDATE posts
            SET title= 'Poistettu Keskustelu', body='Poistettu', visible=2
            WHERE id=:post_id"""
    db.session.execute(sql, {"post_id":post_id})
    db.session.commit()