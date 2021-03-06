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
from frame import Frame

from threading import Thread, Lock
from hksSer import serThread, serVar
import time

mySer = serThread()
mySerVar = serVar

app = Flask(__name__)
app.config['SECRET_KEY'] = 'hard to guess string'

bootstrap = Bootstrap(app)
moment = Moment(app)
manager = Manager(app)

class ControlForm(FlaskForm):
    gid = IntegerField("Group Id:   ",[validators.Required("Please enter your name.")])
    pid = IntegerField("Private Id: ",[validators.Required("Please enter your name.")])
    level = IntegerField("Level:     ",[validators.Required("Please enter your name.")])
    sub = RadioField('Command', choices=[('103','Control'),
    ('104','NewSet'), ('109','Alternative'), ('110','Status'), ('101','Power')])
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

@app.route('/index', methods=['GET', 'POST'])
def index():
    form = NameForm()
    if form.validate_on_submit():
        old_name = session.get('name')
        if old_name is not None and old_name != form.name.data:
            flash('Looks like you have changed your name!')
        session['name'] = form.name.data
        return redirect(url_for('index'))
    return render_template('index.html', form=form, name=session.get('name'))

@app.route('/test', methods=['GET', 'POST'])
def test():
    form = ControlForm()
    if form.validate_on_submit():
        print('validate_on_submit')
        myFrame = Frame()
        myFrame.setFrame()
        print(myFrame.getFrame())
        print('bsl frame test')
    return render_template('control.html', form=form)

class testThread(Thread):
    def __init__(self):
        print('Start testThread')
        Thread.__init__(self)
    def run(self):
        while True:
            time.sleep(1) #for thread, very important
            if mySer.myVar.readFlag:
                mySer.myVar.readFlag = False
                print('var:{}'.format(mySerVar.readFlag))
                mySer.send(mySer.readStr)
                print('self.myVar.readFlag')
        print('End of testThread')


testThreadFirstFlag = True
@app.route('/new', methods=['GET', 'POST'])
def new():
    form = ControlForm()
    global testThreadFirstFlag
    if testThreadFirstFlag:
        print('Generate testThread')
        testThreadFirstFlag = False
        myThread = testThread()
        myThread.start()
    return render_template('control.html', form=form)

@app.route('/stop', methods=['GET', 'POST'])
def stop():
    form = ControlForm()
    if mySer.getSerAlive():
        mySer.send('Quit Serial')
    else:
        print('at start Finished Serial')
    return render_template('control.html', form=form)

@app.route('/start', methods=['GET', 'POST'])
def startSer():
    form = ControlForm()
    if mySer.serFirstFlag:
        mySer.serFirstFlag = False
        mySer.start()
        print('Now start my Serial')
        time.sleep(1)
    return render_template('control.html', form=form)

@app.route('/', methods=['GET', 'POST'])
def control():
    startSer()
    form = ControlForm()
    if request.method == 'POST':
        if form.validate() == False:
            flash('All fields are required.')
            print('form.validate() == False:')
            return render_template('control.html', form=form)
        else:
            myFrame = Frame()
            gid = request.form['gid']
            pid = request.form['pid']
            level = request.form['level']
            sub = request.form['sub']
            print('gid:{}, pid:{}, level:{}, sub:{}'.format(gid, pid, level, sub))
            myFrame.setGid(int(gid)); myFrame.setPid(int(pid)); myFrame.setLevel(int(level));
            myFrame.setSub(int(sub))
            myFrame.setFrame()
            mySer.send(myFrame.getFrame())
            return render_template('control.html', form=form)

    elif request.method == 'GET':
        print('request.method == GET ')
        return render_template('control.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)
    print('Now Run')
    # manager.run()
# python3 hello.py runserver --host 0.0.0.0
