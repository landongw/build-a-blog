"""This program runs a simple blog website"""

import re
from datetime import datetime
from flask import Flask, request, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = ("mysql+pymysql://build-a-blog:"
                                         "GJqHxp3hiinzIPvh@localhost:8889"
                                         "/build-a-blog")
app.config['SQLALCHEMY_ECHO'] = True
db = SQLAlchemy(app)


class Blog(db.Model):
    """ Creates the Blog table and constructor """

    post_id = db.Column(db.Integer, primary_key=True)
    post_title = db.Column(db.String(1000))
    post_body = db.Column(db.String(50000))
    pub_date = db.Column(db.DateTime)

    def __init__(self, post_title, post_body, pub_date=None):
        self.post_title = post_title
        self.post_body = post_body
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date


@app.route('/blog', methods=['GET'])
def blog_page():
    """ Returns the main blog page """

    titles = Blog.query.all()
    return render_template('blog_index.html', title="Blog Name", titles=titles)


@app.route('/newpost')
def index():
    """ Returns a template to submit a new post """

    return render_template('/new_post.html')


def is_not_empty(value):
    """ Tests if a field is not empty """

    if (re.compile('.')).match(value):
        return True


@app.route('/newpost', methods=['GET', 'POST'])
def new_post():
    """ Submits the new post to the database and
    redirects the user to the new post """

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
            obj = db.session.query(Blog).order_by(Blog.post_id.desc()).first()
            post_id = str(obj.post_id)
            return redirect("/single-post/?post_id=" + post_id)
        return render_template('new_post.html', title="New Post",
                               title_error=title_error,
                               post_title=post_title,
                               body_error=body_error,
                               post_body=post_body)


# @app.route('/single-post/<int:id>')
@app.route('/single-post/')
def single_post(post_id=0):
    """ Returns a template with a single post page """

    post_id = request.args.get('post_id', post_id)
    post = Blog.query.get(post_id)

    return render_template('single_post.html', post=post)
    # return "id is {}".format(id)

if __name__ == '__main__':
    app.run()
