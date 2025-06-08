# Import Flask library
from flask import Flask, render_template
from db_connection import *

from routes.airline_staff import airline_staff_bp
from routes.auth import auth_bp
from routes.public_info import public_bp
from routes.customer import customer_bp
from dotenv import load_dotenv

# Initialize app from Flask
app = Flask(__name__)
app.secret_key = 'secret-key'
app.register_blueprint(airline_staff_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(public_bp)
app.register_blueprint(customer_bp)

# Run the app on localhost
# debug = True -> you don't have to restart flask
# for changes to go through, turn off for production
if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 5000))
    app.run('0.0.0.0', port, debug=False)

