from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime
import re
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, ValidationError
from wtforms.validators import DataRequired, Email

import os

def checkEmail(form, field):
    if ("utoronto" not in str(field)):
        raise ValidationError("Email must be from UofT")

class NameForm(FlaskForm):
    name = StringField("What is your name?", validators=[DataRequired()])
    email = StringField("What is your email?", validators=[DataRequired(), Email(), checkEmail])
    submit = SubmitField("Submit")

app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

bootstrap = Bootstrap(app)
moment = Moment(app)
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
@app.route("/", methods=["GET", "POST"])
def index():
    name = None
    email =None
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get("name")
        if old_name is not None and old_name != form.name.data:
            flash("Looks like you have changed your name!")
        name = form.name.data
        session['name'] = name
        form.name.data = ''

        old_email = session.get("email")
        if (old_email is not None and old_email != form.email.data):
            flash("Looks like you have changed your email")

        email = form.email.data
        session['email'] = email
        form.email.data = ''
    return render_template('user.html', form=form, name=name, current_time = datetime.utcnow(), email=email)

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name, current_time = datetime.utcnow())
