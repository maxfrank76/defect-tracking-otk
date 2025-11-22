# 📁 app/models/defect_models.py

from datetime import datetime
from app import db

class DefectReport(db.Model):
    __tablename__ = 'defect_reports'
    
    id = db.Column(db.Integer, primary_key=True)
    
    # 🔢 Номер ведомости (XXYY-ZZZZ)
    report_number = db.Column(db.String(20), unique=True, nullable=False)
    
    # 🏷️ Основные данные
    product_veksh = db.Column(db.String(50), nullable=False)  # Номер ВЕКШ
    osk_operation = db.Column(db.String(10), nullable=False)  # 035/040/045/055
    
    # 🏷️ Классификация (из файла ОТК)
    defect_type = db.Column(db.String(50))    # производственный/конструктивный...
    defect_source = db.Column(db.String(20))  # сырье/процесс/оборудование...
    priority = db.Column(db.String(20))       # критичный/высокий/средний/низкий
    
    # 👥 Ответственность (RACI)
    responsible_department = db.Column(db.String(50))
    assigned_worker_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # Сборщик
    assigned_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))      # Мастер/Нач.ПО
    
    # ⏰ Временные метки для статистики
    created_date = db.Column(db.DateTime, default=datetime.utcnow)
    detected_date = db.Column(db.DateTime, default=datetime.utcnow)
    accepted_date = db.Column(db.DateTime)    # Принял в работу
    work_start_date = db.Column(db.DateTime)  # Начал работу  
    work_end_date = db.Column(db.DateTime)    # Закончил работу
    verified_date = db.Column(db.DateTime)    # Проверка ОТК
    
    # 📈 Статусы
    status = db.Column(db.String(20), default='created')  # created/assigned/in_progress/resolved/verified/archived
    
    # 🚨 Эскалация
    requires_chief_engineer = db.Column(db.Boolean, default=False)
    requires_general_director = db.Column(db.Boolean, default=False)
    
    # 📁 Архив
    scan_filename = db.Column(db.String(200))
    archive_status = db.Column(db.String(20), default='active')
    
    # 🔗 Связи
    defects = db.relationship('Defect', backref='report', lazy=True, cascade='all, delete-orphan')
    created_by_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    
    def generate_report_number(self):
        """Генерация номера ведомости в формате XXYY-ZZZZ"""
        year = datetime.now().strftime('%y')
        month = datetime.now().strftime('%m')
        
        # Получаем количество ведомостей за этот месяц
        month_start = datetime(datetime.now().year, datetime.now().month, 1)
        count = DefectReport.query.filter(
            DefectReport.created_date >= month_start
        ).count() + 1
        
        return f"{month}{year}-{count:04d}"
    
    def __repr__(self):
        return f'<DefectReport {self.report_number}>'

class Defect(db.Model):
    __tablename__ = 'defects'
    
    id = db.Column(db.Integer, primary_key=True)
    report_id = db.Column(db.Integer, db.ForeignKey('defect_reports.id'), nullable=False)
    
    # 📝 Описание дефекта
    description = db.Column(db.Text, nullable=False)
    defect_code = db.Column(db.String(50))  # Код дефекта по классификации
    position = db.Column(db.String(100))    # Позиция в изделии
    quantity = db.Column(db.Integer, default=1)        # Количество
    unit = db.Column(db.String(20), default='шт')      # шт/м/см и т.д.
    
    # 🛠️ Статус устранения
    status = db.Column(db.String(20), default='open')  # open/in_progress/resolved/verified
    resolution_notes = db.Column(db.Text)              # Как устранили
    resolution_method = db.Column(db.String(100))      # Способ устранения
    
    def __repr__(self):
        return f'<Defect {self.defect_code} in report {self.report_id}>'