from flask import Blueprint, render_template, session

from website.models import User


views = Blueprint('views', __name__)

@views.route('/')
def home():
    user_id = session.get('user_id')
    user = User.query.get(user_id) if user_id else None
    return render_template('/index.html', user=user)

@views.route('/login.html')
def login():
    return render_template('login.html')
