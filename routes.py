from app import app
from flask import render_template, request, session, redirect
import posts

@app.route("/")
def index():
    return render_template("index.html", posts=posts.get_posts_index())

@app.route("/login", methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    session["username"] = username
    #return render_template("login.html")
    return redirect("/")

@app.route("/logout")
def logout():
    del session["username"] 
    return redirect("/")

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/newpost", methods=["get", "post"])
def newpost():
    if request.method == "GET":
        return render_template("newpost.html")
    
    if request.method == "POST":
        title = request.form["title"]
        body = request.form["body"]
        try:
            poster_name = session["username"]
        except:
            poster_name = "Anonyymi"
            
        post_id = posts.create_new_post(title,body,poster_name)
        return redirect("/viewpost"+str(post_id))

@app.route("/viewpost/<int:post_id>")
def viewpost(post_id):
    content = posts.get_post_content(post_id)
    return render_template("viewpost.html", id=post_id, title=content[0], body=content[1], poster=content[2])
