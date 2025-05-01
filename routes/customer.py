from flask import Blueprint, render_template, session, redirect, request, flash, url_for
import mysql.connector
from db_connection import *
from datetime import datetime, timedelta

customer_bp = Blueprint('customer_bp', __name__)

# Main customer home shows future flights by default
@customer_bp.route("/customer-home", methods=["GET", "POST"])
def customer_home():
    if "user_id" not in session or session.get("user_type") != "customer":
        return redirect("/login")

    user_email = session.get("user_id")
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # Handle flight filtering 
    query = """
        SELECT DISTINCT f.flight_number, f.departure_airport_code, f.arrival_airport_code,
                        f.departure_date_time, f.arrival_date_time, f.flight_status
        FROM Flight f
        JOIN Ticket t ON f.flight_number = t.flight_number
                    AND f.departure_date_time = t.departure_date_time
                    AND f.airline_name = t.airline_name
        WHERE t.is_purchased = FALSE AND f.departure_date_time > NOW()
    """
    filters = []
    values = []

    if request.method == "POST" and 'filter_type' not in request.form:
        from_date = request.form.get("from_date")
        to_date = request.form.get("to_date")
        src_code = request.form.get("src_code")
        dest_code = request.form.get("dest_code")

        if from_date:
            filters.append("DATE(f.departure_date_time) >= %s")
            values.append(from_date)
        if to_date:
            filters.append("DATE(f.departure_date_time) <= %s")
            values.append(to_date)
        if src_code:
            filters.append("f.departure_airport_code = %s")
            values.append(src_code.upper())
        if dest_code:
            filters.append("f.arrival_airport_code = %s")
            values.append(dest_code.upper())

    if filters:
        query += " AND " + " AND ".join(filters)

    query += " ORDER BY f.departure_date_time"
    cursor.execute(query, values)
    upcoming_flights = cursor.fetchall()

    # Purchased flights toggle
    filter_type = request.form.get("filter_type", "future")  # default to future
    if filter_type == "past":
        purchase_query = """
            SELECT p.ticket_id, f.flight_number, f.departure_airport_code, f.arrival_airport_code,
                   f.departure_date_time, f.arrival_date_time, f.flight_status, t.sold_price
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
                   f.departure_date_time, f.arrival_date_time, f.flight_status, t.sold_price
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


@customer_bp.route("/purchase-ticket", methods=["POST"])
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

    # 1) Get airplane_id and capacity for the flight
    cursor.execute("""
        SELECT f.airline_name, f.airplane_id, f.base_price, a.number_of_seats
        FROM Flight f
        JOIN Airplane a ON f.airplane_id = a.airplane_id
        WHERE f.flight_number = %s AND f.departure_date_time = %s
    """, (flight_number, departure_date_time))
    flight_data = cursor.fetchone()

    if not flight_data:
        flash("Flight not found.")
        return redirect("/customer_home")

    airline_name, airplane_id, base_price, total_seats = flight_data

    # 2) Count how many seats are booked (is_purchased = TRUE)
    cursor.execute("""
        SELECT COUNT(*) FROM Ticket
        WHERE flight_number = %s AND departure_date_time = %s AND airline_name = %s AND is_purchased = TRUE
    """, (flight_number, departure_date_time, airline_name))
    booked_seats = cursor.fetchone()[0]

    if booked_seats >= total_seats:
        flash("This flight is fully booked.")
        return redirect("/customer_home")

    # 3) Find an available ticket (not purchased)
    cursor.execute("""
        SELECT ticket_id, sold_price FROM Ticket
        WHERE flight_number = %s AND departure_date_time = %s AND airline_name = %s AND is_purchased = FALSE
        LIMIT 1
    """, (flight_number, departure_date_time, airline_name))
    ticket = cursor.fetchone()

    if not ticket:
        flash("No available tickets for this flight.")
        return redirect("/customer_home")

    ticket_id, sold_price = ticket

    # 4) Update price if demand > 60%
    if booked_seats >= 0.6 * total_seats:
        sold_price = round(base_price * 1.2, 2)
    else:
        sold_price = base_price

    # 5) Update ticket as purchased and price
    cursor.execute("""
        UPDATE Ticket
        SET is_purchased = TRUE, sold_price = %s
        WHERE ticket_id = %s
    """, (sold_price, ticket_id))

    # 6) Insert into Purchase table
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



@customer_bp.route("/purchase-ticket-form", methods=["POST"])
def purchase_ticket_form():
    if "user_id" not in session or session.get("user_type") != "customer":
        return redirect("/login")

    flight_number = request.form.get("flight_number")
    departure_date_time = request.form.get("departure_date_time")

    return render_template("purchase_ticket.html",
                           flight_number=flight_number,
                           departure_date_time=departure_date_time)


@customer_bp.route("/cancel-ticket", methods=["POST"])
def cancel_ticket():
    if "user_id" not in session or session.get("user_type") != "customer":
        return redirect("/login")

    user_email = session["user_id"]
    ticket_id = request.form.get("ticket_id")

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # 1) Get flight departure time for the ticket
    cursor.execute("""
        SELECT f.departure_date_time
        FROM Purchase p
        JOIN Ticket t ON p.ticket_id = t.ticket_id
        JOIN Flight f ON t.flight_number = f.flight_number
                     AND t.departure_date_time = f.departure_date_time
                     AND t.airline_name = f.airline_name
        WHERE p.email = %s AND p.ticket_id = %s
    """, (user_email, ticket_id))

    result = cursor.fetchone()

    if not result:
        flash("Ticket not found or you don't own this ticket.")
        cursor.close()
        conn.close()
        return redirect("/customer_home")

    departure_time = result["departure_date_time"]
    curr_time_plus_24 = datetime.now() + timedelta(hours=24)

    # 2) Check if cancellation is allowed
    if departure_time <= curr_time_plus_24:
        flash("You can only cancel tickets for flights more than 24 hours in the future.")
    else:
        # 3) Cancel the ticket if allowed (mark Ticket as not purchased, delete from Purchase)
        cursor.execute("""
            UPDATE Ticket
            SET is_purchased = FALSE
            WHERE ticket_id = %s
        """, (ticket_id,))

        cursor.execute("""
            DELETE FROM Purchase
            WHERE ticket_id = %s AND email = %s
        """, (ticket_id, user_email))

        conn.commit()
        flash("Ticket canceled successfully.")

    cursor.close()
    conn.close()
    return redirect("/customer_home")


@customer_bp.route("/review-ticket-form", methods=["POST"])
def review_ticket_form():
    if "user_id" not in session or session.get("user_type") != "customer":
        return redirect("/login")

    ticket_id = request.form.get("ticket_id")
    return render_template("review_ticket.html", ticket_id=ticket_id)


@customer_bp.route("/submit-review", methods=["POST"])
def submit_review():
    if "user_id" not in session or session.get("user_type") != "customer":
        return redirect("/login")

    user_email = session["user_id"]
    ticket_id = request.form.get("ticket_id")
    rating = request.form.get("rating")
    comments = request.form.get("comments")

    conn = get_db_connection()
    cursor = conn.cursor()

    # Check if review already exists for this ticket to prevent duplicates
    cursor.execute("SELECT * FROM Review WHERE email = %s AND ticket_id = %s", (user_email, ticket_id))
    if cursor.fetchone():
        flash("You have already reviewed this flight.")
        cursor.close()
        conn.close()
        return redirect("/customer_home")

    cursor.execute("""
        INSERT INTO Review (email, ticket_id, comments, rating)
        VALUES (%s, %s, %s, %s)
    """, (user_email, ticket_id, comments, rating))

    conn.commit()
    cursor.close()
    conn.close()

    flash("Thank you for your feedback!")
    return redirect("/customer_home")

