from flask import Blueprint, render_template, session, redirect, request, flash, url_for
import psycopg2
import psycopg2.extras
from db_connection import *
from datetime import datetime, timedelta

airline_staff_bp = Blueprint(
    'airline_staff_bp', __name__,
    template_folder="templates",
    url_prefix='/staff'
)

@airline_staff_bp.route("/airline_staff_home")
def airline_staff_home():
    if "user_id" not in session or session.get("user_type") != "staff":
        return redirect("/login")
    return render_template("airline_staff_home.html")


def get_staff_airline():
    username = session.get("user_id")
    if not username or session.get("user_type") != "staff":
        return None

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        "SELECT airline_name FROM airline_staff WHERE username = %s",
        (username,)
    )
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return row[0] if row else None


@airline_staff_bp.route('/home')
def flight_dashboard():
    # require login
    if "user_id" not in session or session.get("user_type") != "staff":
        return redirect("/login")

    airline_name = get_staff_airline()
    if airline_name is None:
        return "Unauthorized", 403

    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    # get filter parameters
    from_date = request.args.get("from_date")
    to_date   = request.args.get("to_date")
    src_code  = request.args.get("src_code")
    dest_code = request.args.get("dest_code")

    # build WHERE clauses
    parameters = [airline_name]

    # default: next 30 days if no filters at all
    if not any([from_date, to_date, src_code, dest_code]):
        where_clause = (
            "flight.airline_name = %s AND "
            "flight.departure_date_time BETWEEN NOW() AND NOW() + INTERVAL '30 days'"
        )
    else:
        where_parts = ["flight.airline_name = %s"]

        # date filters
        if from_date and to_date:
            where_parts.append(
                "flight.departure_date_time::date BETWEEN %s AND %s"
            )
            parameters.extend([from_date, to_date])
        elif from_date:
            where_parts.append("flight.departure_date_time::date >= %s")
            parameters.append(from_date)
        elif to_date:
            where_parts.append("flight.departure_date_time::date <= %s")
            parameters.append(to_date)
        # if neither from_date nor to_date, do not add any date filter here

        # airport code filters
        if src_code:
            where_parts.append("flight.departure_airport_code = %s")
            parameters.append(src_code.upper())
        if dest_code:
            where_parts.append("flight.arrival_airport_code = %s")
            parameters.append(dest_code.upper())

        where_clause = " AND ".join(where_parts)

    # build and execute query
    flight_sql = f"""
        SELECT *
        FROM flight
        WHERE {where_clause}
        ORDER BY departure_date_time;
    """
    cursor.execute(flight_sql, tuple(parameters))
    flights = cursor.fetchall()

    # load passengers for a selected flight
    sel_flight   = request.args.get("flight_number")
    sel_dep_time = request.args.get("dep_time")
    customers    = None
    if sel_flight and sel_dep_time:
        dep_time_sql = sel_dep_time.replace("T", " ")
        cursor.execute(
            """
            SELECT c.*
            FROM customers c
            JOIN purchase  p ON c.email      = p.email
            JOIN ticket    t ON p.ticket_id  = t.ticket_id
            WHERE t.flight_number        = %s
              AND t.departure_date_time = %s;
            """,
            (sel_flight, dep_time_sql)
        )
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

@airline_staff_bp.route('/passengers')
def view_flight_customers():
    return flight_dashboard()

# Part 2, allows staff user to create flights
@airline_staff_bp.route('/create', methods=['GET', 'POST'])
def create_flight():
    # require login
    if "user_id" not in session or session.get("user_type") != "staff":
        return redirect("/login")
    airline_name = get_staff_airline()
    if airline_name is None:
        return "Unauthorized", 403

    if request.method == 'POST':
        # gather all fields
        airplane_id            = request.form.get('airplane_id')
        flight_number          = request.form.get('flight_number')
        airport_code           = request.form.get('airport_code').upper()
        departure_airport_code = request.form.get('departure_airport_code').upper()
        arrival_airport_code   = request.form.get('arrival_airport_code').upper()
        departure_date_time    = request.form.get('departure_date_time').replace('T', ' ')
        arrival_date_time      = request.form.get('arrival_date_time').replace('T', ' ')
        base_price             = request.form.get('base_price')
        airplane_number        = request.form.get('airplane_number')
        flight_status          = request.form.get('flight_status')

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO flight (
                airline_name, airplane_id, flight_number, airport_code,
                departure_airport_code, arrival_airport_code,
                departure_date_time, arrival_date_time,
                base_price, airplane_number, flight_status
                ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """,
                (
                    airline_name, airplane_id, flight_number, airport_code,
                    departure_airport_code, arrival_airport_code,
                    departure_date_time, arrival_date_time,
                    base_price, airplane_number, flight_status
                )
            )
            conn.commit()
            return redirect("/staff/home")

        except psycopg2.IntegrityError:
            conn.rollback()
            flash("Flight already exists or is invalid.")
            return redirect("/staff/create")

        finally:
            cursor.close()
            conn.close()

    # GET → render the form
    return render_template('create_flight.html')


#--------------worked from here--------------
@airline_staff_bp.route('/status', methods=['GET', 'POST'])
def change_flight_status():
    if "user_id" not in session or session.get("user_type") != "staff":
        flash('Please log in as staff for access')
        return redirect(url_for('login'))

    # 1. Open connection and cursor
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    airline_name = get_staff_airline()

    # 2. Fetch all flight numbers from the database
    cursor.execute(
        """SELECT flight_number, departure_date_time
        FROM flight
        WHERE airline_name = %s
        ORDER BY departure_date_time DESC
        """, (airline_name,))
    
    flights = cursor.fetchall()

    # Optional debug:
    print("DEBUG: flights =", flights)

    # 3. Handle POST (status update)
    if request.method == 'POST':
        new_status = request.form.get('flight_status')
        flight_info = request.form.get('flight_info')
        flight_number, dep_time = flight_info.split("||")
 
        try:
            cursor.execute(
                """
                UPDATE flight
                SET flight_status = %s
                WHERE flight_number = %s
                AND departure_date_time = %s
                AND airline_name = %s
                """,
                (new_status, flight_number, dep_time, airline_name)
            )
            conn.commit()
            flash('Flight status has been updated successfully.')
        except Exception as e:
            flash(f'Error updating flight status: {e}')
        finally:
            cursor.close()
            conn.close()

        return redirect(url_for('airline_staff_bp.flight_dashboard'))

    # 4. GET → render form with the `flights` list
    cursor.close()
    conn.close()
    return render_template(
        'change_flight_status.html',
        flights=flights
    )

@airline_staff_bp.route('/add-plane', methods=['GET', 'POST'])
def add_airplane():
    if "user_id" not in session or session.get("user_type") != "staff":
        return redirect(url_for('login'))

    if request.method == 'POST':
        airline_name          = get_staff_airline()
        airplane_id           = request.form.get('airplane_id')
        number_of_seats       = request.form.get('number_of_seats')
        manufacturing_company = request.form.get('manufacturing_company')

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO airplane (
                    airplane_id, airline_name, number_of_seats, manufacturing_company
                ) VALUES (%s, %s, %s, %s)
                """,
                (airplane_id, airline_name, number_of_seats, manufacturing_company)
            )
            conn.commit()
            flash("Airplane added successfully.", "success")
            return redirect(url_for('airline_staff_bp.flight_dashboard'))

        except psycopg2.IntegrityError:
            conn.rollback()
            flash("Airplane already exists or is invalid.", "error")
            return redirect("/staff/add-plane")

        except Exception as e:
            conn.rollback()
            flash(f"Unexpected error: {str(e)}", "error")
            return redirect("/staff/add-plane")

        finally:
            cursor.close()
            conn.close()

    return render_template('add_airplane.html')

