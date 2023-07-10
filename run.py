from time import localtime,strftime
from flask import Flask,render_template,url_for,redirect,flash
from forms import RegistrationForm,LoginForm
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager,UserMixin,login_user,current_user,login_required,logout_user
from flask_socketio import SocketIO,send,emit,join_room,leave_room

app=Flask(__name__)

app.secret_key='9c8f7cfb7c60b59db0b81d7175797aa6'
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///site.db'
db=SQLAlchemy(app)
socketio=SocketIO(app)
bcrypt = Bcrypt(app)
login=LoginManager(app)
login.init_app(app)

ROOMS=['gaming','coding','memes','placement']
class User(UserMixin,db.Model):
	
	id=db.Column(db.Integer, primary_key=True)
	username=db.Column(db.String(125), unique=True, nullable=False)
	password=db.Column(db.String(125), unique=True, nullable=False)
	def __repr__(self):
		return f"User('{self.username}','{self.password}')"

@login.user_loader
def load_user(id):
	return User.query.get(int(id))

@app.route('/',methods=['GET','POST'])
def index():
	form=RegistrationForm()
	if form.validate_on_submit():
		username=form.username.data
		password=form.password.data
		
		hashed_password=bcrypt.generate_password_hash(form.password.data).decode('utf-8')
		user_obj=User.query.filter_by(username=username).first()
		if user_obj:
			return "Someone else already has the username"
		x=User(username=username, password=hashed_password)
		db.session.add(x)
		db.session.commit()
		flash('Registered successfully. Please login', 'success')
		return redirect(url_for('login'))
	return render_template('index.html',form=form)

@app.route('/login',methods=['GET','POST'])
def login():
	form=LoginForm()
	if form.validate_on_submit():
		username=form.username.data
		password=form.password.data
		user_obj=User.query.filter_by(username=username).first()
		if user_obj is None:
			return "Username incorrect or doesn not exist"
		elif user_obj and bcrypt.check_password_hash(user_obj.password,form.password.data):
			login_user(user_obj)
			if current_user.is_authenticated:
				flash('Logged in successfully. Please login', 'success')
				return redirect(url_for('chat'))
		else: 
			"Login Fail"
	return render_template('login.html',form=form)


@app.route('/chat',methods=['GET','POST'])
def chat():
	if not current_user.is_authenticated:
		flash('Please login', 'danger')
		return redirect(url_for('login'))
	return render_template('chat.html', username=current_user.username,rooms=ROOMS)

@app.route('/logout',methods=['GET'])
def logout():
	logout_user()
	flash('Logged out successfully', 'success')
	return redirect(url_for('index'))


#Adding event buckets-server side
#message events bucket keyword:send
@socketio.on('message')
def message(data):
	print(f"\n\n{data}\n\n")
	#Broadcast the mesaage to all clients predefined event bucket caled msg
	send({'msg': data['msg'], 'username': data['username'], 'time_stamp':strftime('%b-%d %I:%M%p',localtime())},room=data['room'])
	
#kwyword:emit
@socketio.on('join')
def join(data):
	join_room(data['room'])
	send({'msg': data['username']+'has joined the '+data['room']+' room'}, room=data['room'])

@socketio.on('leave')
def leave(data):
	leave_room(data['room'])
	send({'msg': data['username']+'has left the '+data['room']+' room'}, room=data['room'])

if(__name__)=='__main__':
	socketio.run(app, debug=True)
