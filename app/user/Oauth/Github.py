from flask_dance.consumer import oauth_authorized, oauth_error
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage
from flask_dance.contrib.github import make_github_blueprint, github
from flask_login import login_user
from sqlalchemy.exc import NoResultFound
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage

from app.models import db
from flask import redirect, url_for, flash
from flask_user import current_user
from app.models.user import OAuth, UserModel,User

blueprint = make_github_blueprint(
    storage=SQLAlchemyStorage(OAuth, db.session, user=current_user)
)


@oauth_authorized.connect_via(blueprint)
def github_logged_in(blueprint, token):
    if not token:
        flash(f"Failed to log in with GitHub.","error")
        return redirect(url_for('UserModel.login'))

    resp = blueprint.session.get("/user")
    if not resp.ok:
        msg = f"Failed to fetch user info from GitHub."
        flash(msg,'error')
        return redirect(url_for('UserModel.login'))

    github_info = resp.json()
    github_user_id = str(github_info["id"])

    # Find this OAuth token in the database, or create it
    query = OAuth.query.filter_by(
        provider=blueprint.name, provider_user_id=github_user_id
    )
    try:
        oauth = query.one()
    except NoResultFound:
        github_user_login = str(github_info["login"])
        oauth = OAuth(
            provider=blueprint.name,
            provider_user_id=github_user_id,
            provider_user_login=github_user_login,
            token=token,
        )

    # Now, figure out what to do with this token. There are 2x2 options:
    # user login state and token link state.

    if current_user.is_anonymous:
        if oauth.user:
            # If the user is not logged in and the token is linked,
            # log the user into the linked user account
            login_user(oauth.user)
            flash("Successfully signed in with GitHub.")

            return redirect(url_for('StoreModel.store'))
        else:
            # If the user is not logged in and the token is unlinked,
            # create a new local user account and log that account in.
            # This means that one person can make multiple accounts, but it's
            # OK because they can merge those accounts later.
            user = User(username=github_info["login"])
            oauth.user = user
            db.session.add_all([user, oauth])
            db.session.commit()
            login_user(user)
            flash("Successfully signed in with GitHub.")
            print(user)
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
            flash("Successfully linked GitHub account.")
            return redirect(url_for('StoreModel.store'))

    # Indicate that the backend shouldn't manage creating the OAuth object
    # in the database, since we've already done so!

    return False


# notify on OAuth provider error
@oauth_error.connect_via(blueprint)
def github_error(blueprint, message, response):
    msg = "OAuth error from {name}! " "message={message} response={response}".format(
        name=blueprint.name, message=message, response=response
    )
    flash(msg, category="error")


# @github_blueprint.route("/")
# def github_login():
#     if not github.authorized:
#         return redirect(url_for("github.login"))
#     account_info_get = github.get('/user')
#     account_info = account_info_get.json()
#     if account_info_get.ok:
#         username = account_info['login']
#         provider_id = account_info['id']
#
#         query = OAuth.query.filter_by(provider_user_login=username)
#
#         try:
#             user = query.one()
#         except NoResultFound:
#             user = OAuth(provider_user_login=username, provider_user_id=provider_id)
#             db.session.add(user)
#             db.session.commit()
#         login_user(user)
#         return redirect(url_for('StoreModel.store'))

#     if not token:
#         flash("Failed to log in with GitHub.", category="error")
#         return
#
#     resp = blueprint.session.get("/user")
#     if not resp.ok:
#         msg = "Failed to fetch user info from GitHub."
#         flash(msg, category="error")
#         return
#
#     github_info = resp.json()
#     github_user_id = str(github_info["id"])
#
#     # Find this OAuth token in the database, or create it
#     query = OAuth.query.filter_by(
#         provider=blueprint.name, provider_user_id=github_user_id
#     )
#     try:
#         oauth = query.one()
#     except NoResultFound:
#         github_user_login = str(github_info["login"])
#         oauth = OAuth(
#             provider=blueprint.name,
#             provider_user_id=github_user_id,
#             provider_user_login=github_user_login,
#             token=token,
#         )
#
#     # Now, figure out what to do with this token. There are 2x2 options:
#     # user login state and token link state.
#
#     if current_user.is_anonymous:
#         if oauth.user:
#             # If the user is not logged in and the token is linked,
#             # log the user into the linked user account
#             login_user(oauth.user)
#             flash("Successfully signed in with GitHub.")
#         else:
#             # If the user is not logged in and the token is unlinked,
#             # create a new local user account and log that account in.
#             # This means that one person can make multiple accounts, but it's
#             # OK because they can merge those accounts later.
#             user = UserModel(username=github_info["login"])
#             oauth.user = user
#             db.session.add_all([user, oauth])
#             db.session.commit()
#             login_user(user)
#             flash("Successfully signed in with GitHub.")
#     else:
#         if oauth.user:
#             # If the user is logged in and the token is linked, check if these
#             # accounts are the same!
#             if current_user != oauth.user:
#                 # Account collision! Ask user if they want to merge accounts.
#                 url = url_for("auth.merge", username=oauth.user.username)
#                 return redirect(url)
#         else:
#             # If the user is logged in and the token is unlinked,
#             # link the token to the current user
#             oauth.user = current_user
#             db.session.add(oauth)
#             db.session.commit()
#             flash("Successfully linked GitHub account.")
#
#     # Indicate that the backend shouldn't manage creating the OAuth object
#     # in the database, since we've already done so!
#     return False
#
#
# # notify on OAuth provider error
# @oauth_error.connect_via(blueprint)
# def github_error(blueprint, message, response):
#     msg = "OAuth error from {name}! " "message={message} response={response}".format(
#         name=blueprint.name, message=message, response=response
#     )
#     flash(msg, category="error")
#
