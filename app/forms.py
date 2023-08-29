from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo



class SignUpForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_pass = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField()

class LogInForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField()

class MatchForm(FlaskForm):
    modes = StringField('Player Rating', validators=[DataRequired()])
    maps = StringField('User Info', validators=[DataRequired()])
    submit = SubmitField()

class SearchForm(FlaskForm):
  username = StringField('Search Username', [DataRequired()])
  submit = SubmitField('Search')
