from flask import Flask, redirect, render_template, flash, session, jsonify, request
from models import db, connect_db, User, Exercise, UserExercise, WorkoutEntry
from forms import RegisterForm, LoginForm, SearchForm, WorkoutEntryForm
# from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError
from dotenv import load_dotenv
from datetime import timedelta
import os
import requests


load_dotenv()

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('MAIN_DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
# app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
# debug = DebugToolbarExtension(app)

connect_db(app)

with app.app_context():  
    # Drop all tables when changes are made
    db.drop_all()
    # Create all tables
    db.create_all()

# route checking if a user is logged in, then redirects to the login if not already signed in
@app.route("/")
def home():
    if 'user' not in session:
        return redirect('/splash')
   
    search_form = SearchForm()
    return render_template('home.html', search_form=search_form)

# splash page for handling registering or logging in
@app.route('/splash')
def splash():
    register_form = RegisterForm()
    login_form = LoginForm()
    return render_template('splash.html', register_form=register_form, login_form=login_form)

# route to handle a user signing up for exercise buddy
@app.route('/register', methods=['POST'])
def register():
    register_form = RegisterForm()
    login_form = LoginForm()
    if register_form.validate_on_submit():
        username = register_form.username.data
        password = register_form.password.data
        email = register_form.email.data
        new_user = User.register(username, password, email)
        db.session.add(new_user)
        try:
            db.session.commit()
        except IntegrityError:
            register_form.username.errors.append('Username already taken. Please enter a new username')
            register_form.email.errors.append('Email address already in use. Please enter a new email address')
            return render_template('register.html', register_form=register_form)
        session['user'] = new_user.username
        flash(f'Welcome {new_user.username}', "success")
        return redirect('/')
    
    return render_template('splash.html', register_form=register_form, login_form=login_form)

# route to handle users signing into the site
@app.route('/login', methods=['POST'])
def login():
    register_form = RegisterForm()
    login_form = LoginForm()
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        user = User.authenticate(username, password)
        
        if user:
            flash(f'Welcome back {user.username}', "success")
            session['user'] = user.username
            return redirect('/')
        else:
            login_form.username.errors = ['Invalid username or password']
        
    return render_template('splash.html', register_form=register_form, login_form=login_form)

# route that logs a user out and removes them from their session
@app.route("/logout")
def logout():
    session.pop("user")
    return redirect("/")

# route that handles the excercise API search on the home page
@app.route('/search', methods=['POST'])
def search():
    search_form = SearchForm()
    if search_form.validate_on_submit():
        q = search_form.muscle.data
        type = search_form.type.data
        diff = search_form.difficulty.data
        API_KEY = os.getenv('API_NINJAS_KEY')
        api_url = f'https://api.api-ninjas.com/v1/exercises?muscle={q}&type={type}&difficulty={diff}'
        response = requests.get(api_url, headers={'X-Api-Key': API_KEY})
        if response.status_code == requests.codes.ok:
            data = response.json()
            return render_template('home.html', search_form=search_form, data=data, search_performed=True)
        else:
            flash(f'Error with the API. Please try again later', "danger")
            return redirect('/')
        
    return render_template('home.html', search_form=search_form)

# helper function to make the youtube API call more manageable 
def extract_youtube_data(response_json):
    videos = []
    if "items" in response_json:
        for item in response_json["items"]:
            video_data = {
                "videoId": item["id"]["videoId"],
                "title": item["snippet"]["title"],
                "description": item["snippet"]["description"],
                "thumbnails": item["snippet"]["thumbnails"],
                "channelTitle": item["snippet"]["channelTitle"],
                "publishTime": item["snippet"]["publishTime"]
            }
            videos.append(video_data)
    return videos

# route for individual exercises. handles both calls to the exercise and youtube APIs
@app.route('/exercise/<name>')
def exercise_info(name):
    if 'user' not in session:
        return redirect('/splash')
    
    username = session['user']
    NINJA_API_KEY = os.getenv('API_NINJAS_KEY')
    ninja_url = f'https://api.api-ninjas.com/v1/exercises?name={name}'
    ninja_response = requests.get(ninja_url, headers={'X-Api-Key': NINJA_API_KEY})

    YT_API_KEY = os.getenv('YT_API_KEY')
    YT_URL = "https://www.googleapis.com/youtube/v3/search"
    YT_options = {
        "part": "snippet",
        "key": YT_API_KEY,
        "type": "video",
        "q": name,
        "maxResults": 3,
        "order": "viewCount",
        "relevanceLanguage": "en",
        "regionCode": "US"
    }
    yt_response = requests.get(YT_URL, params=YT_options)

    if ninja_response.status_code == requests.codes.ok:
        data = ninja_response.json()
        # Ensure data is a list and take the first element if not empty
        if isinstance(data, list) and data:
            data = data[:1]  # Limit to the first element
        elif isinstance(data, dict):
            data = [data]
        else:
            data = []

        # Check if the exercise is already favorited by the user
        exercise = Exercise.query.filter_by(name=name).first()
        if exercise:
            is_favorited = UserExercise.query.filter_by(user=username, exercise_id=exercise.id).first() is not None
        else:
            is_favorited = False

        yt_data = []
        if yt_response.status_code == requests.codes.ok:
            yt_data = extract_youtube_data(yt_response.json())
        else:
            flash('Error fetching YouTube data. Please try again later.', "danger")

        return render_template('exercise.html', data=data[0], yt_data=yt_data, is_favorited=is_favorited)

    else:
        flash(f'Error with chosen exercise. Please try another', "danger")
        return redirect('/')

# route handles favoriting a workout  
@app.route('/favorite/<string:name>', methods=['POST'])
def favorite_exercise(name):
    if 'user' not in session:
        flash("You must be logged in to favorite exercises", "danger")
        return redirect('/splash')
    
    username = session['user']
    user = User.query.filter_by(username=username).first()
    
    exercise = Exercise.query.filter_by(name=name).first()
    
    if not exercise:
        exercise = Exercise(name=name)
        db.session.add(exercise)
        db.session.commit()
    
    user_exercise = UserExercise.query.filter_by(user=username, exercise_id=exercise.id).first()
    
    if user_exercise:
        # If the exercise is already favorited, unfavorite it
        db.session.delete(user_exercise)
        flash(f'Exercise {exercise.name} unfavorited!', "success")
    else:
        # Otherwise, favorite it
        user_exercise = UserExercise(user=username, exercise_id=exercise.id)
        db.session.add(user_exercise)
        flash(f'Exercise {exercise.name} favorited!', "success")
    
    db.session.commit()
    return redirect(f'/exercise/{name}')

# route handles viewing a user's profile page
@app.route("/user/<username>")
def this_user(username):
    
    user = User.query.get_or_404(username)
    workout_form = WorkoutEntryForm()
    user_exercises = UserExercise.query.filter_by(user=username).all()
    exercises = [Exercise.query.get(ue.exercise_id) for ue in user_exercises]
    workouts = WorkoutEntry.query.filter_by(user=username).all()

     # Calculate streak
    streak = 0
    max_streak = 0
    previous_date = None

    for workout in workouts:
        if previous_date:
            if workout.date == previous_date + timedelta(days=1):
                streak += 1
            else:
                max_streak = max(max_streak, streak)
                streak = 1
        else:
            streak = 1
        previous_date = workout.date

    max_streak = max(max_streak, streak)
    
    return render_template('user.html', user=user, exercises=exercises, workout_form=workout_form, workouts=workouts, streak=max_streak)

# this route gets and posts workouts that the user wants to store on their page
@app.route('/user/<username>/workouts', methods=['GET', 'POST'])
def user_workouts(username):
    user = User.query.get_or_404(username)
    form = WorkoutEntryForm()

    if request.method == 'GET':
        workouts = WorkoutEntry.query.filter_by(user=username).all()
        events = [{
            'title': workout.description,
            'start': workout.date.isoformat()
        } for workout in workouts]
        return jsonify(events)

    if request.method == 'POST' and form.validate_on_submit():
        date = form.date.data
        description = form.description.data
        new_workout = WorkoutEntry(user=username, date=date, description=description)
        db.session.add(new_workout)
        db.session.commit()
        return jsonify({'status': 'success'})

# this route handles removing a stored workout from the user's profile
@app.route('/user/<username>/workouts/<int:workout_id>/delete', methods=['POST'])
def delete_workout(username, workout_id):
    user = User.query.get_or_404(username)
    workout = WorkoutEntry.query.get_or_404(workout_id)
    
    if workout.user != username:
        flash('You do not have permission to delete this workout.', 'danger')
        return redirect(f'/user/{username}')
    
    db.session.delete(workout)
    db.session.commit()
    flash('Workout deleted successfully.', 'success')
    return redirect(f'/user/{username}')