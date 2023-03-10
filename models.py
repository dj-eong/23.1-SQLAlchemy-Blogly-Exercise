"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()


def connect_db(app):
    db.app = app
    db.init_app(app)


# MODELS GO BELOW!
class User(db.Model):
    __tablename__ = 'users'

    def __repr__(self):
        return f'<User id: {self.id}, name: {self.first_name} {self.last_name}>'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(20), nullable=False)
    last_name = db.Column(db.String(20), nullable=False)
    image_url = db.Column(
        db.Text, default='https://www.pngkey.com/png/detail/230-2301779_best-classified-apps-default-user-profile.png')

    posts = db.relationship('Post', cascade='all, delete', backref='user')


class Post(db.Model):
    __tablename__ = 'posts'

    def __repr__(self):
        return f'<Post id: {self.id}, title: {self.title}, created at: {self.created_at}, author: {self.user.first_name} {self.user.last_name}>'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.now())
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # user = db.relationship('User', backref='posts')

    tags = db.relationship('Tag', secondary='posts_tags', backref='posts')

    def convert_date(self):
        return self.created_at.strftime('%B %d, %Y at %I:%M %p')


class Tag(db.Model):
    __tablename__ = 'tags'

    def __repr__(self):
        return f'<Tag id: {self.id}, name: {self.name}>'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.Text, nullable=False, unique=True)


class PostTag(db.Model):
    __tablename__ = 'posts_tags'

    def __repr__(self):
        return f'<PostTag post_id: {self.post_id}, tag_id: {self.tag_id}>'

    post_id = db.Column(db.Integer, db.ForeignKey(
        'posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)
