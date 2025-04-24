from flask import Blueprint, render_template, session, redirect, request, flash, url_for
from db_connection import *

airline_staff_bp = Blueprint(
    'airline_staff_bp', __name__,
    template_folder="templates",
    url_prefix='/staff'
)

@airline_staff_bp.route("/airline_staff_home")
def airline_staff_home():
    if "user_id" not in session:
        return redirect("/login")
    return render_template("airline_staff_home.html")


def get_staff_airline():
    username = session.get("user_id")
    if not username:
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
    if "user_id" not in session:
        return redirect("/login")

    airline_name = get_staff_airline()
    if airline_name is None:
        return "Unauthorized", 403

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

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
            "flight.departure_date_time BETWEEN NOW() AND DATE_ADD(NOW(), INTERVAL 30 DAY)"
        )
    else:
        where_parts = ["flight.airline_name = %s"]

        # date filters
        if from_date and to_date:
            where_parts.append(
                "DATE(flight.departure_date_time) BETWEEN %s AND %s"
            )
            parameters.extend([from_date, to_date])
        elif from_date:
            where_parts.append("DATE(flight.departure_date_time) >= %s")
            parameters.append(from_date)
        elif to_date:
            where_parts.append("DATE(flight.departure_date_time) <= %s")
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

    # optional: load passengers for a selected flight
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
    if "user_id" not in session:
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
        cursor.close()
        conn.close()

        # back to the dashboard
        return redirect("/staff/home")

    # GET → render the form
    return render_template('create_flight.html')



#--------------worked from here--------------
@airline_staff_bp.route('/change_status', methods=['GET', 'POST'])
def change_flight_status():
    if "user_id" not in session:
        flash('Please log in as staff for access')
        return redirect(url_for('login'))

    # 1. Open connection and cursor
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    # 2. Fetch all flight numbers from the database
    cursor.execute("SELECT flight_number FROM flight")
    flights = cursor.fetchall()

    # Optional debug:
    print("DEBUG: flights =", flights)

    # 3. Handle POST (status update)
    if request.method == 'POST':
        new_status = request.form.get('flight_status')
        flight_number = request.form.get('flight_number')
        try:
            cursor.execute(
                """
                UPDATE flight
                SET flight_status = %s
                WHERE flight_number = %s
                """,
                (new_status, flight_number)
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
#-------------------airline works -----------------------------

@airline_staff_bp.route('/add_airplane', methods=['GET', 'POST'])
def add_airplane():
    if "user_id" not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        airline_name          = request.form.get('airline_name')
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
            return redirect(url_for('airline_staff_bp.flight_dashboard'))
        finally:
            cursor.close()
            conn.close()

    return render_template('add_airplane.html')


    #-------------------worked upto here-----------------------------

        # back to the dashboard
    return redirect("/staff/home")

    # GET → render the form
    return render_template('create_flight.html')

