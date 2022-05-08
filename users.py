from db import db
from flask import session, abort
from werkzeug.security import check_password_hash, generate_password_hash
from secrets import token_hex

def login(username, password):
    sql = "SELECT id, username, role, password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:   
        if check_password_hash(user.password, password):
            session["user_username"] = user.username
            session["user_id"] = user.id
            session["user_role"] = user.role
            session["csrf_token"] = token_hex(16)
            return True
        else:
            return False


def register(username, password, role):
    if username == "Anonyymi":
        return False

    hash_value = generate_password_hash(password)
    try:
        if role == 0:
            sql = """INSERT INTO users (username, password, role) 
                    VALUES (:username, :password, 0)"""
            db.session.execute(sql, {"username":username, "password":hash_value})
            db.session.commit()
        else:
            sql = """INSERT INTO users (username, password, role) 
                    VALUES (:username, :password, 1)"""
            db.session.execute(sql, {"username":username, "password":hash_value})
            db.session.commit()

    except:
        return False
    return login(username, password)
    
def logout():
    del session["user_username"]
    del session["user_id"]
    del session["user_role"]

def require_role(role):
    
    if session.get("user_role", -1) == None:
        abort(403)
    elif session.get("user_role", -1) >= role:
        return
    abort(403)

def check_csrf(csrf_token):
    if csrf_token != session["csrf_token"]:
        abort(403)