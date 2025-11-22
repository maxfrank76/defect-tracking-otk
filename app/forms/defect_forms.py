# 📁 app/forms/defect_forms.py

from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, IntegerField, DateTimeField, BooleanField
from wtforms.validators import DataRequired, Length, Optional

class DefectReportForm(FlaskForm):
    # Основные данные
    product_veksh = StringField('Номер ВЕКШ', validators=[DataRequired(), Length(max=50)])
    osk_operation = SelectField('Операция ОСК', 
        choices=[
            ('035', '035 - Контроль сборки'),
            ('040', '040 - Контроль монтажа'),
            ('045', '045 - Контроль проводки'), 
            ('055', '055 - Финальный контроль')
        ],
        validators=[DataRequired()]
    )
    
    # Классификация
    defect_type = SelectField('Тип дефекта',
        choices=[
            ('production', 'Производственный'),
            ('constructive', 'Конструктивный'),
            ('material', 'По сырью/материалам'),
            ('equipment', 'По оборудованию')
        ],
        validators=[DataRequired()]
    )
    
    defect_source = SelectField('Источник дефекта',
        choices=[
            ('raw_material', 'Сырье/материалы'),
            ('process', 'Техпроцесс'), 
            ('equipment', 'Оборудование'),
            ('human', 'Человеческий фактор')
        ],
        validators=[DataRequired()]
    )
    
    priority = SelectField('Приоритет',
        choices=[
            ('critical', 'Критичный'),
            ('high', 'Высокий'),
            ('medium', 'Средний'),
            ('low', 'Низкий')
        ],
        validators=[DataRequired()]
    )
    
    responsible_department = SelectField('Ответственное подразделение',
        choices=[
            ('production', 'Производство'),
            ('otk', 'ОТК'),
            ('technology', 'Технологи'),
            ('supply', 'Снабжение')
        ],
        validators=[DataRequired()]
    )

class DefectForm(FlaskForm):
    description = TextAreaField('Описание дефекта', validators=[DataRequired()])
    defect_code = StringField('Код дефекта', validators=[Optional(), Length(max=50)])
    position = StringField('Позиция в изделии', validators=[Optional(), Length(max=100)])
    quantity = IntegerField('Количество', default=1)
    unit = SelectField('Единица измерения',
        choices=[
            ('шт', 'шт'),
            ('м', 'м'),
            ('см', 'см'), 
            ('мм', 'мм')
        ],
        default='шт'
    )