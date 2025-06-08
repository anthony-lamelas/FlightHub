from flask import Blueprint, render_template, request
import psycopg2
import psycopg2.extras
from db_connection import *
from datetime import datetime

public_bp = Blueprint('public_bp', __name__)

@public_bp.route("/", methods=["GET", "POST"])
def search_flights():
    departing_flights = []
    return_flights = []

    if request.method == "POST":
        source = request.form.get("source", "").strip().lower()
        destination = request.form.get("destination", "").strip().lower()
        departure_date = request.form.get("departure_date", "")
        return_date = request.form.get("return_date", "")

        if return_date:
            return_date = datetime.strptime(return_date, "%Y-%m-%d").strftime("%Y-%m-%d")

        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        # Query for departing flights
        query = """
            SELECT f.*
            FROM flight f
            JOIN airport a1 ON f.departure_airport_code = a1.airport_code
            JOIN airport a2 ON f.arrival_airport_code = a2.airport_code
            WHERE f.departure_date_time > NOW()
        """
        params = []

        if source:
            query += " AND (LOWER(f.departure_airport_code) = %s OR LOWER(a1.city) = %s)"
            params.extend([source, source])

        if destination:
            query += " AND (LOWER(f.arrival_airport_code) = %s OR LOWER(a2.city) = %s)"
            params.extend([destination, destination])

        if departure_date:
            query += " AND DATE(f.departure_date_time) = %s"
            params.append(departure_date)

        cursor.execute(query, tuple(params))
        departing_flights = cursor.fetchall()

        # Query for return flights (optional)
        if return_date and source and destination:
            cursor.execute(query, tuple([
                destination, destination,  # flip src/dest
                source, source,
                return_date
            ]))
            return_flights = cursor.fetchall()

        cursor.close()
        conn.close()

    return render_template(
        "home.html",
        departing_flights=departing_flights,
        return_flights=return_flights
    )

