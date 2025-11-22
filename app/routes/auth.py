# app/routes/auth.py
from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models.user import User

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Временный демо-пользователь
        if username == 'demo' and password == 'demo':
            user = User.query.filter_by(username='demo').first()
            if not user:
                user = User(
                    username='demo',
                    email='demo@example.com',
                    role='otk_engineer',
                    full_name='Демо Инженер ОТК'
                )
                db.session.add(user)
                db.session.commit()
            
            login_user(user)
            flash('Вход выполнен успешно!', 'success')
            return redirect(url_for('dashboard.index'))
        else:
            flash('Неверные учетные данные. Используйте demo/demo', 'danger')
    
    return render_template('auth/login.html')

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Вы вышли из системы.', 'info')
    return redirect(url_for('auth.login'))