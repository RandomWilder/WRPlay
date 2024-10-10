from app import create_app, db
from app.models.user import User

def create_admin_user(username, password):
    app = create_app()
    with app.app_context():
        admin_user = User(username=username, is_admin=True)
        admin_user.set_password(password)
        db.session.add(admin_user)
        db.session.commit()
        print(f"Admin user '{username}' created successfully.")

if __name__ == "__main__":
    username = input("Enter admin username: ")
    password = input("Enter admin password: ")
    create_admin_user(username, password)