# run.py
from app import create_app, db
from app.models.user import User
from werkzeug.security import generate_password_hash
from flask import redirect, url_for

app = create_app()

@app.route('/')
def index():
    return redirect(url_for('auth.login'))  # ✅ Исправлено на auth.login

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Создаем демо-пользователей, если их нет
        demo_users = [
            {
                'username': 'demo_otk',
                'email': 'otk@demo.com',
                'password': 'demo',
                'role': 'otk_engineer',
                'full_name': 'Демо Инженер ОТК'
            },
            {
                'username': 'demo_worker', 
                'email': 'worker@demo.com',
                'password': 'demo',
                'role': 'worker',
                'full_name': 'Демо Сборщик'
            },
            {
                'username': 'demo_master',
                'email': 'master@demo.com', 
                'password': 'demo',
                'role': 'master',
                'full_name': 'Демо Мастер'
            },
            {
                'username': 'demo_admin',
                'email': 'admin@demo.com',
                'password': 'demo', 
                'role': 'admin',
                'full_name': 'Демо Администратор'
            },
            {
                'username': 'demo_otk_chief',
                'email': 'otk_chief@demo.com',
                'password': 'demo',
                'role': 'otk_chief', 
                'full_name': 'Демо Начальник ОТК'
            },
            {
                'username': 'demo_production_chief',
                'email': 'production_chief@demo.com',
                'password': 'demo',
                'role': 'production_chief',
                'full_name': 'Демо Начальник ПО'
            },
            {
                'username': 'demo_technologist',
                'email': 'technologist@demo.com',
                'password': 'demo',
                'role': 'technologist',
                'full_name': 'Демо Технолог'
            },
            {
                'username': 'demo_director',
                'email': 'director@demo.com',
                'password': 'demo',
                'role': 'production_director',
                'full_name': 'Демо Директор по производству'
            }
        ]
        
        created_users = []
        for user_data in demo_users:
            if not User.query.filter_by(username=user_data['username']).first():
                user = User(
                    username=user_data['username'],
                    email=user_data['email'],
                    password_hash=generate_password_hash(user_data['password']),
                    role=user_data['role'],
                    full_name=user_data['full_name']
                )
                db.session.add(user)
                created_users.append(user_data['username'])
        
        db.session.commit()
        
        if created_users:
            print("✅ Созданы демо-пользователи:")
            for username in created_users:
                print(f"   👤 {username} - пароль: demo")
        else:
            print("✅ Демо-пользователи уже существуют")
    
    print("\n🚀 Запуск системы управления дефектами ОТК...")
    print("📍 Адрес: http://localhost:5000")
    print("\n👥 Доступные демо-аккаунты:")
    print("   👷 demo_otk - Инженер ОТК")
    print("   🔧 demo_worker - Сборщик") 
    print("   👨‍💼 demo_master - Мастер ПО")
    print("   👑 demo_admin - Администратор")
    print("   📊 demo_otk_chief - Начальник ОТК")
    print("   🏭 demo_production_chief - Начальник ПО")
    print("   🔬 demo_technologist - Технолог")
    print("   💼 demo_director - Директор по производству")
    print("\n🔑 Для всех аккаунтов пароль: demo")
    
    app.run(debug=True)