# app/routes/main.py

from flask import Blueprint, render_template, redirect, url_for
from flask_login import current_user, login_required

# Создаем blueprint
main_routes = Blueprint('main', __name__)

@main_routes.route('/')
@main_routes.route('/index')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('defects.defect_dashboard'))
    return render_template('index.html', title='Главная')

@main_routes.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html', title='Дашборд')

@main_routes.route('/profile')
@login_required
def profile():
    return render_template('profile.html', title='Профиль')