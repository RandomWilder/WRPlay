from app import db, create_app
from app.models import User, Raffle, Ticket

def reset_database():
    app = create_app()
    with app.app_context():
        # Drop all tables
        db.drop_all()
        
        # Create all tables
        db.create_all()
        
        # Optionally, add initial data here
        # For example, create an admin user
        admin = User(username='admin', is_admin=True)
        admin.set_password('admin')  # Make sure to change this in production!
        db.session.add(admin)
        
        db.session.commit()
        
        print("Database has been reset and initialized with basic data.")

if __name__ == "__main__":
    reset_database()