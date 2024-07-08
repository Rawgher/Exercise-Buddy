from app import app
from models import db, connect_db, User
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Configure the database connection
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DEV_DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Create the database tables and adds a test user account
with app.app_context():
    db.drop_all()
    db.create_all()

    # Add the test user
    user = User.register(username='testuser', pwd='testpassword', email='testemail@test.com')
    db.session.add(user)
    db.session.commit()

    print("Database seeded successfully")