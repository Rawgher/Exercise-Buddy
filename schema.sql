-- Table: users
CREATE TABLE users (
    username VARCHAR PRIMARY KEY,
    password TEXT NOT NULL,
    email VARCHAR NOT NULL
);

-- Table: exercises
CREATE TABLE exercises (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL
);

-- Table: workout_entries
CREATE TABLE workout_entries (
    id SERIAL PRIMARY KEY,
    user VARCHAR REFERENCES users(username),
    date DATE NOT NULL,
    description TEXT
);

-- Table: user_exercises
CREATE TABLE user_exercises (
    user VARCHAR REFERENCES users(username),
    exercise_id INTEGER REFERENCES exercises(id),
    PRIMARY KEY (user, exercise_id)
);