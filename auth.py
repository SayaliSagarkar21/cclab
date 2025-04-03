from flask import Blueprint, render_template, redirect, url_for, request, flash, session, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required, current_user
from models import User
import requests
import json
import os
from oauthlib.oauth2 import WebApplicationClient

auth = Blueprint('auth', __name__)
client = WebApplicationClient(os.environ.get('GOOGLE_CLIENT_ID'))

def get_google_provider_cfg():
    try:
        return requests.get(current_app.config['GOOGLE_DISCOVERY_URL']).json()
    except:
        return None

@auth.route('/login')
def login():
    if current_user.is_authenticated:
        return redirect(url_for('weather.dashboard'))
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def login_post():
    email = request.form.get('email')
    password = request.form.get('password')
    remember = True if request.form.get('remember') else False

    user = User.get_by_email(email)

    if not user or not check_password_hash(user.password, password):
        flash('Please check your login details and try again.')
        return redirect(url_for('auth.login'))

    user.is_authenticated = True
    login_user(user, remember=remember)
    return redirect(url_for('weather.dashboard'))

@auth.route('/register')
def register():
    if current_user.is_authenticated:
        return redirect(url_for('weather.dashboard'))
    return render_template('register.html')

@auth.route('/register', methods=['POST'])
def register_post():
    email = request.form.get('email')
    name = request.form.get('name')
    password = request.form.get('password')

    user = User.get_by_email(email)

    if user:
        flash('Email address already exists')
        return redirect(url_for('auth.register'))

    new_user = User(
        email=email, 
        name=name, 
        password=generate_password_hash(password, method='pbkdf2:sha256')
    )
    new_user.save()

    return redirect(url_for('auth.login'))

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/login/google')
def google_login():
    google_provider_cfg = get_google_provider_cfg()
    if not google_provider_cfg:
        return "Error loading Google configuration", 500
    
    authorization_endpoint = google_provider_cfg["authorization_endpoint"]
    
    request_uri = client.prepare_request_uri(
        authorization_endpoint,
        redirect_uri=request.base_url + "/callback",
        scope=["openid", "email", "profile"],
    )
    return redirect(request_uri)

@auth.route('/login/google/callback')
def google_callback():
    # Get authorization code Google sent back
    code = request.args.get("code")

    # Find out what URL to hit to get tokens that allow you to ask for
    # things on behalf of a user
    google_provider_cfg = get_google_provider_cfg()
    token_endpoint = google_provider_cfg["token_endpoint"]

    # Prepare and send a request to get tokens
    token_url, headers, body = client.prepare_token_request(
        token_endpoint,
        authorization_response=request.url,
        redirect_url=request.base_url,
        code=code
    )
    token_response = requests.post(
        token_url,
        headers=headers,
        data=body,
        auth=(current_app.config['https://cclab-d97ee-default-rtdb.firebaseio.com/'], current_app.config['AIzaSyB4DLavb41-xR3O1ESyrlOFKNJh5LnuX5w']),
    )

    # Parse the tokens
    client.parse_request_body_response(json.dumps(token_response.json()))

    # Get user info from Google
    userinfo_endpoint = google_provider_cfg["userinfo_endpoint"]
    uri, headers, body = client.add_token(userinfo_endpoint)
    userinfo_response = requests.get(uri, headers=headers, data=body)

    # Make sure their email is verified
    if userinfo_response.json().get("email_verified"):
        google_id = userinfo_response.json()["sub"]
        email = userinfo_response.json()["email"]
        name = userinfo_response.json().get("name", email.split('@')[0])
    else:
        return "User email not available or not verified by Google.", 400

    # Check if user exists by Google ID
    user = User.get_by_google_id(google_id)
    
    if not user:
        # Check if user exists by email
        user = User.get_by_email(email)
        
        if not user:
            # Create new user
            user = User(
                google_id=google_id,
                email=email,
                name=name,
                password=generate_password_hash("", method='pbkdf2:sha256')
            )
            user.save()
        else:
            # Update existing user with Google ID
            user.google_id = google_id
            user.save()

    # Log in the user
    user.is_authenticated = True
    login_user(user)
    return redirect(url_for('weather.dashboard'))