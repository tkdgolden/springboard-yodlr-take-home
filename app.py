from flask import Flask, render_template, request, redirect, flash
import requests
import json
from forms import AddUserForm, EditUserForm

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"

@app.route('/')
def index():
    """ Homepage with links to login and admin pages """

    return render_template('/index.html')

@app.route('/admin')
def admin():
    """ Admin view lists all users """

    try:
        # get from api
        r = requests.get("http://localhost:3000/users")
        data = json.loads(r.text)
        return render_template('/admin.html', data=data)
    except:
        # error page
        return render_template("/error.html")


@app.route('/signup', methods=["GET", "POST"])
def signup():
    """ Signup form to create new user """

    form = AddUserForm()

    if form.validate_on_submit():
        try:
            # post to api
            requests.post("http://localhost:3000/users", data=form.data)
            flash(f"Added {form.data}")
            return redirect('/admin')
        except:
            # error page
            return render_template("/error.html")
    
    else:
        return render_template('/signup.html', form=form)
    
@app.route('/users/<user_id>', methods=["GET", "POST"])
def view_user(user_id):
    """ View and edit a user. """

    try:
        r = requests.get(f"http://localhost:3000/users/{user_id}")
        user = json.loads(r.text)
    except:
        return render_template("/error.html")

    form = EditUserForm()

    if form.validate_on_submit():
        try:
            # post to api
            requests.put(f"http://localhost:3000/users/{user_id}", data=form.data)
            flash(f"Added {form.data}")
            return redirect('/admin')
        except:
            # error page
            return render_template("/error.html")
    
    else:
        form.firstName.data = user['firstName']
        form.lastName.data = user['lastName']
        form.email.data = user['email']
        form.id.data = user['id']
        form.state.data = user['state']

        return render_template('/user.html', form=form, user=user)
    
@app.route("/users/<user_id>/delete")
def delete_user(user_id):
    """ deletes a user and returns to admin page """

    try:
        requests.delete(f"http://localhost:3000/users/{user_id}")
        return redirect("/admin")
    except:
        return render_template("/error.html")
    
