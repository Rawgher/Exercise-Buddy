from unittest import TestCase
from app import app
from models import db, User, Exercise, WorkoutEntry, UserExercise
from dotenv import load_dotenv
import os
load_dotenv()



class BaseTestCase(TestCase):
    """A base test case."""

    def setUp(self):
        app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('TEST_DATABASE_URL')
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_ECHO'] = False
        app.config['TESTING'] = True
        app.testing = True
        self.app = app.test_client()
        with app.app_context():
            db.create_all()
            self.populate_db()

    def tearDown(self):
        with app.app_context():
            db.session.remove()
            db.drop_all()

    def populate_db(self):
        """Populate the database with initial data for testing."""
        user = User.register(username='testuser', pwd='testpassword', email='test@example.com')
        db.session.add(user)
        db.session.commit()

class TestUserRoutes(BaseTestCase):
    """Test cases for user-related routes."""

    def test_register(self):
        with app.app_context():
            response = self.app.post('/register', data=dict(
                username='newuser',
                password='newpassword',
                email='newuser@example.com'
            ), follow_redirects=True)
            self.assertEqual(response.status_code, 200)  # Redirect after successful registration
            user = User.query.filter_by(username='newuser').first()
            self.assertIsNotNone(user)

    def test_login(self):
        response = self.app.post('/login', data=dict(
            username='testuser',
            password='testpassword'
        ), follow_redirects=True)
        self.assertEqual(response.status_code, 200)  # Redirect after successful login
        with self.app as c:
            with c.session_transaction() as sess:
                self.assertEqual(sess['user'], 'testuser')

    def test_logout(self):
        with self.app as c:
            with c.session_transaction() as sess:
                sess['user'] = 'testuser'
        response = self.app.get('/logout', follow_redirects=True)
        self.assertIn(b'Login', response.data)

class TestExerciseRoutes(BaseTestCase):
    """Test cases for exercise-related routes."""

    def test_search_exercises(self):
        response = self.app.post('/search', data=dict(
            muscle='biceps',
            type='strength',
            difficulty='beginner'
        ))
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Incline Hammer Curls', response.data)  

    def test_favorite_exercise(self):
        with app.app_context():
            with self.app as c:
                with c.session_transaction() as sess:
                    sess['user'] = 'testuser'
            exercise = Exercise(name='Push Up')
            db.session.add(exercise)
            db.session.commit()
            response = self.app.post(f'/favorite/{exercise.name}', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            user_exercise = UserExercise.query.filter_by(user='testuser', exercise_id=exercise.id).first()
            self.assertIsNotNone(user_exercise)

    def test_unfavorite_exercise(self):
        """Test unfavoriting an exercise."""
        with app.app_context():
            with self.app as c:
                with c.session_transaction() as sess:
                    sess['user'] = 'testuser'
            exercise = Exercise(name='Push Up')
            db.session.add(exercise)
            db.session.commit()
            user_exercise = UserExercise(user='testuser', exercise_id=exercise.id)
            db.session.add(user_exercise)
            db.session.commit()

            response = self.app.post(f'/favorite/{exercise.name}', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            user_exercise = UserExercise.query.filter_by(user='testuser', exercise_id=exercise.id).first()
            self.assertIsNone(user_exercise)

    def test_delete_workout(self):
        with app.app_context():
            with self.app as c:
                with c.session_transaction() as sess:
                    sess['user'] = 'testuser'
            workout = WorkoutEntry(user='testuser', date='2023-01-01', description='Test Workout')
            db.session.add(workout)
            db.session.commit()
            response = self.app.post(f'/user/testuser/workouts/{workout.id}/delete', follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            deleted_workout = WorkoutEntry.query.get(workout.id)
            self.assertIsNone(deleted_workout)

    def test_add_workout(self):
        with app.app_context():
            with self.app as c:
                with c.session_transaction() as sess:
                    sess['user'] = 'testuser'
            response = self.app.post('/user/testuser/workouts', data=dict(
                date='2023-01-01',
                description='Test Workout'
            ), follow_redirects=True)
            self.assertEqual(response.status_code, 200)
            workout = WorkoutEntry.query.filter_by(user='testuser', date='2023-01-01', description='Test Workout').first()
            self.assertIsNotNone(workout)

    def test_user_page(self):
        with app.app_context():
            with self.app as c:
                with c.session_transaction() as sess:
                    sess['user'] = 'testuser'
            workout = WorkoutEntry(user='testuser', date='2023-01-01', description='Test Workout')
            db.session.add(workout)
            db.session.commit()
            response = self.app.get('/user/testuser')
            self.assertEqual(response.status_code, 200)
            self.assertIn(b'Test Workout', response.data)

if __name__ == '__main__':
    import unittest
    unittest.main()
