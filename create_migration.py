# migrate_database.py

from app import create_app, db
from app.models.defect_models import DefectReport

def migrate_database():
    app = create_app()
    
    with app.app_context():
        try:
            # Проверяем, существует ли поле factory_number
            from sqlalchemy import inspect
            inspector = inspect(db.engine)
            columns = [col['name'] for col in inspector.get_columns('defect_reports')]
            
            if 'factory_number' not in columns:
                print("🔧 Добавляем поле factory_number в таблицу defect_reports...")
                
                # Используем правильный способ для добавления колонки
                from sqlalchemy import text
                
                # Для SQLite
                db.session.execute(text('ALTER TABLE defect_reports ADD COLUMN factory_number VARCHAR(50)'))
                db.session.commit()
                
                print("✅ Поле factory_number успешно добавлено!")
            else:
                print("✅ Поле factory_number уже существует")
                
        except Exception as e:
            print(f"❌ Ошибка при миграции: {e}")
            db.session.rollback()

if __name__ == '__main__':
    migrate_database()