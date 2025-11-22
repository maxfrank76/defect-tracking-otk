# app/routes/defects.py

from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from app import db
from app.models.defect_models import DefectReport, Defect
from app.models.user import User
from datetime import datetime

# Создаем blueprint
defect_routes = Blueprint('defects', __name__)

@defect_routes.route('/defects')
@login_required
def defect_dashboard():
    """Дашборд дефектов для всех ролей"""
    
    # Фильтрация по ролям
    if current_user.role == 'otk_engineer':
        defects = DefectReport.query.filter_by(created_by_id=current_user.id).order_by(DefectReport.created_date.desc()).all()
    elif current_user.role == 'worker':
        defects = DefectReport.query.filter_by(assigned_worker_id=current_user.id).order_by(DefectReport.created_date.desc()).all()
    elif current_user.role in ['master', 'production_chief', 'otk_chief', 'production_director', 'admin']:
        defects = DefectReport.query.order_by(DefectReport.created_date.desc()).all()
    else:
        defects = DefectReport.query.order_by(DefectReport.created_date.desc()).limit(50).all()
    
    return render_template('defects/dashboard.html', 
                         defects=defects, 
                         title='Дашборд дефектов')

@defect_routes.route('/defects/create', methods=['GET', 'POST'])
@login_required
def create_defect_report():
    """Создание новой ведомости дефектации"""
    
    if not current_user.can_create_defects():
        flash('У вас нет прав для создания ведомостей', 'error')
        return redirect(url_for('defects.defect_dashboard'))
    
    if request.method == 'POST':
        # Создаем ведомость из формы
        report = DefectReport(
            product_veksh=request.form.get('product_veksh'),
            osk_operation=request.form.get('osk_operation'),
            defect_type=request.form.get('defect_type'),
            defect_source=request.form.get('defect_source'),
            priority=request.form.get('priority'),
            responsible_department=request.form.get('responsible_department'),
            created_by_id=current_user.id
        )
        
        # Генерируем номер
        report.report_number = report.generate_report_number()
        
        db.session.add(report)
        db.session.commit()
        
        flash(f'Ведомость {report.report_number} создана успешно!', 'success')
        return redirect(url_for('defects.defect_detail', report_id=report.id))
    
    return render_template('defects/create_report.html', title='Создание ведомости')

@defect_routes.route('/defects/<int:report_id>')
@login_required
def defect_detail(report_id):
    """Детальная страница ведомости"""
    report = DefectReport.query.get_or_404(report_id)
    
    # Проверка прав доступа
    if (report.created_by_id != current_user.id and 
        current_user.role not in ['master', 'production_chief', 'otk_chief', 'production_director', 'admin'] and
        report.assigned_worker_id != current_user.id):
        flash('У вас нет прав для просмотра этой ведомости', 'error')
        return redirect(url_for('defects.defect_dashboard'))
    
    # Получаем список пользователей для назначения (только для мастеров и начальников)
    users_for_assignment = []
    if current_user.role in ['master', 'production_chief', 'admin']:
        users_for_assignment = User.query.filter_by(role='worker').all()
    
    return render_template('defects/detail.html', 
                         report=report,
                         users_for_assignment=users_for_assignment,
                         title=f'Ведомость {report.report_number}')

@defect_routes.route('/defects/<int:report_id>/add-defect', methods=['POST'])
@login_required
def add_defect_to_report(report_id):
    """Добавление дефекта в ведомость"""
    report = DefectReport.query.get_or_404(report_id)
    
    if report.created_by_id != current_user.id and current_user.role not in ['master', 'admin']:
        flash('У вас нет прав для редактирования этой ведомости', 'error')
        return redirect(url_for('defects.defect_detail', report_id=report.id))
    
    defect = Defect(
        report_id=report.id,
        description=request.form.get('description'),
        defect_code=request.form.get('defect_code'),
        position=request.form.get('position'),
        quantity=request.form.get('quantity', 1, type=int),
        unit=request.form.get('unit', 'шт')
    )
    
    db.session.add(defect)
    db.session.commit()
    
    flash('Дефект добавлен в ведомость', 'success')
    return redirect(url_for('defects.defect_detail', report_id=report.id))

@defect_routes.route('/defects/<int:report_id>/assign', methods=['POST'])
@login_required
def assign_worker(report_id):
    """Назначение исполнителя на ведомость"""
    report = DefectReport.query.get_or_404(report_id)
    
    if not current_user.can_assign_work():
        flash('У вас нет прав для назначения исполнителей', 'error')
        return redirect(url_for('defects.defect_detail', report_id=report.id))
    
    worker_id = request.form.get('worker_id')
    worker = User.query.get(worker_id)
    
    if worker and worker.role == 'worker':
        report.assigned_worker_id = worker.id
        report.assigned_by_id = current_user.id
        report.status = 'assigned'
        report.accepted_date = datetime.utcnow()
        
        db.session.commit()
        flash(f'Исполнитель {worker.full_name} назначен на ведомость', 'success')
    else:
        flash('Ошибка при назначении исполнителя', 'error')
    
    return redirect(url_for('defects.defect_detail', report_id=report.id))

@defect_routes.route('/defects/<int:report_id>/update-status', methods=['POST'])
@login_required
def update_report_status(report_id):
    """Обновление статуса ведомости"""
    report = DefectReport.query.get_or_404(report_id)
    new_status = request.form.get('status')
    
    # Проверка прав в зависимости от статуса
    if new_status == 'in_progress' and current_user.id != report.assigned_worker_id:
        flash('Только назначенный исполнитель может начать работу', 'error')
        return redirect(url_for('defects.defect_detail', report_id=report.id))
    
    if new_status == 'resolved' and current_user.id != report.assigned_worker_id:
        flash('Только назначенный исполнитель может завершить работу', 'error')
        return redirect(url_for('defects.defect_detail', report_id=report.id))
        
    if new_status == 'verified' and current_user.role not in ['otk_engineer', 'otk_chief', 'admin']:
        flash('Только сотрудники ОТК могут проверять устранение дефектов', 'error')
        return redirect(url_for('defects.defect_detail', report_id=report.id))
    
    # Обновление статуса и временных меток
    report.status = new_status
    
    if new_status == 'in_progress':
        report.work_start_date = datetime.utcnow()
    elif new_status == 'resolved':
        report.work_end_date = datetime.utcnow()
    elif new_status == 'verified':
        report.verified_date = datetime.utcnow()
    
    db.session.commit()
    flash(f'Статус ведомости обновлен на: {new_status}', 'success')
    return redirect(url_for('defects.defect_detail', report_id=report.id))

@defect_routes.route('/api/defects/stats')
@login_required
def defect_stats():
    """API для получения статистики по дефектам"""
    if not current_user.can_view_statistics():
        return jsonify({'error': 'Нет прав доступа'}), 403
    
    # Базовая статистика (будет расширена)
    total_reports = DefectReport.query.count()
    open_reports = DefectReport.query.filter_by(status='created').count()
    assigned_reports = DefectReport.query.filter_by(status='assigned').count()
    in_progress_reports = DefectReport.query.filter_by(status='in_progress').count()
    resolved_reports = DefectReport.query.filter_by(status='resolved').count()
    verified_reports = DefectReport.query.filter_by(status='verified').count()
    
    return jsonify({
        'total_reports': total_reports,
        'open_reports': open_reports,
        'assigned_reports': assigned_reports,
        'in_progress_reports': in_progress_reports,
        'resolved_reports': resolved_reports,
        'verified_reports': verified_reports
    })