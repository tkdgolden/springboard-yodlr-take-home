from flask_wtf import FlaskForm
from wtforms import StringField, EmailField, HiddenField, SelectField, PasswordField, IntegerField
from wtforms.validators import InputRequired

class AddUserForm(FlaskForm):
    """ Form for adding users. """

    firstName = StringField("First Name: ", validators=[InputRequired()])
    lastName = StringField("Last Name: ", validators=[InputRequired()])
    email = EmailField("Email: ", validators=[InputRequired()])
    password = PasswordField("Password: ", validators=[InputRequired()])

class EditUserForm(FlaskForm):
    """ Form for editing users. """

    firstName = StringField("First Name: ", validators=[InputRequired()])
    lastName = StringField("Last Name: ", validators=[InputRequired()])
    email = EmailField("Email: ", validators=[InputRequired()])
    id = HiddenField()
    state = SelectField("Status: ", choices=[('active', "Active"), ("pending", "pending")])

class LoginForm(FlaskForm):
    """ Form for logging in users. """

    id = IntegerField("Id: ", validators=[InputRequired()])
    password = PasswordField("Password: ", validators=[InputRequired()])