# Add Airport
@airline_staff_bp.route('/add-airport', methods=['GET', 'POST'])
def add_airport():
    if "user_id" not in session or session.get("user_type") != "staff":
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        airport_code   = request.form.get('airport_code')
        airport_name   = request.form.get('airport_name')
        city           = request.form.get('city')
        country        = request.form.get('country')

        conn = get_db_connection()
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                INSERT INTO airport (
                    airport_code, airport_name, city, country
                ) VALUES (%s, %s, %s, %s)
                """,
                (airport_code, airport_name, city, country)
            )
            conn.commit()
            flash("Airport added successfully.", "success")
            return redirect(url_for('airline_staff_bp.flight_dashboard'))

        except psycopg2.IntegrityError:
            conn.rollback()
            flash("Airport already exists or input is invalid.", "error")
            return redirect("/staff/add-airport")

        except Exception as e:
            conn.rollback()
            flash(f"Unexpected error: {str(e)}", "error")
            return redirect("/staff/add-airport")

        finally:
            cursor.close()
            conn.close()

    return render_template('add_airport.html')

# View flight ratings
@airline_staff_bp.route('/flight-ratings', methods=['GET', 'POST'])
def view_ratings():
    if "user_id" not in session or session.get("user_type") != "staff":
        return redirect(url_for('auth.login'))

    airline_name = get_staff_airline()
    ratings_data = []

    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    try:
        query = """
                SELECT f.flight_number,
                    AVG(r.rating) AS avg_rating,
                    STRING_AGG(r.comments, ' || ') AS comments
                FROM review r
                JOIN ticket t ON r.ticket_id = t.ticket_id
                JOIN flight f ON t.airline_name = f.airline_name
                AND t.flight_number = f.flight_number
                AND t.departure_date_time = f.departure_date_time
                WHERE f.airline_name = %s
                GROUP BY f.flight_number;
            """
        cursor.execute(query, (airline_name,))
        ratings_data = cursor.fetchall()

    finally:
        cursor.close()
        conn.close()

    return render_template('view_ratings.html', ratings=ratings_data)

@airline_staff_bp.route('/view-reports', methods=['GET','POST'])
def view_reports():
    if "user_id" not in session or session.get("user_type") != "staff":
        return redirect(url_for('auth.login'))
    
    airline_name = get_staff_airline()
    from_date = request.args.get("from_date")
    to_date   = request.args.get("to_date")

    # default to last year if no dates are provided
    if not from_date or not to_date:
        today = datetime.today()
        from_date = (today.replace(year=today.year-1)).strftime('%Y-%m-%d')
        to_date = today.strftime('%Y-%m-%d')

    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    try:
        query = """
                            SELECT EXTRACT(YEAR FROM p.purchase_date_time) AS year,
                   EXTRACT(MONTH FROM p.purchase_date_time) AS month,
                    COUNT(*) AS tickets_sold
                    FROM ticket t JOIN purchase p ON t.ticket_id = p.ticket_id
                    WHERE t.airline_name = %s
                    AND p.purchase_date_time BETWEEN %s AND %s
                    GROUP BY EXTRACT(YEAR FROM p.purchase_date_time), EXTRACT(MONTH FROM p.purchase_date_time)
                    ORDER BY year, month
                """
        cursor.execute(query,(airline_name,from_date,to_date))
        report_data = cursor.fetchall()
        for row in report_data:
            month_number = int(row['month'])  # Convert Decimal to int
            month_name = datetime(1900, month_number, 1).strftime('%B')  # January, February, etc.
            row['month_name'] = month_name
        
    finally:
        cursor.close()
        conn.close()

    return render_template('view_reports.html', report_data=report_data, from_date=from_date, to_date=to_date)

