from flask import render_template, session
from flask_bcrypt import Bcrypt
import api

bcrypt = Bcrypt()


def create_pass_hash(user_data):
    """ updates a given users data to include newly hashed password """

    hashed = bcrypt.generate_password_hash(user_data['password'])
    new_user_data = {**user_data, 'password': hashed}

    # post to api
    api.post_user(new_user_data)


def check_password(form_data):
    """ checks the input password against hash sfrom api """

    user = api.get_user(form_data['id'])

    if (bcrypt.check_password_hash(user['password'], form_data['password'])):
        session['user'] = form_data["id"]
        return True
    else:
        return False


def check_logged_in():
    """ if a correct user id not saved on session, redirect to index """

    print(session)

    if ('user' in session.keys()):
        try:
            api.get_user(session['user'])
            return True
        except:
            return False
    else:
        return False

        

def log_out():
    """ log out user by clearing session """

    session.clear()