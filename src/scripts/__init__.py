from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from random import randint
from datetime import datetime

UPLOAD_FOLDER = "scripts\static"

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['SECRET_KEY'] = 'super secret key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///post.db'
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'connect_args': {
        'timeout': 1000000
    }
}

def random_integer():
    min_ = 100
    max_ = 1000000
    rand = randint(min_, max_)

    return int(rand)

db = SQLAlchemy(app)

db.session.execute(
    'CREATE TABLE IF NOT EXISTS blog (id INTEGER, title VARCHAR(200) NOT NULL, author VARCHAR(100) NOT NULL, blog_text VARCHAR(100000), PRIMARY KEY(id))'
    )
# db.session.execute('CREATE TABLE IF NOT EXISTS clients (id INTEGER NOT NULL,"user_id"	INTEGER, username VARCHAR(100) NOT NULL,	date_added DATETIME, PRIMARY KEY (id))')

db.session.close()

class blog(db.Model):
    __table__name = 'blog',
    id = db.Column(db.Integer, primary_key=True),
    title = db.Column(db.String(100), nullable=False),
    author = db.Column(db.String(100), nullable=False),
    blog_text = db.Column(db.String(100000), nullable=True)
    def __repr__(self):
        return f'{self.id} - {self.title} - {self.author} - {self.blog_text} - {self.thumbnail}'
# class Clients(db.Model):
#     __tablename__ = 'clients'
#     id = db.Column(db.Integer, primary_key=True)
#     user_id = db.Column(db.Integer, default=random_integer, primary_key=True)
#     username = db.Column(db.String(100), nullable=False)
#     date_added = db.Column(db.DateTime, default=datetime.utcnow)
#     clients_data = db.relationship('Clients_Data', backref='author', lazy=True)
#     clients_input = db.relationship('Clients_Input', backref='author', lazy=True)

#     def __repr__(self):
#         return f'{self.user_id} - {self.username} - {self.date_added}'
        
from scripts import routes