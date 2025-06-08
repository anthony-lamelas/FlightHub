from flask import Blueprint, render_template, request, redirect, session
import hashlib 
import psycopg2
from db_connection import *
from psycopg2 import IntegrityError


auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/login/customer", methods=["GET"])
def customer_login():
    return render_template("customer_login.html")

@auth_bp.route("/login/staff", methods=["GET"])
def staff_login():
    return render_template("staff_login.html")

@auth_bp.route('/logout')
def logout():
    user_type = session.get("user_type")
    session.clear()

    if user_type == "staff":
        return redirect('/login/staff')  
    else:
        return redirect('login/customer')

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    try:        
        if request.method == "POST":  # checks if form has been submitted
            role = request.form.get("role")

            conn = get_db_connection()
            cursor = conn.cursor()

            if role == "customer":
                first_name = request.form.get("first_name")
                last_name = request.form.get("last_name")
                building_number = request.form.get("building_number")
                street = request.form.get("street")
                city = request.form.get("city")
                state = request.form.get("state")
                phone_number = request.form.get("phone_number")
                passport_number = request.form.get("passport_number")
                passport_country = request.form.get("passport_country")
                passport_expiration = request.form.get("passport_expiration")
                date_of_birth = request.form.get("date_of_birth")
                email = request.form.get("email")
                password_raw = request.form.get("password")
                if not password_raw:
                    return render_template("register.html", error="Password is required.", selected_role=role)
                password = hashlib.md5(password_raw.encode()).hexdigest()

                cursor.execute("""
                    INSERT INTO customers (
                        email, password, first_name, last_name,
                        building_number, street, city, state,
                        phone_number, passport_number, passport_country,
                        passport_expiration, date_of_birth
                    )
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (
                    email, password, first_name, last_name,
                    building_number, street, city, state,
                    phone_number, passport_number, passport_country,
                    passport_expiration, date_of_birth
                ))
            
            elif role == "staff":
                username = request.form.get("username")
                airline_name = request.form.get("airline_name")
                first_name = request.form.get("first_name")
                last_name = request.form.get("last_name")
                date_of_birth = request.form.get("date_of_birth")
                password_raw = request.form.get("password")
                
                # Validate required fields
                if not all([username, airline_name, first_name, last_name, date_of_birth, password_raw]):
                    return render_template("register.html", error="All fields are required for staff registration.", selected_role=role)
                
                # password_raw is guaranteed to be non-None after the validation above
                password = hashlib.md5(password_raw.encode()).hexdigest()

                # Check if airline exists
                cursor.execute("SELECT airline_name FROM airline WHERE airline_name = %s", (airline_name,))
                if not cursor.fetchone():
                    return render_template("register.html", error=f"Airline '{airline_name}' does not exist. Please contact your administrator.", selected_role=role)

                cursor.execute("""
                    INSERT INTO airline_staff (
                    username, password, first_name, last_name, date_of_birth, airline_name)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """, (username, password, first_name, last_name, date_of_birth, airline_name))
                
                emails = [e for e in request.form.getlist("email") if e.strip()]
                phones = [p for p in request.form.getlist("phone_number") if p.strip()]

                if not emails:
                    return render_template("register.html", error="At least one email is required for staff.", selected_role=role)
                if not phones:
                    return render_template("register.html", error="At least one phone number is required for staff.", selected_role=role)

                for email in emails:
                    cursor.execute("INSERT INTO staff_email (username, email) VALUES (%s, %s)", (username, email))

                for phone in phones:
                    cursor.execute("INSERT INTO staff_phone (username, phone_number) VALUES (%s, %s)", (username, phone))

            else:
                return "Invalid role", 400
            
            conn.commit()
            cursor.close()
            conn.close()
            return redirect("/")
        return render_template("register.html")
        
    except IntegrityError as e:
        conn.rollback()
        error_msg = str(e).lower()
        if "duplicate" in error_msg or "unique" in error_msg:
            if role == "staff":
                return render_template("register.html", error="Username already exists. Please choose a different username.", selected_role=role)
            else:
                return render_template("register.html", error="Email already exists. Please use a different email.", selected_role=role)
        elif "foreign key" in error_msg:
            return render_template("register.html", error="Invalid airline name. Please contact your administrator.", selected_role=role)
        else:
            return render_template("register.html", error=f"Database error: {str(e)}", selected_role=role)
    except Exception as e:
        conn.rollback()
        print(f"Registration error: {e}")  # Log the error for debugging
        return render_template("register.html", error="Registration failed. Please check your input and try again.", selected_role=role)
@auth_bp.route("/login", methods=["POST"])
def login():
    role = request.form.get("role", "").lower()

    if role not in ["customer", "staff"]:
        return render_template("home.html", error="Invalid role selected.")

    # Get identifier and password based on role
    if role == "customer":
        identifier = request.form.get("customer_identifier")
        password = request.form.get("customer_password")
        template = "customer_login.html"
        query = "SELECT * FROM customers WHERE email = %s AND password = %s"
    else:  # staff
        identifier = request.form.get("staff_identifier")
        password = request.form.get("staff_password")
        template = "staff_login.html"
        query = "SELECT * FROM airline_staff WHERE username = %s AND password = %s"

    # Check for missing fields
    if not identifier or not password:
        return render_template(template, error="Missing credentials.", selected_role=role)

    hashed_pw = hashlib.md5(password.encode()).hexdigest()

    try:
        conn = get_db_connection()
        cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(query, (identifier, hashed_pw))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        if user:
            session["user_id"] = user["email"] if role == "customer" else user["username"]
            session["user_type"] = role
            if role == "customer":
                session["user_email"] = user["email"]
                return redirect("/customer_home")
            else:
                return redirect("/staff/home")
        else:
            return render_template(template, error="Invalid credentials. Please try again.", selected_role=role)

    except psycopg2.Error as e:
        print(f"Database error: {e}")
        return render_template(template, error="An error occurred. Try again later.", selected_role=role)
