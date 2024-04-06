from flask import Flask, render_template, redirect
from forms import AddUserForm, EditUserForm, LoginForm
import api
import auth

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

app.config['SECRET_KEY'] = "secret"


@app.route('/')
def index():
    """ Homepage with links to login and register pages """

    return render_template('/index.html')


@app.route('/admin')
def admin():
    """ Admin view lists all users """

    if (not auth.check_logged_in()):
        return redirect("/")

    try:
        # get from api
        data = api.get_all_users()
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
            # hash password
            auth.create_pass_hash(form.data)
            return redirect('/login')
        except:
            # error page
            return render_template("/error.html")
    
    else:
        return render_template('/signup.html', form=form)


@app.route('/users/<user_id>', methods=["GET", "POST"])
def view_user(user_id):
    """ View and edit a user. """

    if (not auth.check_logged_in()):
        return redirect("/")

    try:
        user = api.get_user(user_id)
    except:
        return render_template("/error.html")
    
    form = EditUserForm()

    if form.validate_on_submit():
        try:
            # post to api
            api.edit_user(user_id, form.data)
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

    if (not auth.check_logged_in()):
        return redirect("/")

    try:
        api.delete_user(user_id)
        return redirect("/admin")
    except:
        return render_template("/error.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """ logs in a user """

    form = LoginForm()

    if form.validate_on_submit():
        try:
            if (auth.check_password(form.data)):
                return redirect("/admin")
            else:
                return redirect("/login")
        except:
            return render_template("/error.html")
        
    return render_template("/login.html", form=form)


@app.route("/logout")
def logout():
    """ logs out a user """

    auth.log_out()

    return redirect("/")