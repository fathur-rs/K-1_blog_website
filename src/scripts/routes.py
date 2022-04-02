from email.policy import default
from io import BytesIO
from flask import flash, redirect, render_template, request, send_file
from flask.helpers import url_for
from werkzeug.utils import secure_filename
from scripts import app
import os
from scripts import Blogs, db
from sqlalchemy import desc
import base64

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

def render_picture(data):
    render_pic = base64.b64encode(data).decode('ascii') 
    return render_pic

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/", methods=['GET', 'POST'])
@app.route("/home", methods=['GET', 'POST'])
def index_page():
    if request.method == 'POST':
        flash('hello')
        return render_template('write.html')

    all_post = Blogs.query.order_by(Blogs.posted_on).all()
    return render_template('index.html', posts=all_post)


@app.route("/post", methods=['GET', 'POST'])
def post_page():
    # post_id = db.session.query(Blogs.id).order_by(desc(Blogs.posted_on)).first()

    return render_template('post.html')


@app.route("/write", methods=["POST", "GET"])
def write_page():
    if request.method == "POST":
        _title = request.form.get("title")
        _author = request.form.get("author")
        _blog = request.form.get("blog_content")
        print(_title, _author, _blog)

        # Storing Thumbnail
        if 'file' not in request.files:
            flash("no file part")
            return redirect(request.url)

        file = request.files['file']

        if file.filename == '':
            flash('No Image selected for uploading')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            mimetype = file.mimetype

            if not filename or not mimetype:
                return '400'

            _img_base64 = render_picture(file.read())

            blog = Blogs(title=_title, author=_author, img=file.read(), img_base64=_img_base64, img_name=filename, mimetype=mimetype, blog_content=_blog)
            db.session.add(blog)
            db.session.commit()

            flash("Image Succesfuly")
            return render_template('write.html')
        else:
            flash("Error")
        
    return render_template('write.html')

