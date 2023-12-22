from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
app.app_context().push()


# команды в терминале для подключения к базе данных
# Run in terminal
#     >python
#     >>>from app import app
#     >>>from app import db
#     >>>db.create_all()
#
# Now it should work


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    intro = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Article %r>' % self.id


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/posts')
def posts():
    post = User.query.order_by(User.date.desc()).all()
    return render_template('posts.html', post=post)


@app.route('/posts/<int:id>')
def post_detail(id):
    post = User.query.get(id)
    return render_template('post_detail.html', post=post)


@app.route('/create', methods=['POST', 'GET'])
def create_user():
    if request.method == 'POST':
        title = request.form['title']
        intro = request.form['intro']
        text = request.form['text']

        users = User(title=title, intro=intro, text=text)

        try:
            db.session.add(users)
            db.session.commit()
            return redirect('/posts')
        except:
            return 'При добавлении статьи произошла ошибка'
    else:
        return render_template('create_user.html')


if __name__ == '__main__':
    app.run(debug=True)
