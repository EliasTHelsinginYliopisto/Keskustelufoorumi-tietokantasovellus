from crypt import methods
from app import app
from flask import render_template, request, session, redirect
import posts, users, comments, ratings

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
        password = request.form["password"]
        if users.register(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Rekisteröinti ei onnistunut. Käyttäjänimi saattaa olla käytössä")


@app.route("/newpost", methods=["get", "post"])
def newpost():
    if request.method == "GET":
        return render_template("newpost.html")
    
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        try:
            poster_id = session["user_id"]
        except:
            poster_id = 0
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
    comment = request.form["comment"]
    post_id = session["post_id"]
    commenter_id = session["user_id"]
    if comments.create_new_comment(commenter_id, post_id, comment):
        return redirect("/viewpost/"+str(post_id))
    else:
        return render_template("error.html", message="Kommentointi epäonnistui")


@app.route("/rate", methods=["POST"])
def rate():
    rater_id = session["user_id"]
    post_id = session["post_id"]
    if request.form["upvote_post"]:
        ratings.create_rating_on_post(rater_id,post_id)
    return redirect("/viewpost/"+str(post_id))


