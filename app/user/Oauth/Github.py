from flask_dance.consumer import oauth_authorized, oauth_error
from flask_dance.contrib.github import make_github_blueprint
from sqlalchemy.exc import NoResultFound
from flask_dance.consumer.storage.sqla import SQLAlchemyStorage

from app.models import db
from flask import redirect, url_for, flash
from flask_login import current_user
from flask_login import login_user
from app.models.user import OAuth, UserModel

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
        flash("Failed to fetch user info from Google.", "error")
        return redirect(url_for('UserModel.login'))

    github_info = resp.json()
    github_user_id = str(github_info["id"])
    print(github_info)
    # Find this OAuth token in the database, or create it
    query = OAuth.query.filter_by(
        provider=blueprint.name, provider_user_id=github_user_id
    )
    try:
        oauth = query.one()
    except NoResultFound:
        github_user_login = str(github_info["login"])
        github_user_name = str(github_info['login'])
        oauth = OAuth(
            provider=blueprint.name,
            provider_user_id=github_user_id,
            provider_user_name=github_user_name,
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
            flash("Successfully signed in with Github.", 'success')
            return redirect(url_for('StoreModel.store'))
        else:
            # If the user is not logged in and the token is unlinked,
            # create a new local user account and log that account in.
            # This means that one person can make multiple accounts, but it's
            # OK because they can merge those accounts later.
            user = UserModel(firstname=github_info["login"],
                             lastname=github_info["login"],
                             username=github_info["login"],
                             email=github_info["login"],
                             password=token["access_token"],
                             )
            oauth.user = user
            db.session.add_all([user, oauth])
            db.session.commit()
            login_user(user)
            flash("Successfully signed in with Github.", 'success')
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
            flash("Successfully linked Github account.", 'success')
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
