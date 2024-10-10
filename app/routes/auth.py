from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required
from app.models.user import User
from app import db
import logging

bp = Blueprint('auth', __name__)

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user:
            flash('Username already exists')
            return redirect(url_for('auth.register'))
        new_user = User(username=username)
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        logging.info(f"New user registered: {username}")
        flash('Registration successful')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html')

@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        logging.debug(f"Login attempt for user: {username}")
        logging.debug(f"User found: {user is not None}")
        if user and user.check_password(password):
            login_user(user)
            logging.info(f"Login successful for user: {username}")
            return redirect(url_for('main.index'))
        else:
            logging.warning(f"Login failed for user: {username}")
            if user:
                logging.debug("User found but password check failed")
            else:
                logging.debug("User not found")
        flash('Invalid username or password')
    return render_template('auth/login.html')

@bp.route('/logout')
@login_required
def logout():
    logging.info(f"User logged out: {current_user.username}")
    logout_user()
    return redirect(url_for('main.index'))