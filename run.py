# run.py
from app import create_app, db
from app.models.user import User
from flask import redirect, url_for

app = create_app()

@app.route('/')
def index():
    return redirect(url_for('auth.login'))

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        if not User.query.filter_by(username='demo').first():
            demo_user = User(
                username='demo',
                email='demo@example.com',
                role='otk_engineer', 
                full_name='Демо Инженер ОТК'
            )
            db.session.add(demo_user)
            db.session.commit()
            print("✅ Демо-пользователь создан: demo/demo")
    
    print("🚀 Запуск системы управления дефектами ОТК...")
    print("📍 Адрес: http://localhost:5000")
    print("👤 Для входа используйте: Логин - demo, Пароль - demo")
    app.run(debug=True)