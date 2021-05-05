from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user
from werkzeug.security import generate_password_hash

from app.user.forms import RegistrationForm, LoginForm
from app.data.pages_resource import pages
from app import db

from app.models.user import UserModel

user_blueprint = Blueprint('UserModel',
                           __name__,
                           template_folder='templates/user'
                           )


@user_blueprint.route('/registration', methods=['GET', 'POST'])
def registration():
    form = RegistrationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            firstname = form.firstname.data
            lastname = form.lastname.data
            password = form.password.data
            email = form.email.data
            username = form.username.data
            user = UserModel(firstname, lastname, username, password, email)
            if UserModel.find_by_username(username) is None:
                user.add_user()
                flash(f"{firstname}, თქვენ წარმატებით გაიარეთ რეგისტრაცია", 'success')
                return redirect(url_for('UserModel.login'))
            else:
                flash(f"მომხმარებელი {username} სახელით უკვე დარეგისტრირებულია", 'error')
    return render_template('register.html', form=form, pages=pages)


@user_blueprint.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            user = UserModel.query.filter_by(username=username).first()
            if user:
                if user.check_password(password):
                    login_user(user)
                    flash(f"{user.firstname},თქვენ წარმატებით გაიარეთ ავტორიზაცია", 'success')
                    return redirect(url_for('StoreModel.store'))
                else:
                    flash(f"პაროლი არასწორია", 'error')
                    return redirect(url_for('UserModel.login'))
            flash(f"{username} სახელით მომხმარებელი არ არის რეგისტრირებული", 'error')
    return render_template('login.html', form=form, pages=pages)


@user_blueprint.route('/recovery', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        # user_data = UserModel.query.get(request.form.get('username'))
        username = request.form['username']
        user = UserModel.query.filter_by(username=username).first()
        if user:
            user.password = generate_password_hash(request.form['password'])
            db.session.commit()
            flash('პაროლი წარმატებით განახლდა', 'success')
        else:
            flash(f'მომხმარებელი სახელით {username} არ არის რეგისტრირებული', 'error')
    return redirect(url_for('UserModel.login'))
