from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, EmailField, SelectField, TextAreaField, DateField
from wtforms.validators import InputRequired, Email, DataRequired

class RegisterForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])
    email = EmailField("Email", validators=[InputRequired(), Email()])

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[InputRequired()])
    password = PasswordField("Password", validators=[InputRequired()])

class SearchForm(FlaskForm):
    muscle = SelectField('Select A Muscle Group', choices=[('', 'Please Select'), ('abdominals', 'Abs'), ('abductors', 'Abductors'), ('adductors', 'Adductors'), ('biceps', 'Biceps'), ('calves', 'Calves'), ('chest', 'Chest'), ('forearms', 'Forearms'), ('glutes', 'Glutes'), ('hamstrings', 'Hamstrings'), ('lats', 'Lats'), ('lower_back', 'Lower Back'), ('middle_back', 'Middle Back'), ('neck', 'Neck'), ('quadriceps', 'Quadriceps'), ('traps', 'Traps'), ('triceps', 'Triceps')], validators=[InputRequired()])
    type = SelectField('Select An Exercise Type (Optional)', choices=[('', 'Please Select'), ('cardio', 'Cardio'), ('olympic_weightlifting', 'Olympic Lifting'), ('plyometrics', 'Plyometrics'), ('powerlifting', 'Powerlifting'), ('strength', 'Strength'), ('stretching', 'Stretching'), ('strongman', 'Strongman')])
    difficulty = SelectField('Select A Difficulty Level (Optional)', choices=[('', 'Please Select'), ('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('expert', 'Expert')])

class WorkoutEntryForm(FlaskForm):
    date = DateField('Date', format='%Y-%m-%d', validators=[InputRequired()])
    description = TextAreaField('Description', validators=[InputRequired()]) 