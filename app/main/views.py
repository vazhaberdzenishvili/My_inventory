from app import babel
from flask import Blueprint, render_template, session, request, redirect, url_for
from app.data.pages_resource import pages

main_blueprint = Blueprint('main',
                           __name__,
                           template_folder='templates'
                           )


@main_blueprint.route('/')
def home_page():
    return render_template('home.html',pages=pages)


@main_blueprint.route('/about')
def about_us():
    return render_template('about.html',pages=pages)

@babel.localeselector
def get_locale():
    """
    returns current language and stores it in session['locale']
    the default language is 'ka'
    """
    if 'locale' not in session.keys():
        session['locale'] = 'ka'
    return session['locale']


@main_blueprint.route('/language', methods=['GET', 'POST'])
def toggle_lang():
    """
    toggles language: from 'ka' to 'en' or from 'en' to 'ka' and changes it in session['locale']
    """
    if 'locale' in session.keys():
        if session['locale'] == 'en':
            session['locale'] = 'ka'
        elif session['locale'] == 'ka':
            session['locale'] = 'en'
    else:
        session['locale'] = 'ka'

    if request.referrer:
        return redirect(request.referrer)
    else:
        return redirect(url_for('UserModel.login'))