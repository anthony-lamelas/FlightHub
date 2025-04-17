from flask import Blueprint, render_template, session, redirect

customer_bp = Blueprint('customer_bp', __name__)

@customer_bp.route("/customer_home")
def customer_home():
    if "user_id" not in session:
        return redirect("/login")
    return render_template("customer_home.html")

@customer_bp.route('/customer_homepage/view_my_flights')
def view_my_flights():
    if 'user_id' in session and session.get('user_type') == 'customer':
        email = session.get('user_email')
        cursor = mysql.connection.cursor()

        cursor.execute("""
            SELECT t.*, f.departure_date_and_time, f.arrival_date_and_time, 
                   f.departure_airport_code, f.arrival_airport_code, f.status
            FROM ticket t
            JOIN flight f ON t.flight_number = f.flight_number
            WHERE t.email = %s AND f.departure_date_and_time > NOW()
            ORDER BY f.departure_date_and_time
            """, [email])
        upcoming_flights = cursor.fetchall()

        cursor.execute("""
            SELECT t.*, f.departure_date_and_time, f.arrival_date_and_time, 
                   f.departure_airport_code, f.arrival_airport_code, f.status
            FROM ticket t
            JOIN flight f ON t.flight_number = f.flight_number
            WHERE t.email = %s AND f.departure_date_and_time < NOW()
            ORDER BY f.departure_date_and_time DESC
            """, [email])
        past_flights = cursor.fetchall()

        cursor.close()
        return render_template('view_my_flights.html', upcoming_flights=upcoming_flights, past_flights=past_flights)
    else:
        flash('Please log in to view your flights.')
        return redirect(url_for('login'))

customer_bp.route('/search_flights', methods=['GET', 'POST'])
def search_flights():
    if 'user_id' not in session:
        flash('Please log in to search for flights.')
        return redirect('/login')

    if request.method == 'POST':
        source = request.form.get('source')
        destination = request.form.get('destination')
        departure_date = request.form.get('departure_date')

        cursor = mysql.connection.cursor()
        
        try:
            query = '''
                SELECT f.airline_name, f.flight_num, f.departure_airport, f.arrival_airport, 
                f.departure_date, f.departure_time, f.arrival_date, f.arrival_time, f.base_price
                FROM flight f
                WHERE f.departure_airport = %s 
                AND f.arrival_airport = %s 
                AND f.departure_date >= %s
                ORDER BY f.departure_date ASC, f.departure_time ASC
            '''
            cursor.execute(query, (source, destination, departure_date))
            flights = cursor.fetchall()

            if not flights:
                flash('No flights found based on the search criteria.')
        except Exception as e:
            flash(f'Error occurred while searching for flights: {str(e)}')
        finally:
            cursor.close()

        return render_template('flight_results.html', flights=flights)

    return render_template('search_flights.html')

