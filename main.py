"""This script runs a simple blog website"""

from flask import Flask, request, escape, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
import re

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://build-a-blog:GJqHxp3hiinzIPvh@localhost:8889/build-a-blog'
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)

class Blog(db.Model):

    id = db.Column(db.Integer, primary_key=True)
    post_title = db.Column(db.String(1000))
    post_body = db.Column(db.String(50000))

    def __init__(self, post_title, post_body):
        self.post_title = post_title
        self.post_body = post_body


@app.route('/blog', methods=['GET'])
def blog_page():
    titles = Blog.query.all()
    return render_template('blog_index.html', title="Blog Name", titles=titles)

@app.route('/newpost')
def index():
    return render_template('/new_post.html')

def is_not_empty(value):
    if (re.compile('.')).match(value):
        return True

@app.route('/newpost', methods=['GET', 'POST'])
def new_post():

    title_error = ""
    body_error = ""

    if request.method == 'POST':
        post_title = request.form['post_title']
        post_body = request.form['post_body']
        if not is_not_empty(post_title):
            title_error += "This field cannot be empty. "

        if not is_not_empty(post_body):
            body_error += "This field cannot be empty. "

        if not title_error and not body_error:
            new_post = Blog(post_title, post_body)
            db.session.add(new_post)
            db.session.commit()
            return redirect('/blog')
        else:
            return render_template('new_post.html', title="New Post", 
                                   title_error=title_error, post_title=post_title, 
                                   body_error=body_error, post_body=post_body)

@app.route('/single-post/<int:id>')
def single_post(id = 0):
    post = Blog.query.get(id)
    return render_template('single_post.html', post=post)

if __name__ == '__main__':
    app.run()
