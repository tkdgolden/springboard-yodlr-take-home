from app import app
from unittest import TestCase
import requests
import json

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

class UserViews(TestCase):
    """ Tests for views for admin page. """

    def test_user_view(self):
        with app.test_client() as client:
            resp = client.get("/users/3")
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<h1>Lilly Smith</h1>', html)

    def test_submit_edit_form(self):
        with app.test_client() as client:
            resp = client.post("/users/2", data={'firstName': 'Random', 'lastName': 'Blah', 'email': 'timbuctu@gmail.com', 'state': 'pending', 'id': 2})

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "/admin")

    def test_submit_edit_form_redirect(self):
        with app.test_client() as client:
            resp = client.post("/users/1", data={'firstName': 'Daniel', 'lastName': 'Barnes', 'email': 'edittest@gmail.com', 'state': 'pending', 'id': 1}, follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertIn('<td>Daniel</td>', html)
            self.assertIn('<td>Barnes</td>', html)
            self.assertIn('<td>edittest@gmail.com</td>', html)

            r = requests.get(f"http://localhost:3000/users/1")
            user = json.loads(r.text)
            self.assertEqual(user['state'], "pending")

    def test_delete_user(self):
        with app.test_client() as client:
            resp = client.get("/users/4/delete")

            self.assertEqual(resp.status_code, 302)
            self.assertEqual(resp.location, "/admin")

    def test_delete_redirect(self):
        with app.test_client() as client:
            resp = client.get("/users/4/delete", follow_redirects=True)
            html = resp.get_data(as_text=True)

            self.assertEqual(resp.status_code, 200)
            self.assertNotIn('<td>Fred</td>', html)