# Import Flask library
from flask import Flask, render_template
from db_connection import *

from routes.airline_staff import airline_staff_bp
from routes.auth import auth_bp
from routes.public_info import public_bp
from routes.customer import customer_bp
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Initialize app from Flask
app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'secret-key')

# Register blueprints
app.register_blueprint(airline_staff_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(public_bp)
app.register_blueprint(customer_bp)

# Production configuration
if os.environ.get('FLASK_ENV') == 'production':
    app.config['DEBUG'] = False
    app.config['TESTING'] = False

# Run the app only if this file is executed directly (for development)
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV') != 'production'
    app.run('0.0.0.0', port, debug=debug_mode)

