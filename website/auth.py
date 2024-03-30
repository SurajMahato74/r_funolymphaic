import datetime
import io
import requests
from .models import userdetail, db, User, shows , Favourite, Live, AdminUser
from .forms import RegistrationForm, ChangePasswordForm, LiveUploadForm , ProfileForm, UploadForm
from datetime import datetime
from . import db
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, Response
from website import cv2
from flask_login import LoginManager, current_user, login_required
from flask import Blueprint, request, jsonify
import base64
from flask import request
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required



auth = Blueprint('auth', __name__)

def init_auth(app, cam):
    app.camera = cam   


def generate_frames():
    while True:
        success, frame = camera.read()
        if not success:
            break
        else:
            ret, buffer = cv2.imencode('.jpg', frame)

            # Check if the encoding was successful
            if ret:
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            else:
                # Log or handle the error as needed
                print("Error encoding frame.")



auth = Blueprint('auth', __name__)
camera = None

def init_auth(app, cam):
    global camera
    camera = cam



                                               

@auth.route('/admin')
def admin():
    return render_template('admin.html')                            



@auth.route('/adminform')
def adminform():
    return render_template('adminform.html')

@auth.route('/admintable')
def admintable():
    users = User.query.all()
    # Unhash the passwords
    for user in users:
        unhashed_password = check_password_hash(user.password_hash, user.password_hash)
        user.password = unhashed_password
    return render_template('admintable.html', users=users)



@auth.route('/adminlogin', methods=['GET', 'POST'])
def adminlogin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = AdminUser.query.filter_by(email=email).first()

        if user and user.check_password(password):
            # Set the user session
            session['user_id'] = user.id
            session['user_name'] = user.username 
            return redirect(url_for('auth.radmindashboard'))
            
        else:
            # If user doesn't exist or password is incorrect, show an alert
            flash('Invalid email or password. Please try again.', 'error')

    return render_template('adminlogin.html')


@auth.route('/live_upload', methods=['GET', 'POST'])
def live_upload():
    form = LiveUploadForm()
    if form.validate_on_submit():
        video_file = form.video.data
        new_live = Live(video=video_file.read())
        db.session.add(new_live)
        db.session.commit()
        return redirect(url_for('auth.live_upload'))
    return render_template('live_upload.html', form=form)



@auth.route('/live')
def live():
    user_id = session.get('user_id')
    user = User.query.get(user_id) if user_id else None
    active_tab = 'ongoing'
    upcoming_shows = shows.query.filter(shows.release > datetime.now()).all()
    previous_shows = shows.query.filter(shows.release < datetime.now()).all()
    live_shows = Live.query.all()
    return render_template('live.html', user=user, active_tab=active_tab, upcoming_shows=upcoming_shows, previous_shows=previous_shows, live_shows=live_shows)


@auth.route('/register.html', methods=['GET', 'POST'])
def register():
    print("Entered the register route.")
    form = RegistrationForm()

    if request.method == 'POST' and form.validate():
        print("Form is valid and submitted.")

        # Registration logic here
        email = form.email.data
        password = form.password.data
        name = form.name.data
        country = form.country.data   

        # Check if the email is already registered
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('Email is already registered', 'error')
            return redirect(url_for('auth.register'))

        # Create a new user
        new_user = User(email=email, name=name, country=country)
        new_user.set_password(password)

        # Save the user to the database
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful. You can now log in.', 'success')
        return redirect(url_for('auth.login'))  # Corrected redirection

    else:
        print("Form validation errors:", form.errors)

    country_names = get_country_names()
    return render_template('register.html', form=form, country_names=country_names)

def get_country_names():
    api_endpoint = 'https://restcountries.com/v3.1/all'
    
    response = requests.get(api_endpoint)

    if response.status_code == 200:
        countries = response.json()
        country_names = [country['name']['common'] for country in countries]
        sorted_country_names = sorted(country_names)
        return sorted_country_names
    else:
        return []

