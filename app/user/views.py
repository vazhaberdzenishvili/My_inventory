from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_user
from werkzeug.security import generate_password_hash
from app.user.forms import RegistrationForm, LoginForm
from app.data.pages_resource import pages
from app import db
from app.models.user import UserModel
from flask_user import current_user


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


# google = oauth.register(
#     name='google',
#     client_id='476339205106-lpk066f3fkbojgglimso4n9vf7vojlou.apps.googleusercontent.com',
#     client_secret='c8JeeK6iBqSTyElaPY_8Fdhm',
#     access_token_url='https://accounts.google.com/o/oauth2/token',
#     access_token_params=None,
#     authorize_url='https://accounts.google.com/o/oauth2/auth',
#     authorize_params=None,
#     api_base_url='https://www.googleapis.com/oauth2/v1/',
#     userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
#     # This is only needed if using openId to fetch user info
#     client_kwargs={'scope': 'openid email profile'},
# )
#

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
                    print(current_user.email)
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



    # return redirect(url_for('StoreModel.store'))
# @user_blueprint.route('/oauth_login', methods=['GET', 'POST'])
# def oauth_login():
#     google = oauth.create_client('google')  # create the google oauth client
#     redirect_uri = url_for('UserModel.authorize', _external=True)
#     return google.authorize_redirect(redirect_uri)
#
#
# @user_blueprint.route('/authorize/oauth', methods=['GET', 'POST'])
# def authorize():
#     google = oauth.create_client('google')  # create the google oauth client
#     token = google.authorize_access_token()  # Access token from google (needed to get user info)
#     resp = google.get('userinfo')  # userinfo contains stuff u specificed in the scrope
#     user_info = resp.json()
#     user = oauth.google.userinfo()  # uses openid endpoint to fetch user info
#     # Here you use the profile/user data that you got and query your database find/register the user
#     # and set ur own data in the session not the profile from google
#     session.permanent = True  # make the session permanant so it keeps existing after broweser gets closed
#     if user_info.json().get("email_verified"):
#         unique_id = user_info.json()["sub"]
#         user_email = user_info.json()["email"]
#         picture = user_info.json()["picture"]
#         user_name = user_info.json()["given_name"]
#     else:
#         return "User email not available or not verified by Google.", 400
#     login_user(user)
#         return redirect(url_for(StoreModel.store))
