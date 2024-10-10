from app import create_app, db
import os

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        print("Database tables created.")
        
        # Check if the database file exists
        db_path = app.config['SQLALCHEMY_DATABASE_URI'].replace('sqlite:///', '')
        if os.path.exists(db_path):
            print(f"Database file created at: {db_path}")
        else:
            print(f"WARNING: Database file not found at expected location: {db_path}")

    app.run(debug=True)