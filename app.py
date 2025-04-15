from flask import Flask, render_template
import mysql.connector

# Import Blueprints from your routes folder
from routes.public_info import public_bp
from routes.auth import auth_bp
from routes.airline_staff import staff_bp
from routes.customer import customer_bp

# Initialize Flask app and set template folder
app = Flask(__name__, template_folder='html_templates')

# Secret key is required for session handling
app.secret_key = "supersecretkey"  

# Register Blueprints
app.register_blueprint(public_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(staff_bp)
app.register_blueprint(customer_bp)

# Public homepage
@app.route('/')
def home():
    return render_template('home.html')

# Shared DB connection function
def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',
        port=8889,
        user='root',
        password='root',
        database='air_ticket_db'
    )
    return conn

# Run the app
if __name__ == '__main__':
    app.run(host='localhost', port=5000, debug=True)
