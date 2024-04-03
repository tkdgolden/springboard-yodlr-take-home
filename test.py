from app import app
from unittest import TestCase

app.config['WTF_CSRF_ENABLED'] = False
app.config['TESTING'] = True

class IndexViews(TestCase):
    """ Tests for views for index page. """

    def test_index(self):
        with app.test_client() as client:
            resp = client.get("/")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Yodlr Design Challenge</h1>', html)

class AdminViews(TestCase):
    """ Tests for views for admin page. """

    def test_admin(self):
        with app.test_client() as client:
            resp = client.get("/admin")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<td>Kyle</td>', html)

class SignupViews(TestCase):
    """ Tests for views for admin page. """

    def test_signup_form(self):
        with app.test_client() as client:
            resp = client.get("/signup")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<label for="firstName">First Name: </label>', html)

    def test_submit_signup_form(self):
        with app.test_client() as client:
            resp = client.post("/signup", data={'firstName': 'Sam', 'lastName': 'Stewart', 'email': 'test@gmail.com'})

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "/admin")

    def test_submit_signup_form_redirect(self):
        with app.test_client() as client:
            resp = client.post("/signup", data={'firstName': 'Sam', 'lastName': 'Stewart', 'email': 'test@gmail.com'}, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<td>Sam</td>', html)

    def test_signup_form_validation(self):
        with app.test_client() as client:
            client.post("/signup", data={'firstName': 'NoEmail', 'lastName': 'Stewart'})
            resp = client.get("/admin")
            html = resp.get_data(as_text=True)

            self.assertNotIn('<td>NoEmail</td>', html)

            client.post("/signup", data={'lastName': 'NoFirstName', 'email': 'test@gmail.com'})
            resp = client.get("/admin")
            html = resp.get_data(as_text=True)

            self.assertNotIn('<td>NoFirstName</td>', html)

            client.post("/signup", data={'firstName': 'NoLastName', 'email': 'test@gmail.com'})
            resp = client.get("/admin")
            html = resp.get_data(as_text=True)

            self.assertNotIn('<td>NoLastName</td>', html)