@auth.route('/login', methods=['GET', 'POST'])
def loginn():
    if 'user_id' in session:
        # Fetch the user object from the database or use the stored information as needed
        user = User.query.get(session['user_id'])
        shows_data = shows.query.all()

        # Fetch saved shows for the current user from the database
        saved_shows = [fav.show_id for fav in Favourite.query.filter_by(user_id=user.id).all()]

        return render_template('index.html', user=user, shows_data=shows_data, saved_shows=saved_shows)

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        # Find the user by email
        user = User.query.filter_by(email=email).first()

        # Check if the user exists and the password is correct
        if user and user.check_password(password):
            # Set the user session
            session['user_id'] = user.id
            session['user_name'] = user.name 

            # Fetch shows data from the database
            shows_data = shows.query.all()

            # Fetch saved shows for the current user from the database
            saved_shows = [fav.show_id for fav in Favourite.query.filter_by(user_id=user.id).all()]

            # Render admin page with user and shows data
            return render_template('index.html', user=user, shows_data=shows_data, saved_shows=saved_shows)
        else:
            flash('Invalid email or password', 'error')

    return render_template('login.html')


@auth.route('/sports')

def sports():
    user_id = session.get('user_id')
    user = User.query.get(user_id) if user_id else None
    return render_template('sports.html', user=user)

@auth.route('/schedule')

def schedule():
    user_id = session.get('user_id')
    user = User.query.get(user_id) if user_id else None
    return render_template('schedule.html', user=user)

@auth.route('/highlights')
def highlights():
    user_id = session.get('user_id')
    user = User.query.get(user_id) if user_id else None
    return render_template('highlights.html', user=user)

@auth.route('auth/login.html')  # No need to include '/auth' in the route URL
def login():
    return render_template('login.html')

@auth.route('/index.html')  
def index():
    user_id = session.get('user_id')
    user = User.query.get(user_id) if user_id else None
    return render_template('index.html',user=user)

@auth.route('/changepassword')
def changepassword():
        user_id = session.get('user_id')
        user = User.query.get(user_id) if user_id else None
        return render_template('changepassword.html',user=user)

@auth.route('/radmindashboard')
def radmindashboard():
        user_id = session.get('user_id')
        user = User.query.get(user_id) if user_id else None
        return render_template('radmindashboard.html',user=user)



@auth.route('/firm', methods=['GET', 'POST'])
def firm():
    form = UploadForm()
    if form.validate_on_submit():
        try:
            title = form.title.data
            category = form.category.data
            release_date_str = form.releaseDate.data
            release_date = datetime.strptime(release_date_str, '%Y-%m-%d').date()
            language = form.language.data
            
            new_show = shows(
                title=title,
                category=category,
                release=release_date,
                language=language
            )

            db.session.add(new_show)
            db.session.commit()
            
            flash('Files uploaded successfully', 'success')
        except Exception as e:
            flash(f'Error uploading files: {str(e)}', 'error')
    
    return render_template('showupload.html', form=form)



@auth.route('/logout', methods=['GET'])
def logout():
    # Clear the user session
    session.clear()
    # Redirect the user to the login page or any other desired page
    return redirect(url_for('auth.login'))

@auth.route('/adminlogout')
def adminlogout():
    # Clear the session
    session.clear()
    # Redirect to the adminlogin page
    return redirect(url_for('auth.adminlogin'))

@auth.route('/resetuser', methods=['GET', 'POST'])
def resetuser():
    if request.method == 'POST':
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        if user:
            if request.form.get('save'):  # Check if the form is submitted to save changes
                # Update user data with the form values
                user.name = request.form.get('username')
                user.country = request.form.get('country')
                user.contact_number = request.form.get('phone-number')
                # Commit changes to the database
                db.session.commit()
                user_data = {  # Update user_data with the updated values
                    'username': user.name,
                    'email': user.email,
                    'country': user.country,
                    'phone_number': user.contact_number
                }
                flash('Changes saved successfully', 'success')
                return render_template('resetuser.html', user_data=user_data)  # Render template with updated data
            else:
                user_data = {
                    'username': user.name,
                    'email': user.email,
                    'country': user.country,
                    'phone_number': user.contact_number
                }
                return render_template('resetuser.html', user_data=user_data)
        else:
            error_message = 'User not found'
            return render_template('resetuser.html', error_message=error_message)
    else:
        return render_template('resetuser.html')

@auth.route('/update_password', methods=['POST'])
def update_password():
    user_id = session.get('user_id')
    user = User.query.get(user_id) if user_id else None
    email = request.form.get('email')
    new_password = request.form.get('newPassword')
    user = User.query.filter_by(email=email).first()
    if user:
        # Hash the new password and update the user's password
        user.set_password(new_password)
        db.session.commit()
        flash('Password updated successfully', 'success')
    return render_template('login.html', show_password_form=True,user=user)

@auth.route('watchvideo')
def watchvideo():
    user_id = session.get('user_id')
    user = User.query.get(user_id) if user_id else None
    return render_template('watchvideo.html', user=user)