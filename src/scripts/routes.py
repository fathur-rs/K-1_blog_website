from flask import flash, redirect, render_template, request
from flask.helpers import url_for
from werkzeug.utils import secure_filename
from scripts import app
import os


ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/")
@app.route("/home")
def index_page():
    return render_template('index.html')


@app.route("/author")
def author_page():
    return render_template('author.html')


@app.route("/post")
def post_page():
    return render_template('post.html')


@app.route("/write", methods=["POST", "GET"])
def write_page():
    if request.method == "POST":
        _title = request.form.get("title")
        _author = request.form.get("author")
        _blog = request.form.get("blog_content")
        db.session.add(blog())
        print(_title, _author, _blog)

        Upload Thumbnail
        if 'file' not in request.files:
            flash("no file part")
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No Image selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'] , filename))
            flash("Image Succesfuly")
            return render_template('write.html')
        else:
            flash("Error")
            return redirect(request.url)
        
    return render_template('write.html')