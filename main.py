from flask import Flask, request, escape, redirect, render_template
from flask_sqlalchemy import SQLAlchemy 

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:VAHmmxedL4OMCzCL@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Post(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    post_title = db.Column(db.String(1000))
    post_body = db.Column(db.Strong(50000))

    def __init__(self, post_title, post_body):
        self.post_title = post_title
        self.post_body = post_body


# TODO: Setup app route with def index to display blog posts "/blog"


# TODO: Setup app route with def new_post "/newpost"



if __name__ == '__main__':
    app.run()