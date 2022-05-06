from db import db

def create_group(name, members, owner_id):
    sql = """INSERT INTO groups (name)
            VALUES (:name) RETURNING id"""
    group_id = db.session.execute(sql, {"name":name}).fetchone()[0]

    sql = """INSERT INTO members (member_id, group_id, role)
            VALUES (:owner_id, :group_id, 1)"""
    db.session.execute(sql, {"owner_id":owner_id, "group_id":group_id})

    for username in members.split(";"):
        sql = """INSERT INTO members (member_id, group_id, role)
                VALUES (
                (SELECT id FROM users WHERE username=:username), :group_id, 0)"""
        db.session.execute(sql, {"username":username, "group_id":group_id})
    db.session.commit()
    return group_id

def get_my_groups(user_id):
    sql = """SELECT G.name, G.id 
            FROM groups G, members M
            WHERE M.group_id = G.id AND M.member_id=:user_id
            ORDER BY G.id"""
    return db.session.execute(sql, {"user_id":user_id}).fetchall()
    
def get_group_members(group_id):
    sql = """SELECT U.username 
            FROM users U, members M
            WHERE M.group_id=:group_id AND M.member_id = U.id"""
    return db.session.execute(sql, {"group_id":group_id}).fetchall()

def get_group_name(group_id):
    sql = """SELECT name FROM groups WHERE id=:group_id"""
    return db.session.execute(sql, {"group_id":group_id}).fetchone()[0]

