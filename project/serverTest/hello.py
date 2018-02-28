from flask import Flask, render_template, session, redirect, url_for, flash, request
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import TextField, IntegerField, TextAreaField
from wtforms import SubmitField, RadioField, SelectField
from wtforms import validators, ValidationError
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_script import Manager

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

bootstrap = Bootstrap(app)
moment = Moment(app)
manager = Manager(app)


class ControlForm(FlaskForm):
    gid = IntegerField("Group Id:   ",[validators.Required("Please enter your name.")])
    pid = IntegerField("Private Id: ",[validators.Required("Please enter your name.")])
    level = IntegerField("Level:     ",[validators.Required("Please enter your name.")])
    cmd = RadioField('Command', choices=[('C','Control'),
    ('N','NewSet'), ('A','Alternative')])
    submit = SubmitField("Send")

class NameForm(FlaskForm):
    name = StringField('What is your name?', validators=[DataRequired()])
    submit = SubmitField('Submit')

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

@app.route('/', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'))

@app.route('/control', methods=['GET', 'POST'])
def contact():
    form = ControlForm()
    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.')
            return render_template('control.html', form=form)
        else:
            gid = request.form['gid']
            pid = request.form['pid']
            level = request.form['level']
            cmd = request.form['cmd']
            print('gid:{}, pid:{}, level:{}, cmd:{}'.format(gid, pid, level, cmd))
            return render_template('control.html', form=form)
    elif request.method == 'GET':
        return render_template('control.html', form=form)


if __name__ == '__main__':
    app.run(debug=True)
    # manager.run()
# python3 hello.py runserver --host 0.0.0.0
