from flask import Blueprint, render_template, request
from app import get_db_connection

public_bp = Blueprint('public_bp', __name__)


@public_bp.route("/search", methods=["GET", "POST"])

def search_flights():
    source = request.form.get("source")
    destination = request.form.get("destination")
    departure_date = request.form.get("departure_date")

    conn = get_db_connection()            # connect to the database
    cursor = conn.cursor(dictionary=True) # create a cursor (can return rows as dictionaries)

    query = """
        SELECT * FROM Flight
        WHERE departure_airport = %s
        AND arrival_airport = %s
        AND DATE(departure_date_time) = %s
        AND departure_date_time > NOW()
    """

    cursor.close()                        # close the cursor
    conn.close()                          # close the connection
    
