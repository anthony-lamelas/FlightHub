from flask import Blueprint, render_template, session, redirect, request, flash, url_for
import mysql.connector
from db_connection import *

customer_bp = Blueprint('customer_bp', __name__)

# Main customer home shows future flights by default
@customer_bp.route("/customer_home", methods=["GET", "POST"])
def customer_home():
    if "user_id" not in session or session.get("user_type") != "customer":
        return redirect("/login")

    user_email = session.get("user_id")
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Handle flight filtering (optional)
    query = """
        SELECT flight_number, departure_airport_code, arrival_airport_code,
               departure_date_time, arrival_date_time, flight_status
        FROM flight
        WHERE departure_date_time > NOW()
    """
    filters = []
    values = []

    if request.method == "POST" and 'filter_type' not in request.form:
        from_date = request.form.get("from_date")
        to_date = request.form.get("to_date")
        src_code = request.form.get("src_code")
        dest_code = request.form.get("dest_code")

        if from_date:
            filters.append("DATE(departure_date_time) >= %s")
            values.append(from_date)
        if to_date:
            filters.append("DATE(departure_date_time) <= %s")
            values.append(to_date)
        if src_code:
            filters.append("departure_airport_code = %s")
            values.append(src_code.upper())
        if dest_code:
            filters.append("arrival_airport_code = %s")
            values.append(dest_code.upper())

    if filters:
        query += " AND " + " AND ".join(filters)

    query += " ORDER BY departure_date_time"
    cursor.execute(query, values)
    upcoming_flights = cursor.fetchall()

    # Purchased flights toggle
    filter_type = request.form.get("filter_type", "future")  # default to future
    if filter_type == "past":
        purchase_query = """
            SELECT f.flight_number, f.departure_airport_code, f.arrival_airport_code,
                   f.departure_date_time, f.arrival_date_time, f.flight_status
            FROM Purchase p
            JOIN Ticket t ON p.ticket_id = t.ticket_id
            JOIN Flight f ON t.airline_name = f.airline_name
                         AND t.flight_number = f.flight_number
                         AND t.departure_date_time = f.departure_date_time
            WHERE p.email = %s AND f.departure_date_time < NOW()
            ORDER BY f.departure_date_time DESC
        """
    else:
        purchase_query = """
            SELECT f.flight_number, f.departure_airport_code, f.arrival_airport_code,
                   f.departure_date_time, f.arrival_date_time, f.flight_status
            FROM Purchase p
            JOIN Ticket t ON p.ticket_id = t.ticket_id
            JOIN Flight f ON t.airline_name = f.airline_name
                         AND t.flight_number = f.flight_number
                         AND t.departure_date_time = f.departure_date_time
            WHERE p.email = %s AND f.departure_date_time >= NOW()
            ORDER BY f.departure_date_time
        """

    cursor.execute(purchase_query, (user_email,))
    purchased_flights = cursor.fetchall()

    cursor.close()
    conn.close()

    return render_template("customer_home.html",
                           upcoming_flights=upcoming_flights,
                           purchased_flights=purchased_flights,
                           filter_type=filter_type)
