from flask import Blueprint, render_template
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
