from flask import Flask
from flask_login import LoginManager
from dotenv import load_dotenv
import os
from firebase_config import initialize_firebase

# Load environment variables
load_dotenv()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    
    # Configure the app
    app.config.from_object('config.Config')
    
    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # Initialize Firebase
    initialize_firebase()
    
    # Initialize login manager
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    from models import User
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.get_by_id(user_id)
    
    # Register blueprints
    from auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)
    
    from weather import weather as weather_blueprint
    app.register_blueprint(weather_blueprint)
    
    # Register main route
    @app.route('/')
    def index():
        return "Weather App - Navigate to /login or /register"
    
    return app

# Run the app
if __name__ == '__main__':
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))