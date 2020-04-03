from flask import Flask , render_template , redirect , url_for , session ,flash , request 
from flask_socketio import SocketIO , emit ,join_room , leave_room
from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap 

from flask_login import login_user , LoginManager  , login_required , logout_user

from wtforms import StringField , SubmitField , PasswordField, TextAreaField , SelectField
from wtforms.validators import DataRequired 

import random

import Data
import json

from profanity_check import predict

app = Flask(__name__)
bootstrap = Bootstrap(app)
socketio = SocketIO(app)

def createCSRF():

    char_list = 'abcdefghijklmnopqrstuvwxyz1234567890@!#$%&*'

    CSRF_token = ""

    for i in range(30):

        CSRF_token+=char_list[random.randint(0,len(char_list)-1)]

    return CSRF_token

global list_username_choices
global data
global game


list_username_choices = [('0' , 'PSN') , ('1','Steam'),('2','Xbox Live'),('3','Ingame Id'),
('4','Origin'),('5','Google Play'),('6','Apple Game Center')]

class DataFields(FlaskForm):

    name = StringField('Name',validators=[DataRequired()])
    username = StringField('Username',validators=[DataRequired()])
    username_type = SelectField('Username Type' , choices=list_username_choices)
    submit = SubmitField('Submit')

class AddGame(FlaskForm):

    gameName = StringField('name',validators=[DataRequired()])
    submit = SubmitField('submit')

class ChatForm(FlaskForm):

    EnterMessage = TextAreaField('Enter Message:', validators=[DataRequired('Enter message')])
    submit = SubmitField()
    #logout = SubmitField()


def init():

    data_storage = Data.DataStorage()
    game_data = Data.GameSort(data_storage.dict)

    return data_storage , game_data



@app.route('/form',methods=['GET','POST'])
def index():

    data_field_form = DataFields()


    if data_field_form.validate_on_submit():

        username = data_field_form.username.data
        name = data_field_form.name.data

        if 1 in predict([username,name]):

            flash("you can't use inappropraite words , i am smarter than u , bitch")

        else:

            if data.CheckUsername(username,session['game']):

                flash("username already exists")

            else:

                try:

                    new_user = Data.User(name , username , 
                    list_username_choices[int(data_field_form.username_type.data)][1]
                    ,session['game'],data)

                    session['username'] = username

                    return redirect(url_for('userpage'))

                except Exception as e:

                    print(str(e))

                    return render_template('index.html',form = data_field_form,game_test = session['game'])

    return render_template('index.html',form = data_field_form,game_test = session['game'])


@app.route('/userpage',methods=['GET' , 'POST'])
def userpage():

    req_data = dict()
    
    index = 0

    for user in data.dict.values():

        if str(user.game) == session['game']:

            req_data[index] = user
            index+=1
    

    return render_template('userpage.html',req_data=req_data)

@app.route('/')
def home():

    game.Count()
    games_list = game.GetList()

    return render_template('home.html',games_list=games_list)


@app.route('/game<game>')
def gamepage(game):

    session['game'] = game

    return  redirect(url_for('index'))

@app.route('/Chat',methods=['GET','POST'])
def Chat():

    form = ChatForm()

    return render_template('Chat.html',form=form,username=session['username'])

@app.route('/addgame',methods=['GET','POST'])
def addgame():

    form = AddGame()

    if form.validate_on_submit():

        new_game = form.gameName.data

        try:


            if 1 in predict([new_game]):

                flash("you can't use inappropraite words , i am smarter than u , bitch")

            else:

                game.CheckGame(new_game)

                session['game'] = new_game

                return redirect(url_for('index'))

        except Exception as e:

            print(str(e))

    return render_template('addgame.html',form = form)


#SocketIO code 

@socketio.on('connect', namespace='/Chat')
def connect():

    print('Client connected')

    room = session['game']

    join_room(room)

    emit('UserConnectionResponse' , {'username':'server' , 'data':'{} has entered the {} chat'.format(session['username'],room)},room=room)

        

@socketio.on('UserMessage' , namespace = '/Chat')
def UserMessage(message):

    print("{}:{}".format(session['username'] , message))

    room = session['game']
    
    emit('RecieveUserMessage' , {'username':session['username'] , 'data': message},room=room)

@socketio.on('disconnect' , namespace='/Chat')
def disconnected():

    room = session['game']

    leave_room(room)

    print('{} has disconnected'.format(session['username']))

    emit('UserDisconnection' , {'username':'server' , 'data':'{} has left {}'.format(session['username'],room)})

if __name__ == '__main__':

    data,game = init()

    app.config['SECRET_KEY'] = createCSRF()

    socketio.run(app,debug=True)