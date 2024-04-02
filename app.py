from flask import Flask, render_template, request, redirect
import requests

CURR_USER_KEY = "curr_user"

app = Flask(__name__)

@app.route('/')
def index():
    """ Homepage with links to login and admin pages """

    return render_template('/index.html')

@app.route('/admin')
def admin():
    """ Admin view lists all users """

    return render_template('/admin.html')

@app.route('/signup', methods=["GET", "POST"])
def signup():
    """ Signup form to create new user """

    if request.method == "POST":
        try:
            # post to api
            r = requests.post("http://localhost:3000/users")
            return redirect('/')
        except:
            # error page
            return redirect('/signup')
    
    else:
        return render_template('/signup.html')