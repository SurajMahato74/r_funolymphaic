from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired, FileAllowed
from wtforms import SubmitField

class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    country = StringField('Country', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

from flask_wtf import FlaskForm
from wtforms import StringField, FileField
from wtforms.validators import InputRequired

class UploadForm(FlaskForm):
    video = FileField('Video', validators=[InputRequired()])
    title = StringField('Title', validators=[InputRequired()])
    category = StringField('Category', validators=[InputRequired()])
    releaseDate = StringField('Release Date', validators=[InputRequired()])
    language = StringField('Language', validators=[InputRequired()])
    
class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Old Password', validators=[DataRequired()])
    new_password = PasswordField('New Password', validators=[DataRequired()])
    submit = SubmitField('Change Password')
    
class LiveUploadForm(FlaskForm):
   video = FileField('Upload Video', validators=[FileRequired(), FileAllowed(['mp4', 'avi'], 'Videos only!')])
   submit = SubmitField('Upload')

class ProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')
    