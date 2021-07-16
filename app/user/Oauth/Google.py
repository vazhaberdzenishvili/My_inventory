from flask import flash, url_for, redirect
from flask_login import current_user, login_user
from flask_dance.contrib.google import make_google_blueprint
from flask_dance.consumer import oauth_authorized, oauth_error
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from sqlalchemy.orm.exc import NoResultFound
from app.models import db
from app.models.user import User, OAuth

blueprint = make_google_blueprint(
    scope=[
        "openid",
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile",
    ],
    storage=SQLAlchemyStorage(OAuth, db.session, user=current_user),
)


# create/login local user on successful OAuth login
# @oauth_authorized.connect_via(blueprint)
# def google_logged_in(blueprint, token):
#     if not token:
#         flash("Failed to log in.", 'error')
#         return False
#
#     resp = blueprint.session.get("/oauth2/v2/userinfo")
#     if not resp.ok:
#         msg = "Failed to fetch user info."
#         flash(msg, 'error')
#         return False
#
#     google_info = resp.json()
#     google_user_id = google_info["id"]
#
#     # Find this OAuth token in the database, or create it
#     query = OAuth.query.filter_by(
#         provider=blueprint.name, provider_user_id=google_user_id
#     )
#     try:
#         oauth = query.one()
#     except NoResultFound:
#         google_user_login = str(google_info["email"])
#         oauth = OAuth(
#             provider=blueprint.name,
#             provider_user_id=google_user_id,
#             provider_user_login=google_user_login,
#             token=token,
#         )
#     print('aqacsheidzleba')
#     if oauth.user:
#         # db.session.add(oauth.user)
#         login_user(oauth.user)
#         flash("Successfully signed in.", 'success')
#         return redirect(url_for('StoreModel.store'))
#     #
# else:
#     print('aqvar')
#     # Create a new local user account for this user
#     user = User(username=google_info["email"], password_hash=token['access_token'])
#     # Associate the new local user account with the OAuth token
#     # oauth.user = user
#
#     # Save and commit our database models
#     if User.query.filter_by(username=google_info['email']) is None:
#         print('anaq')
#         db.session.add([user, oauth.user])
#         db.session.commit()
#     # Log in the new local user account
#     login_user(user)
#     flash("Successfully signed in with GOOGle.", 'success')
#     redirect(url_for('StoreModel.store'))
#
# # Disable Flask-Dance's default behavior for saving the OAuth token
# return False


# create/login local user on successful OAuth login
@oauth_authorized.connect_via(blueprint)
def google_logged_in(blueprint, token):
    if not token:
        flash("Failed to log in with Google.", 'error')
        return
    resp = blueprint.session.get("/oauth2/v2/userinfo")
    if not resp.ok:
        flash("Failed to fetch user info from Google.", 'error')
        return

    google_info = resp.json()
    google_user_id = str(google_info["id"])

    # Find this OAuth token in the database, or create it
    query = OAuth.query.filter_by(
        provider=blueprint.name, provider_user_id=google_user_id
    )
    try:
        oauth = query.one()
    except NoResultFound:
        google_user_login = str(google_info["email"])
        oauth = OAuth(
            provider=blueprint.name,
            provider_user_id=google_user_id,
            provider_user_login=google_user_login,
            token=token
        )
    # Now, figure out what to do with this token. There are 2x2 options:
    # user login state and token link state.
    if current_user.is_anonymous:
        if oauth.user:
            # If the user is not logged in and the token is linked,
            # log the user into the linked user account
            login_user(oauth.user)
            db.session.add(oauth)
            db.session.commit()
            flash("Successfully signed in with Google.", 'success')
            return redirect(url_for('StoreModel.store'))
        elif not oauth.user:
            # If the user is not logged in and the token is unlinked,
            # create a new local user account and log that account in.
            # This means that one person can make multiple accounts, but it's
            # OK because they can merge those accounts later.
            user = User(username=google_info["email"])
            # print(user)
            # google_user_login = str(google_info["email"])
            # print(google_user_login)
            # if OAuth.query.filter_by(provider_user_login=google_user_login) is None:

            oauth.user = user
            db.session.add_all([user, oauth])
            db.session.commit()
            login_user(user)
            print(user)
            flash("Successfully signed in with Google.", 'success')
            # else:
            #     login_user(user)
            return redirect(url_for('StoreModel.store'))
    else:
        if oauth.user:
            # If the user is logged in and the token is linked, check if these
            # accounts are the same!
            if current_user != oauth.user:
                # Account collision! Ask user if they want to merge accounts.
                url = url_for("auth.merge", username=oauth.user.username)
                return redirect(url)
        else:
            # If the user is logged in and the token is unlinked,
            # link the token to the current user
            oauth.user = current_user
            db.session.add(oauth)
            db.session.commit()
            flash("Successfully linked Google account.", 'success')
            return redirect(url_for('StoreModel.store'))
    # Indicate that the backend shouldn't manage creating the OAuth object
    # in the database, since we've already done so!
    return False


# notify on OAuth provider error
@oauth_error.connect_via(blueprint)
def google_error(blueprint, message, response):
    msg = "OAuth error from {name}! " "message={message} response={response}".format(
        name=blueprint.name, message=message, response=response
    )
    flash(msg, 'error')
