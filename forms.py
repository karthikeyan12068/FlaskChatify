from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField
from wtforms.validators import InputRequired,Length,EqualTo,ValidationError
class RegistrationForm(FlaskForm):
	username=StringField('username_label',
		validators=[InputRequired(message="Username Required"),
		Length(min=4,max=25,message="Between 4 and 25 chars")])
	password=PasswordField('password_label',
		validators=[InputRequired(message="Password Required"),
		Length(min=4,max=25,message="Between 4 and 25 chars")])
	confirm_pswd=PasswordField('confirm_pswd_label',
		validators=[InputRequired(message="Password Required"),
		Length(min=4,max=25,message="Passwords must match")])
	submit=SubmitField('Create')

class LoginForm(FlaskForm):
	username=StringField('username_label',
		validators=[InputRequired(message="Username Required"),
		Length(min=4,max=25,message="Between 4 and 25 chars")])
	password=PasswordField('password_label',
		validators=[InputRequired(message="Password Required"),
		Length(min=4,max=25,message="Between 4 and 25 chars")])
	submit=SubmitField('Login')
	
