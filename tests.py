from unittest import TestCase
from server import app
from model import connect_to_db, db, example_data
from flask import session


class FlaskTestsBasic(TestCase):
    """Flask tests."""

    def setUp(self):
        """Stuff to do before every test."""

        # Get the Flask test client
        self.client = app.test_client()

        # Show Flask errors that happen during tests
        app.config['TESTING'] = True

        # Connect to test database
        connect_to_db(app, "postgresql:///testdb")
        db.create_all()
        example_data()


    def tearDown(self):
        """Do at end of every test."""

        db.session.remove()
        db.drop_all()
        db.engine.dispose()

    def test_homepage(self):
        """Test homepage page."""

        # In homepage route, expected result contain Sign Up displayed on html
        result = self.client.get("/")
        self.assertIn(b"Sign Up", result.data)

    def test_login(self):
        """Test login page."""

        # When a user log in, expect redirect to user's profile page 
        # where "What's your next date plan" is part of result
        result = self.client.post("/check_userinfo",
                                  data={"email": "test1@test1.com", "password": "123"},
                                  follow_redirects=True)
        self.assertIn(b"What's your next date plan", result.data)


    def test_important_page(self):
        """Test that user can't see user's dashboard page when logged out."""

        result = self.client.get("/users/3", follow_redirects=True)
        self.assertNotIn(b"What's your next date", result.data)
        self.assertIn(b"You must be logged in", result.data)
    
    def test_logout(self):
        """Test logout route."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess['user_id'] = 2

            result = self.client.get('/logout', follow_redirects=True)

            self.assertNotIn(b'user_id', session)
            self.assertIn(b'Logged Out', result.data)



if __name__ == "__main__":
    import unittest

    unittest.main()