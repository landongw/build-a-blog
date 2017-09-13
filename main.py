from flask import Flask, request, escape, redirect, render_template
from flask_sqlalchemy import SQLAlchemy

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


# TODO: Setup app route with def index to display blog posts "/blog"


# TODO: Setup app route with def new_post "/newpost"
@app.route('/', methods=['GET', 'POST'])
def index():
    
    if request.method == 'POST':
        post_title = request.form['post_title']
        post_body = request.form['post_body']
        new_post = Blog(post_title, post_body)

        db.session.add(new_post)
        db.session.commit()

    return render_template('new_post.html', title="New Post")


if __name__ == '__main__':
    app.run()