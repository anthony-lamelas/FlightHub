from flask import Blueprint, render_template, session, redirect, request, flash, url_for
import mysql.connector
from db_connection import *
from datetime import datetime, timedelta

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
            SELECT p.ticket_id, f.flight_number, f.departure_airport_code, f.arrival_airport_code,
                f.departure_date_time, f.arrival_date_time, f.flight_status
            FROM Purchase p
            JOIN Ticket t ON p.ticket_id = t.ticket_id
            JOIN Flight f ON t.flight_number = f.flight_number
                        AND t.departure_date_time = f.departure_date_time
                        AND t.airline_name = f.airline_name
            WHERE p.email = %s AND f.departure_date_time < NOW()
            ORDER BY f.departure_date_time DESC
        """
    else:
        purchase_query = """
            SELECT p.ticket_id, f.flight_number, f.departure_airport_code, f.arrival_airport_code,
                f.departure_date_time, f.arrival_date_time, f.flight_status
            FROM Purchase p
            JOIN Ticket t ON p.ticket_id = t.ticket_id
            JOIN Flight f ON t.flight_number = f.flight_number
                        AND t.departure_date_time = f.departure_date_time
                        AND t.airline_name = f.airline_name
            WHERE p.email = %s AND f.departure_date_time >= NOW()
            ORDER BY f.departure_date_time
        """


    cursor.execute(purchase_query, (user_email,))
    purchased_flights = cursor.fetchall()
    current_time_plus_24 = datetime.now() + timedelta(hours=24)

    cursor.close()
    conn.close()

    return render_template("customer_home.html",
                           upcoming_flights=upcoming_flights,
                           purchased_flights=purchased_flights,
                           filter_type=filter_type,
                           current_time_plus_24=current_time_plus_24)


@customer_bp.route("/purchase_ticket", methods=["POST"])
def purchase_ticket():
    # Check if user is logged in
    if "user_id" not in session or session.get("user_type") != "customer":
        return redirect("/login")

    user_email = session["user_id"]
    flight_number = request.form.get("flight_number")
    departure_date_time = request.form.get("departure_date_time")

    # Collect purchase form data
    first_name = request.form.get("first_name")
    last_name = request.form.get("last_name")
    dob = request.form.get("date_of_birth")
    card_type = request.form.get("card_type")
    card_number = request.form.get("card_number")
    name_on_card = request.form.get("name_on_card")
    expiration_date = request.form.get("expiration_date")

    # Convert 'YYYY-MM' from HTML input to 'YYYY-MM-01'
    if expiration_date:
        expiration_date = expiration_date + "-01"

    conn = get_db_connection()
    cursor = conn.cursor()

    # Step 1: Get an available ticket for this flight
    cursor.execute("""
        SELECT ticket_id, airline_name, flight_number, departure_date_time, sold_price
        FROM Ticket
        WHERE flight_number = %s AND departure_date_time = %s
        LIMIT 1
    """, (flight_number, departure_date_time))
    ticket = cursor.fetchone()

    if not ticket:
        flash("No available tickets for this flight.")
        return redirect("/customer_home")

    ticket_id, airline_name, flight_number, departure_date_time, sold_price = ticket

    # Step 2: Remove the ticket from availability
    cursor.execute("DELETE FROM Ticket WHERE ticket_id = %s", (ticket_id,))

    # Step 3: Insert into Purchase
    cursor.execute("""
        INSERT INTO Purchase (
            email, ticket_id, first_name, last_name, date_of_birth,
            card_type, card_number, name_on_card, expiration_date, purchase_date_time
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, NOW())
    """, (
        user_email, ticket_id, first_name, last_name, dob,
        card_type, card_number, name_on_card, expiration_date
    ))

    conn.commit()
    cursor.close()
    conn.close()

    flash("Ticket purchased successfully!")
    return redirect("/customer_home")


@customer_bp.route("/purchase_ticket_form", methods=["POST"])
def purchase_ticket_form():
    if "user_id" not in session or session.get("user_type") != "customer":
        return redirect("/login")

    flight_number = request.form.get("flight_number")
    departure_date_time = request.form.get("departure_date_time")

    return render_template("purchase_ticket.html",
                           flight_number=flight_number,
                           departure_date_time=departure_date_time)


@customer_bp.route("/cancel_ticket", methods=["POST"])
def cancel_ticket():
    if "user_id" not in session or session.get("user_type") != "customer":
        return redirect("/login")

    user_email = session["user_id"]
    ticket_id = request.form.get("ticket_id")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Step 1: Get flight info for the ticket
    cursor.execute("""
        SELECT t.airline_name, t.flight_number, t.departure_date_time, t.sold_price, f.departure_date_time
        FROM Purchase p
        JOIN Ticket t ON p.ticket_id = t.ticket_id
        JOIN Flight f ON t.flight_number = f.flight_number
                    AND t.departure_date_time = f.departure_date_time
                    AND t.airline_name = f.airline_name
        WHERE p.email = %s AND p.ticket_id = %s
    """, (user_email, ticket_id))

    result = cursor.fetchone()

    # If not result
    if not result:
        flash("Ticket not found or you don't own this ticket.")
        cursor.close()
        conn.close()
        return redirect("/customer_home")

    departure_time = result["departure_date_time"]
    curr_time_plus_24 = datetime.now() + timedelta(hours=24)

    # Step 2: Check timing
    if departure_time <= curr_time_plus_24:
        flash("You can only cancel tickets for flights more than 24 hours in the future.")
    else:
        # Step 3: Cancel the ticket (delete from Purchase, re-add to Ticket if it doesn't already exist)
        cursor.execute("DELETE FROM Purchase WHERE ticket_id = %s AND email = %s", (ticket_id, user_email))

        # Try to reinsert only if it doesn’t exist in Ticket
        cursor.execute("SELECT 1 FROM Ticket WHERE ticket_id = %s", (ticket_id,))
        exists = cursor.fetchone()

        if not exists:
            cursor.execute("""
                INSERT INTO Ticket (ticket_id, airline_name, flight_number, departure_date_time, sold_price)
                VALUES (%s, %s, %s, %s, %s)
            """, (
                ticket_id, result["airline_name"], result["flight_number"],
                result["departure_date_time"], result["sold_price"]
            ))

        conn.commit()
        flash("Ticket canceled successfully.")

    cursor.close()
    conn.close()
    return redirect("/customer_home")
