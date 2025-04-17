from flask import Blueprint, render_template, session, redirect

customer_bp = Blueprint('customer_bp', __name__)

@customer_bp.route("/customer_home")
def customer_home():
    if "user_id" not in session:
        return redirect("/login")
    return render_template("customer_home.html")

@customer_bp.route("/customer_home/view_my_flights", methods=['GET', 'POST'])
def view_my_flights():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    email = session.get('user_email')
    cursor = mysql.connection.cursor()

    filters = []
    params = [email]

    if request.method == 'POST':
        start_date = request.form.get('start_date')
        end_date = request.form.get('end_date')
        source = request.form.get('source')
        destination = request.form.get('destination')

        if start_date:
            filters.append("f.departure_date_and_time >= %s")
            params.append(start_date)
        if end_date:
            filters.append("f.departure_date_and_time <= %s")
            params.append(end_date)
        if source:
            filters.append("f.departure_airport_code = %s")
            params.append(source)
        if destination:
            filters.append("f.arrival_airport_code = %s")
            params.append(destination)

    base_query = """
        SELECT t.*, f.departure_date_and_time, f.arrival_date_and_time,
               f.departure_airport_code, f.arrival_airport_code, f.status
        FROM ticket t
        JOIN flight f ON t.flight_number = f.flight_number
        WHERE t.email = %s
    """

    if filters:
        base_query += " AND " + " AND ".join(filters)

    base_query += " ORDER BY f.departure_date_and_time"

    cursor.execute(base_query, params)
    flights = cursor.fetchall()
    cursor.close()

    return render_template('view_my_flights.html', flights=flights)


@customer_bp.route('/search_flights', methods=['GET', 'POST'])
def search_flights():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':
        source = request.form.get('source')
        destination = request.form.get('destination')
        departure_date = request.form.get('departure_date')
        return_date = request.form.get('return_date')

        cursor = mysql.connection.cursor()

        try:
            outbound_flights = []
            return_flights = []

            query_out = """
                SELECT * FROM flight 
                WHERE departure_airport_code = %s 
                AND arrival_airport_code = %s 
                AND DATE(departure_date_and_time) = %s
            """
            cursor.execute(query_out, (source, destination, departure_date))
            outbound_flights = cursor.fetchall()

            if return_date:
                query_ret = """
                    SELECT * FROM flight 
                    WHERE departure_airport_code = %s 
                    AND arrival_airport_code = %s 
                    AND DATE(departure_date_and_time) = %s
                """
                cursor.execute(query_ret, (destination, source, return_date))
                return_flights = cursor.fetchall()

            cursor.close()

            return render_template(
                'flight_results.html',
                outbound_flights=outbound_flights,
                return_flights=return_flights
            )

        except Exception as e:
            flash(f'Error: {str(e)}')
            return redirect(url_for('search_flights'))

    return render_template('search_flights.html')

