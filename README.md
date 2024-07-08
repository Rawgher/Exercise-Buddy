# Exercise Buddy

Welcome to Exercise Buddy, your ultimate workout companion! Whether you're a fitness enthusiast or just starting your fitness journey, Exercise Buddy helps you stay on track with your workout goals. Sign up to give it a try.

View the deployed site [Click Here](https://exercise-buddy.onrender.com/)

## Key Features

- Search Exercises: Find exercises tailored to specific muscle groups, exercise types, and difficulty levels. The API in use contains a comprehensive list of thousands of exercises targeting every major muscle group.

- YouTube Integration: Watch related workout videos directly from the site to get tips and guidance for your exercises.

- Favorite Exercises: Save your favorite exercises for quick access and a personalized workout experience.

- Workout Tracking: Easily log your workouts on your user page. Record the type of exercise to keep track of your fitness activities.

## To Run Locally

Clone the repo and create the virtual environment.

To create the virtual environment run the following:

```
$python -m venv venv
```

Switch to the new environment:

```
//windows
$source venv/Scripts/activate

//mac
$source venv/bin/activate
```

Install the requirements:

```
pip install -r requirements.txt
```

Create a .env file on the root level of the project with the following fields filled out (links to register for the apis can be found at the end of this markdown):

```
API_NINJAS_KEY=your_api_key_here
YT_API_KEY=your_api_key_here
SECRET_KEY=your_secret_key_here
TEST_DATABASE_URL=your_test_db_url_here
DEV_DATABASE_URL=your_db_url_here
```

Once those are added you can create and seed the database:

```
$python seed.py
```

After completing all the steps above you will be able to run the app using the following:

```
$flask run
```

You can create your own user profile or use the built in test account with the credentials provided in the seed file.

## User Flow

![Exercise Buddy Splash Page](/app-screenshots/splash-page.png "Exercise Buddy Splash Page")

Users will be required to login or register before accessing the full site.

![Exercise Buddy Home Page](/app-screenshots/home-page.png "Exercise Buddy Home Page")

After logging in, the user will then be asked what muscle group they are interested in working out. The type of exercise and difficulty levels are filters that can be used but are not required to start searching the Exercises API.

![Exercise Buddy Home Page With Search](/app-screenshots/home-page-search.png "Exercise Buddy Home Page With Search")

After searching, a table of the top exercises that meet the requirements will be available for the user to access. The exercise name can be clicked to go to an individual exercise page with more information.

![Exercise Buddy Single Exercise Page](/app-screenshots/exercise-page.png "Exercise Buddy Single Exercise Page")

On each exercise page, there is a more detailed description of the exercise along with the top three most relevant YouTube videos for the exercise (provided by the YouTube API). There is also an option to favorite and unfavorite the exercise. Favoriting an exercise will cause it to be listed on a user's profile page, so they can quickly access it again in the future.

![Exercise Buddy User Page](/app-screenshots/user-page.png "Exercise Buddy User Page")

Each user can view their custom page where they will have their favorited exercises listed and they are able to keep track of what workouts they have done.

## APIs Used

1. Exercises API: [Click Here](https://api-ninjas.com/api/exercises)
2. YouTube API: [Click Here](https://developers.google.com/youtube/v3/docs/videos)
