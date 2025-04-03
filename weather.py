from flask import Blueprint, render_template, redirect, url_for, request, flash, current_app
from flask_login import login_required, current_user
import requests
from models import WeatherSearch
from firebase_admin import firestore

weather = Blueprint('weather', __name__)

@weather.route('/dashboard')
@login_required
def dashboard():
    # Get user's recent searches
    recent_searches = WeatherSearch.get_recent_searches_by_user(current_user.id, limit=5)
    return render_template('dashboard.html', name=current_user.name, recent_searches=recent_searches)

@weather.route('/weather', methods=['GET', 'POST'])
@login_required
def get_weather():
    weather_data = None
    city = None
    
    if request.method == 'POST':
        city = request.form.get('city')
        if not city:
            flash('Please enter a city name')
            return redirect(url_for('weather.get_weather'))
        
        api_key = "800577c64d9c09f92eae219696734d04"

        url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"
        
        try:
            response = requests.get(url)
            response.raise_for_status()
            weather_data = response.json()
            
            # Save search to database
            temperature = weather_data.get('main', {}).get('temp')
            description = weather_data.get('weather', [{}])[0].get('description')
            
            new_search = WeatherSearch(
                user_id=current_user.id,
                city=city,
                temperature=temperature,
                description=description
            )
            
            new_search.save()
            
        except requests.exceptions.HTTPError as http_err:
            if response.status_code == 404:
                flash(f"City '{city}' not found. Please check the spelling.")
            else:
                flash(f"HTTP error occurred: {http_err}")
        except Exception as err:
            flash(f"An error occurred: {err}")
    
    return render_template('weather.html', weather=weather_data, city=city)