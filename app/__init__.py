# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from config import Config

# Инициализация расширений
db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = 'Пожалуйста, войдите для доступа к этой странице.'
login_manager.login_message_category = 'info'

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Инициализация расширений с приложением
    db.init_app(app)
    login_manager.init_app(app)
    
    # Регистрация Blueprints
    from app.routes.main import main_routes
    from app.routes.auth import auth_routes
    from app.routes.defects import defect_routes
    
    app.register_blueprint(main_routes)
    app.register_blueprint(auth_routes)
    app.register_blueprint(defect_routes)
    
    # Создание таблиц в базе данных
    with app.app_context():
        db.create_all()
    
    return app

# Импорт моделей после создания db для избежания циклических импортов
from app.models.user import User
from app.models.defect_models import DefectReport, Defect

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))