import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.wsgi import WSGIMiddleware
from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
api = FastAPI()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
api.mount("/blog", WSGIMiddleware(app))



class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(300), nullable=False)
    password = db.Column(db.String(300), nullable=False)
    text = db.Column(db.Text, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self):
        return '<Article %r>' % self.id


with app.app_context():
    db.create_all()


@app.route('/')
@app.route('/home')
def index():
    return render_template("index.html")


@app.route('/about')
def about():
    return render_template("about-us.html")


@app.route('/blog')
def blog():
    return render_template("blog.html")


@app.route('/blog-single')
def blog1():
    return render_template("blog-single.html")


@app.route('/services')
def services():
    return render_template("services.html")


@app.route('/posts')
def posts():
    articles = Article.query.order_by().all()
    return render_template("posts.html", articles=articles)


@app.route('/posts/<int:id>')
def post_detail(id):
    article = Article.query.get(id)
    return render_template("post_detail.html", article=article)


@app.route('/create-article', methods=['POST', 'GET'])
def create_article():
    if request.method == "GET":
        phone = request.form['phone']
        email = request.form['email']
        text = request.form['text']
        password = request.form['password']

        article = Article(phone=phone, email=email, text=text, password=password)
        db.session.add(article)
        db.session.commit()
        return render_template("index.html")
    else:
        return render_template("index.html")


@api.get('/api')
def root():
    articles = Article.query.order_by().all()
    return {
        'text': articles
    }


if __name__ == "__main__":
    uvicorn.run(api, host='127.0.0.1', port=8000)