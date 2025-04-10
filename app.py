# Import Flask library
from flask import Flask
import pymsql.cursor

# Initialize app from Flask
app = Flask(__name__)

# Define route to hello function
@app.route('/')
def hello():
    return 'Hello World'

# Run the app on localhost
# debug = True -> you don't have to restart flask
# for changes to go through, turn off for production
if __name__ == '__main__':
    app.run('', 5000, debug=True)



@app.route('/')
def home():
    # search form + results for public users
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    # handle user type selection: Customer or Staff
    # show different registration forms or handle in one form
    pass

@app.route('/login', methods=['GET', 'POST'])
def login():
    # similar: detect user type and check correct table
    pass