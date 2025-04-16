from flask import Blueprint, render_template, request
from db_connection import *
from datetime import datetime

public_bp = Blueprint('public_bp', __name__)


@public_bp.route("/", methods=["GET", "POST"])

def search_flights():
    source = request.form.get("source")
    destination = request.form.get("destination")
    return_date = request.form.get("return_date")  
    departure_date = request.form.get("departure_date")

    if not departure_date:
        return render_template("home.html", error="Please enter a valid departure date.")

    if return_date:
        return_date = datetime.strptime(return_date, "%Y-%m-%d").strftime("%Y-%m-%d")

    conn = get_db_connection()            # connect to the database
    cursor = conn.cursor(dictionary=True) # create a cursor (can return rows as dictionaries)

    # %s is a placeholder 
    query = """
        SELECT * FROM flight
        WHERE departure_airport_code = %s
        AND arrival_airport_code = %s
        AND DATE(departure_date_time) = %s
        AND departure_date_time > NOW()
    """
    cursor.execute(query, (source, destination, departure_date))
    departing_flights = cursor.fetchall()  # Fetch the results (flights is a list of dictionaries)

    return_flights = []
    if return_date:
        # flip destination and source for round trip
        cursor.execute(query, (destination, source, return_date)) 
        return_flights = cursor.fetchall()  


    print("Source:", source)
    print("Destination:", destination)
    print("Departure Date:", departure_date)
    print("Flights found:", len(departing_flights))

    cursor.close()                        # close the cursor
    conn.close()                          # close the connection

    return render_template(
        "home.html", 
        departing_flights=departing_flights, 
        return_flights=return_flights
        )
    


