from flask_wtf import FlaskForm
from wtforms import StringField, EmailField
from wtforms.validators import InputRequired

class AddUserForm(FlaskForm):
    """ Form for adding users. """

    firstName = StringField("First Name: ", validators=[InputRequired()])
    lastName = StringField("Last Name: ", validators=[InputRequired()])
    email = EmailField("Email: ", validators=[InputRequired()])