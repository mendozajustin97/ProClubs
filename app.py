import os
from flask import Flask, render_template, request, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, EqualTo

from sqlalchemy.sql import func

basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    email = db.Column(db.String(50), nullable=False, unique=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    def __repr__(self):
        return '<Name %r' % self.name
    
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
    
@app.route('/user/add', methods=['GET', 'POST'])
def add_user():
    form = User()
    if form.validate_on_sumbit():
        user = Users.query.filter_by(email=form.email.data).first
        if user is None:
            user = Users(name=form.name.data, email=form.email.data)
            db.session.add(user)
            db.session.commmit()
            flash("User Added Successfully!")
    our_users = Users.query.order_by(Users.date_added)
    return render_template("signup.html", form=form)
    form=form,
    our_users=our_users