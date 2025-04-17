from flask import Blueprint, render_template, session, redirect, request
import mysql.connector
from db_connection import *

airline_staff_bp = Blueprint('airline_staff_bp', __name__,template_folder="html_templates", url_prefix='/staff')



# Takes user back to login page if user_id not found
@airline_staff_bp.route("/airline_staff_home")
def airline_staff_home():
    if "user_id" not in session:
        return redirect("/login")
    return render_template("airline_staff_home.html")

# Helper function to get the airline of the staff user
def get_staff_airline():
    username = session.get("user_id")
    if not username:
        return None
    
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        """
        SELECT airline_name 
        FROM airline_staff 
        WHERE username=%s
        """,
        (username,)
    )

    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row[0] if row else None

# Create dashboard of flights the user works, defautling to next 30 days
@airline_staff_bp.route('/home')
def flight_dashboard():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    airline_name = get_staff_airline()

    if airline_name is None:
        return "Unauthorized", 403
    
    to_date   = request.args.get("to_date")
    from_date = request.args.get("from_date")     
    src_code  = request.args.get("src_code")
    dest_code = request.args.get("dest_code")
    city      = request.args.get("city")

    # Building the WHERE clause
    where_parts = ["f.airline_name = %s"]
    parameters = [airline_name]

    if from_date:
        where_parts.append("DATE(f.departure_date_time) >= %s")
        parameters.append(from_date)
    else:
        # default: next 30 days
        where_parts.append(
            "f.departure_date_time BETWEEN NOW() AND DATE_ADD(NOW(), INTERVAL 30 DAY)"
        )

    if to_date:
        where_parts.append("DATE(f.departure_date_time) <= %s")
        parameters.append(to_date)

    if src_code:
        where_parts.append("f.departure_airport_code = %s")
        parameters.append(src_code.upper())

    if dest_code:
        where_parts.append("f.arrival_airport_code = %s")
        parameters.append(dest_code.upper())

    if city:
        # match either departure or arrival city
        where_parts.append("(a1.city = %s OR a2.city = %s)")
        parameters.extend([city, city])

    # join each part of the WHERE with an AND statement
    where_clause = " AND ".join(where_parts)

    # SQL query

    flight_sql = f"""
      SELECT f.*
      FROM flight f
      JOIN airport a1 ON f.departure_airport_code = a1.airport_code
      JOIN airport a2 ON f.arrival_airport_code   = a2.airport_code
      WHERE {where_clause}
      ORDER BY f.departure_date_time;
    """
    
    cursor.execute(flight_sql, tuple(parameters))
    flights = cursor.fetchall()

    # Passenger List
    sel_flight   = request.args.get("flight_number")
    sel_dep_time = request.args.get("dep_time")  
    customers    = None


    if sel_flight and sel_dep_time:
        dep_time_sql = sel_dep_time.replace("T", " ")
        cursor.execute("""
          SELECT c.*
          FROM customers c
          JOIN purchase p ON c.email = p.email
          JOIN ticket   t ON p.ticket_id = t.ticket_id
          WHERE t.flight_number = %s
            AND t.departure_date_time = %s;
        """, (sel_flight, dep_time_sql))
        customers = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template(
        "airline_staff_home.html",
        airline_name = airline_name,
        flights      = flights,
        customers    = customers,
        sel_flight   = sel_flight
    )

    
    







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