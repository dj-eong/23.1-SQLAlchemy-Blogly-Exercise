"""Blogly application."""

from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

connect_db(app)
db.create_all()

app.config['SECRET_KEY'] = 'abc123'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)


@app.route('/')
def home_page():
    front_page_posts = Post.query.order_by(
        Post.created_at.desc()).limit(5).all()
    return render_template('index.html', posts=front_page_posts)


@app.route('/users')
def show_users():
    users = User.query.all()
    return render_template('users.html', users=users)


@app.route('/users/new')
def show_new_user_form():
    return render_template('add-user.html')


@app.route('/users/new', methods=['POST'])
def process_new_user():
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    image_url = request.form['image_url'] or None

    new_user = User(first_name=first_name,
                    last_name=last_name, image_url=image_url)
    db.session.add(new_user)
    db.session.commit()

    return redirect(f'/users/{new_user.id}')


@app.route('/users/<int:user_id>')
def show_user_info(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('user-info.html', user=user)


@app.route('/users/<int:user_id>/edit')
def show_edit_user_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('edit-user.html', user=user)


@app.route('/users/<int:user_id>/edit', methods=['POST'])
def process_edited_user(user_id):
    edited_user = User.query.get_or_404(user_id)
    edited_user.first_name = request.form['first_name']
    edited_user.last_name = request.form['last_name']
    edited_user.image_url = request.form['image_url'] or 'https://www.pngkey.com/png/detail/230-2301779_best-classified-apps-default-user-profile.png'

    db.session.add(edited_user)
    db.session.commit()

    return redirect(f'/users/{user_id}')


@app.route('/users/<int:user_id>/delete', methods=['POST'])
def delete_user(user_id):
    User.query.filter_by(id=user_id).delete()
    db.session.commit()

    return redirect('/users')


@app.route('/users/<int:user_id>/posts/new')
def show_new_post_form(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('add-post.html', user=user)


@app.route('/users/<int:user_id>/posts/new', methods=['POST'])
def process_new_post(user_id):
    title = request.form['title']
    content = request.form['content']

    new_post = Post(title=title, content=content, user_id=user_id)
    db.session.add(new_post)
    db.session.commit()

    return redirect(f'/users/{user_id}')


@app.route('/posts/<int:post_id>')
def show_post_info(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post-info.html', post=post)


@app.route('/posts/<int:post_id>/edit')
def show_edit_post_form(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('edit-post.html', post=post)


@app.route('/posts/<int:post_id>/edit', methods=['POST'])
def process_edited_post(post_id):
    edited_post = Post.query.get_or_404(post_id)
    edited_post.title = request.form['title']
    edited_post.content = request.form['content']

    db.session.add(edited_post)
    db.session.commit()

    return redirect(f'/posts/{post_id}')


@app.route('/posts/<int:post_id>/delete', methods=['POST'])
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    user = post.user
    Post.query.filter_by(id=post_id).delete()
    db.session.commit()

    return redirect(f'/users/{user.id}')
