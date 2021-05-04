from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, length, email, equal_to


class RegistrationForm(FlaskForm):
    firstname = StringField("First name", [DataRequired()])
    lastname = StringField("Last name", [DataRequired()])
    username = StringField("Username",[DataRequired(), length(min=8)])
    password = PasswordField("Password", [DataRequired(), length(min=8)])
    Repassword = PasswordField("Re-enter Password", [equal_to("password", message="Passwords don't match")])
    email = StringField("Email", [DataRequired(), email()])
    submit = SubmitField("submit")


class LoginForm(FlaskForm):
    username = StringField("Username", [DataRequired(),length(min=8)])
    password = PasswordField("Password", [DataRequired(), length(min=8)])
    submit = SubmitField("submit")
