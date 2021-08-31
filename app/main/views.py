from app import babel
from flask import Blueprint, render_template, session, request, redirect, url_for, current_app, g
from app.data.pages_resource import pages

main_blueprint = Blueprint('main',
                           __name__,
                           template_folder='templates'
                           )


@main_blueprint.route('/')
def home_page():
    return render_template('home.html', pages=pages)


@main_blueprint.route('/about')
def about_us():
    return render_template('about.html', pages=pages)


@babel.localeselector
def get_locale():
    """
        returns current language and stores it in session['locale']
        the default language is 'ka'
        """
    if 'locale' not in session.keys():
        session['locale'] = 'en'
    return session['locale']


@main_blueprint.route('/en', methods=['GET', 'POST'])
def toggle_en_lang():
    session['locale'] = 'en'
    print(session['locale'])

    if request.referrer:
        return redirect(request.referrer)
    else:
        return redirect(url_for('UserModel.login'))


@main_blueprint.route('/ka', methods=['GET', 'POST'])
def toggle_ka_lang():
    session['locale'] = 'ka'
    print('ka')
    if request.referrer:
        return redirect(request.referrer)
    else:
        return redirect(url_for('UserModel.login'))
