import json
import requests


def get_user(id):
    """ gets user info from api """

    r = requests.get(f"http://localhost:3000/users/{id}")
    user = json.loads(r.text)

    return user


def get_all_users():
    """ gets all user info from api """

    r = requests.get("http://localhost:3000/users")
    users = json.loads(r.text)

    return users


def post_user(user_data):
    """ posts a new user to api """

    requests.post("http://localhost:3000/users", data=user_data)


def edit_user(user_id, user_data):
    """ sends updated user data to api """

    requests.put(f"http://localhost:3000/users/{user_id}", data=user_data)


def delete_user(user_id):
    """ deletes all user data from api """ 

    requests.delete(f"http://localhost:3000/users/{user_id}")
