from crypt import methods
from app import app
from flask import render_template, request, session, redirect
import posts, users, comments, ratings, groups
from messages import get_group_messages, create_message #"import messages" ei onnistunut

@app.route("/")
def index():
    return render_template("index.html", posts=posts.get_posts_index())

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Väärä Käyttäjänimi tai Salasana")

@app.route("/logout")
def logout():
    users.logout()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        if len(username) < 3 or len(username) > 20:
            return render_template("error.html", message="Käyttäjänimen kuuluu olla 3-20 merkkiä")   

        password = request.form["password"]
        if len(password) < 3 or len(password) > 20:
            return render_template("error.html", message="Salasanan kuuluu olla 3-20 merkkiä")  

        role = request.form["role"]
        if int(role) < 0 or int(role) > 1:
            return render_template("error.html", message="Virheellinen käyttäjärooli")  

        if users.register(username, password, role):
            return redirect("/")
        else:
            return render_template("error.html", message="Rekisteröinti ei onnistunut. Käyttäjänimi saattaa olla käytössä")


@app.route("/newpost", methods=["get", "post"])
def newpost():
    if request.method == "GET":
        users.require_role(0)
        return render_template("newpost.html")
    
    if request.method == "POST":
        users.require_role(0)
        csrf_token = request.form["csrf_token"]
        users.check_csrf(csrf_token)

        title = request.form["title"]
        if len(title) < 1 or len(title) > 100:
            return render_template("error.html", message="Otsikko on tyhjä tai yli 100 merkkiä")  

        body = request.form["body"]
        if len(body) < 1 or len(body) > 1000:
            return render_template("error.html", message="Leipäteksti on tyhjä tai yli 1000 merkkiä")  

        poster_id = session["user_id"]
        try:  
            post_id = posts.create_new_post(title,body,poster_id)
            return redirect("/viewpost/"+str(post_id))
        except:
            return render_template("error.html", message="Keskustelun aloittaminen epäonnistui")

@app.route("/viewpost/<int:post_id>")
def viewpost(post_id):
    session["post_id"] = post_id
    content = posts.get_post_content(post_id)
    post_comments = comments.get_post_comments(post_id)
    return render_template("viewpost.html", post = content, comments = post_comments)


@app.route("/comment", methods=["POST"])
def comment():
    users.require_role(0)
    csrf_token = request.form["csrf_token"]
    users.check_csrf(csrf_token)
        
    comment = request.form["comment"]
    if len(comment) < 1 or len(comment) > 1000:
        return render_template("error.html", message="Kommentti on tyhjä tai yli 1000 merkkiä") 

    post_id = session["post_id"]
    commenter_id = session["user_id"]
    if comments.create_new_comment(commenter_id, post_id, comment):
        return redirect("/viewpost/"+str(post_id))
    else:
        return render_template("error.html", message="Kommentointi epäonnistui")

@app.route("/group/<int:group_id>")
def group(group_id):
    session["group_id"] = group_id
    try:
        members = groups.get_group_members(group_id)

        memblist = []
        for list in members:
            for member in list:
                memblist.append(member)
        if session["user_username"] not in memblist:
            return render_template("error.html", message="Käyttäjä ei ole ryhmän jäsen")

        group_messages = get_group_messages(group_id)
        name = groups.get_group_name(group_id)
        return render_template("group.html", name = name, members = members, messages = group_messages)
    except:
        return render_template("error.html", message="Ryhmää ei löytynyt")


@app.route("/message", methods=["POST"])
def message():
    users.require_role(0)
    csrf_token = request.form["csrf_token"]
    users.check_csrf(csrf_token)
        
    message = request.form["message"]
    if len(message) < 1 or len(message) > 1000:
        return render_template("error.html", message="Viesti on tyhjä tai yli 1000 merkkiä") 

    group_id = session["group_id"]
    user_id = session["user_id"]
    create_message(message, group_id, user_id)
    return redirect("/group/"+str(group_id))


@app.route("/rate", methods=["POST"])
def rate():
    users.require_role(0)
    csrf_token = request.form["csrf_token"]
    users.check_csrf(csrf_token)

    rater_id = session["user_id"]
    post_id = session["post_id"]
    if request.form["upvote_post"]:
        ratings.create_rating_on_post(rater_id,post_id)
    return redirect("/viewpost/"+str(post_id))

@app.route("/messages/<int:user_id>")
def messages(user_id):
    users.require_role(0)
    if user_id != session["user_id"]:
        return render_template("error.html", message="Väärä käyttäjä") 
    return render_template("messages.html", groups=groups.get_my_groups(user_id))

@app.route("/newgroup", methods=["GET", "POST"])
def newgroup():
    if request.method == "GET":
        users.require_role(0)
        return render_template("newgroup.html")
    if request.method == "POST":
        users.require_role(0)
        csrf_token = request.form["csrf_token"]
        users.check_csrf(csrf_token)

        name = request.form["name"]
        if len(name) < 1 or len(name) > 20:
            return render_template("error.html", message="Ryhmän nimen kuuluu olla 1-20 merkkiä") 

        members = request.form["members"]
        if len(members) > 1000:
            return render_template("error.html", message="Jäsenet-lomake on yli 1000 merkkiä") 

        owner_id = session["user_id"]
        group_id = groups.create_group(name, members, owner_id)
        return redirect("/group/"+str(group_id))

@app.route("/search/<search_term>")
def search(search_term):
    results = posts.search_for_posts(search_term)
    return render_template("search.html", results = results, search_term = search_term)
    
@app.route("/searchpost", methods=["POST"])
def searchpost():
    search_term = request.form["search_term"]
    if len(search_term) < 1 or len(search_term) > 100:
            return render_template("error.html", message="Tyhjä tai liian pitkä haku") 
    return redirect("/search/"+str(search_term))

@app.route("/edit", methods=["GET", "POST"])
def edit():
    if request.method == "GET":
        users.require_role(0)
        post_id = session["post_id"]
        content = posts.get_post_content(post_id)
        if content[3] != session["user_id"]:
            return render_template("error.html", message="Väärä käyttäjä") 

        return render_template("edit.html", post_id = post_id, content = content)
    if request.method == "POST":
        users.require_role(0)
        csrf_token = request.form["csrf_token"]
        users.check_csrf(csrf_token)

        body = request.form["body"]
        if len(body) < 1 or len(body) > 1000:
            return render_template("error.html", message="Leipäteksti on tyhjä tai yli 1000 merkkiä") 

        post_id = session["post_id"]
        post_id = posts.edit_post(post_id, body)
        return redirect("/viewpost/"+str(post_id))

@app.route("/hidepost", methods=["POST"])
def hidepost():
    csrf_token = request.form["csrf_token"]
    users.check_csrf(csrf_token)

    post_id = request.form["post_id"]
    posts.toggle_post_visibility(post_id)
    return redirect("/myposts")

@app.route("/deletepost", methods=["POST"])
def deletepost():
    csrf_token = request.form["csrf_token"]
    users.check_csrf(csrf_token)
        
    post_id = request.form["post_id"]
    posts.delete_post(post_id)
    return redirect("/")

@app.route("/deletecomment", methods=["POST"])
def deletecomment():
    csrf_token = request.form["csrf_token"]
    users.check_csrf(csrf_token)

    comment_id = request.form["comment_id"]
    post_id = session["post_id"]
    comments.delete_comment(comment_id)
    return redirect("/viewpost/"+str(post_id))


@app.route("/myposts")
def myposts():
    users.require_role(0)
        
    user_id = session["user_id"]
    content = posts.get_my_posts(user_id)
    return render_template("myposts.html", content = content)
    
