from flask import Flask
from flask_sqlalchemy import SQLAlchemy

UPLOAD_FOLDER = "scripts\static"

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER





from scripts import routes