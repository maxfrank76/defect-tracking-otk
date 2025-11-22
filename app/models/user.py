# 📁 app/models/user.py

from app import db, login_manager
from flask_login import UserMixin
from datetime import datetime

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(50), nullable=False)
    department = db.Column(db.String(100))
    full_name = db.Column(db.String(100))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    
    # 🔗 Связи с дефектами
    created_defects = db.relationship('DefectReport', foreign_keys='DefectReport.created_by_id', backref='creator', lazy=True)
    assigned_defects = db.relationship('DefectReport', foreign_keys='DefectReport.assigned_worker_id', backref='assigned_worker', lazy=True)
    
    # 🎯 Расширенная ролевая модель из финального ТЗ
    ROLE_CHOICES = {
        'otk_engineer': 'Инженер ОТК',
        'otk_chief': 'Начальник ОТК',
        'worker': 'Сборщик/Исполнитель',
        'master': 'Мастер ПО', 
        'production_chief': 'Начальник ПО',
        'technologist': 'Технолог',
        'chief_engineer': 'Главный инженер',
        'production_director': 'Директор по производству',
        'general_director': 'Генеральный директор',
        'admin': 'Администратор системы'
    }
    
    def get_role_display(self):
        return self.ROLE_CHOICES.get(self.role, self.role)
    
    def can_create_defects(self):
        return self.role in ['otk_engineer', 'worker', 'master']
    
    def can_assign_work(self):
        return self.role in ['master', 'production_chief']
    
    def can_view_statistics(self):
        return self.role in ['otk_chief', 'production_director', 'general_director', 'admin']
    
    def __repr__(self):
        return f'<User {self.username} ({self.role})>'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))