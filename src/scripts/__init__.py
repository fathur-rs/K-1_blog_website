from flask import Flask
from flask_sqlalchemy import SQLAlchemy
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

db = SQLAlchemy(app)

class Blogs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    img = db.Column(db.Text, nullable=True)
    img_base64 = db.Column(db.Text, nullable=True)
    img_name = db.Column(db.Text, nullable=True)
    mimetype = db.Column(db.Text, nullable=True)
    blog_content = db.Column(db.Text, nullable=False)
    posted_on = db.Column(db.DateTime, nullable=False, default=datetime.utcnow())


from scripts import routes