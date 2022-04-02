from email.policy import default
from io import BytesIO
from flask import flash, redirect, render_template, request, send_file
from flask.helpers import url_for
from werkzeug.utils import secure_filename
from scripts import app
import os
from scripts import Blogs, db
from sqlalchemy import desc, update
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


@app.route("/post/<int:post_id>", methods=['GET', 'POST'])
def post_page(post_id):
    post = Blogs.query.filter_by(id=post_id).one()
    content = post.blog_content.split('\p')
    paragraf = []
    for i in content:
        print(f"{i}\n")
        paragraf.append(i)
    return render_template('post.html', post=post, paragraf=paragraf)


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

@app.route("/post/<int:post_id>/edit", methods=['GET', 'POST'])
def post_edit_page(post_id):
    post_edit = Blogs.query.filter_by(id=post_id).one()

    content = post_edit.blog_content.split('\p')
    paragraf = []
    for i in content:
        print(f"{i}\n")
        paragraf.append(i)

    if request.method == 'POST':
        _title_edit = request.form.get("title_edit")
        _author_edit = request.form.get("author_edit")
        _blog_edit = request.form.get("blog_content_edit")
        print(_title_edit, _author_edit, _blog_edit)

        file_edit = request.files['file_edit']
        filename_edit = secure_filename(file_edit.filename)
        mimetype_edit = file_edit.mimetype
        img_base_64 = render_picture(file_edit.read())

        update_db = db.session.query(Blogs).filter_by(id=post_id).update({
            'title':_title_edit,
            'author':_author_edit,
            'img':file_edit.read(),
            'img_base64':img_base_64,
            'img_name': filename_edit,
            'mimetype': mimetype_edit,
            'blog_content': _blog_edit})

        db.session.commit()

        
        return redirect(url_for('post_page',post_id=post_id ))

    return render_template("post_edit.html", post_edit=post_edit, paragraf=paragraf)
