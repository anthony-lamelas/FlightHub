from flask import Blueprint, render_template, session, redirect, request
import mysql.connector
from db_connection import *

airline_staff_bp = Blueprint('airline_staff_bp', __name__,template_folder="html_templates")



# Takes user back to login page if user_id not found
@airline_staff_bp.route("/airline_staff_home")
def airline_staff_home():
    if "user_id" not in session:
        return redirect("/login")
    return render_template("airline_staff_home.html")

# Part 1, allows view of future flights
def future_flights():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = '''
        SELECT *
        FROM Flight
        WHERE airline_name = %s
        AND departure_date_time BETWEEN NOW() AND DATE_ADD(NOW(), INTERVAL 30 DAY)
        ORDER BY departure_date_time ASC
    '''

    cursor.execute(query)
    flights = cursor.fetchall()
    conn.close()
    return render_template('airline_staff.html', flights=flights)





# # Part 2, allows staff user to create flights
# @airline_staff_bp.route("/create",metods=['GET', 'POST'])
# def create_flight():
#     if request.method == 'POST':
#         flight_number = request.form['flight_number']
#         departure = request.form['departure']
#         arrival = request.form['arrival']
#         departure_time = request.form['departure_time']

#         conn = get_db_connection()
#         cursor = conn.cursor()

#         query = '''
#             INSERT INTO flights ()
#             VALUES ()
#             '''
        
#         cursor.execute(query, (flight_number, departure, arrival, departure_time))
#         conn.commit()
#         conn.close()
#         return "Flight added successfully!"
    
#     return render_template()