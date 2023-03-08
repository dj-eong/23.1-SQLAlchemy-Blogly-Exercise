from unittest import TestCase

from app import app
from models import db, User

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()


class BloglyTestCase(TestCase):

    def setUp(self):
        User.query.delete()

        user = User(first_name="Test", last_name="User")
        db.session.add(user)
        db.session.commit()

        self.user = user

    def tearDown(self):
        db.session.rollback()

    def test_list_users(self):
        with app.test_client() as client:
            resp = client.get("/users")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('Test User', html)

    def test_show_user(self):
        with app.test_client() as client:
            resp = client.get(f"/users/{self.user.id}")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h2>Test User</h2>', html)
            self.assertIn(self.user.image_url, html)

    def test_process_new_user_followed(self):
        with app.test_client() as client:
            d = {"first_name": "Elton", "last_name": "John", "image_url": ""}
            resp = client.post("/users/new", data=d, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h2>Elton John</h2>', html)
            self.assertIn(
                'https://www.pngkey.com/png/detail/230-2301779_best-classified-apps-default-user-profile.png', html)

    def test_delete_user(self):
        with app.test_client() as client:
            resp = client.post(
                f"/users/{self.user.id}/delete", follow_redirects=True)
            self.assertEqual(User.query.all(), [])
