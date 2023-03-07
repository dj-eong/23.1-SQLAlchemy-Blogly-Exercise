"""Models for Blogly."""

from flask_sqlalchemy import SQLAlchemy

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
    image_url = db.Column(db.String(
    ), default='https://www.pngkey.com/png/detail/230-2301779_best-classified-apps-default-user-profile.png')
    hunger = db.Column(db.Integer, nullable=False, default=20)

    @classmethod
    def get_all_users(cls):
        return cls.query.all()
