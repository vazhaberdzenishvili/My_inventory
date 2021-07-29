from flask_babel import gettext

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, length, email, equal_to


class RegistrationForm(FlaskForm):
    firstname = StringField(gettext("First name"), [DataRequired()])
    lastname = StringField(gettext("Last name"), [DataRequired()])
    username = StringField(gettext("Username"),[DataRequired(), length(min=8)])
    password = PasswordField(gettext("Password"), [DataRequired(), length(min=8)])
    Repassword = PasswordField(gettext("Re-enter Password"), [equal_to("password", message="Passwords don't match")])
    email = StringField(gettext("Email"), [DataRequired(), email()])
    submit = SubmitField(gettext("submit"))


class LoginForm(FlaskForm):
    username = StringField(gettext("Username"), [DataRequired(),length(min=8)])
    password = PasswordField(gettext("Password")), [DataRequired(), length(min=8)]
    submit = SubmitField(gettext("submit"))
