import functools

from flask import (
    Blueprint, flash, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
from myfavshows.db import get_db
import re

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    """
    View of the register page, handles the register form
    :return:
    """
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        error = None
        regu_expr = r"^[a-zA-Z0-9_\-]+(\.[a-zA-Z0-9_\-]+)*@[a-zA-Z0-9_\-]+(\.[a-zA-Z0-9_\-]+)*(\.[a-zA-Z]{2,6})$"

        if not username:
            error = 'Username is required.'
        if re.search(regu_expr, email) is None:
            error = 'Please enter a correct email address.'
        elif not password:
            error = 'Password is required.'
        elif db.execute(
                'SELECT id FROM user WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'The username "{}" is already registered. Please choose another one'.format(username)

        if error is None:
            # storing the new user information in the db
            db.execute(
                'INSERT INTO user (username, email, password) VALUES (?, ?, ?)',
                (username, email, generate_password_hash(password))
            )
            db.commit()
            flash('Hi %s, welcome to MyFavShows! Enter your credentials to log in :' % username.capitalize())
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    """
    View of the login page, handles the users connections
    :return:
    """
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            # storing user information in the object "session"
            session.clear()
            session['user_id'] = user['id']
            session['user_name'] = username
            flash('Hi %s, welcome back to MyFavShows!' % username.capitalize())
            return redirect(url_for('search.search'))

        flash(error)

    return render_template('auth/login.html')


@bp.route('/logout')
def logout():
    """
    Logs out the user by cleaning the session user and redirects to the homepage
    :return:
    """
    session.clear()
    return redirect(url_for('search.search'))


def login_required(view):
    """
    Decorator that will check if a user is signed in and redirect him to the sign in page if not
    :param view:
    :return:
    """
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if session.get('user_id') is None:
            flash('You need to sign in to access this page.')
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view