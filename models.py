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

    posts = db.relationship('Post', backref='user',
                            cascade='all, delete-orphan')


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

    def convert_date(self):
        return self.created_at.strftime('%B %d, %Y at %I:%M %p')
