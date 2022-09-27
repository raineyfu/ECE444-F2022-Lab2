from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from datetime import datetime

from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

import os

class NameForm(FlaskForm):
    name = StringField("What is your name?", validators=[DataRequired()])
    submit = SubmitField("Submit")
    
app = Flask(__name__)

SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

bootstrap = Bootstrap(app)
moment = Moment(app)

@app.route("/", methods=["GET", "POST"])
def index():
    name = None
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get("name")
        if old_name is not None and old_name != form.name.data:
            flash("Looks like you have changed your name!")
        name = form.name.data
        session['name'] = name
        form.name.data = ''
    return render_template('user.html', form=form, name=name, current_time = datetime.utcnow())

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name, current_time = datetime.utcnow())
