from os import getenv
from app import app
from flask_sqlalchemy import SQLAlchemy

uri  = getenv("DATABASE_URL")
if uri.startswith("postgres://"):
    uri = uri.replace("postgres://", "postgresql://", 1) 
app.config["SQLALCHEMY_DATABASE_URI"] = uri
#heroku tries to use discontinued "postgres://" uri scheme, tris changes it to the correct "postgresql://"

db = SQLAlchemy(app)