from flask import Blueprint, render_template, request, redirect, session
import hashlib 
import mysql.connector
from db_connection import *
from mysql.connector.errors import IntegrityError



auth_bp = Blueprint("auth", __name__)

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
                # hashlib.md5() creates a hash
                # encode() converts it to bytes
                # hexdigest() turns it into a readable string
                password = hashlib.md5(request.form.get("password").encode()).hexdigest()

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
                # hashlib.md5() creates a hash
                # encode() converts it to bytes
                # hexdigest() turns it into a readable string
                password = hashlib.md5(request.form.get("password").encode()).hexdigest()

                cursor.execute("""
                    INSERT INTO airline_staff (
                    username, password, first_name, last_name, date_of_birth, airline_name)
                    VALUES (%s, %s, %s, %s, %s, %s)
                    """, (username, password, first_name, last_name, date_of_birth, airline_name))
                
                emails = [e for e in request.form.getlist("email") if e.strip()]  # supports multiple if form uses name="email"
                phones = [p for p in request.form.getlist("phone_number") if p.strip()]  # supports multiple if form uses name="phone_number"

                for email in emails:
                    cursor.execute("INSERT INTO staff_email (username, email) VALUES (%s, %s)", (username, email))

                for phone in phones:
                    cursor.execute("INSERT INTO staff_phone (username, phone_number) VALUES (%s, %s)", (username, phone))
                
                if not emails:
                    return render_template(
                        "register.html",
                        error="At least one email is required for staff.",
                        selected_role=role)

                if not phones:
                    return render_template(
                        "register.html",
                        error="At least one phone number is required for staff.",
                        selected_role=role)

            else:
                return "Invalid role", 400
            
            conn.commit()
            cursor.close()
            conn.close()
            return redirect("/login")
        return render_template("register.html")
        
    # If error
    except IntegrityError as e:
        # undo the query
        conn.rollback()

        if "Duplicate entry" in str(e):
                return render_template("register.html", 
                                       error="User already exists. Please try again.", 
                                       selected_role = role)
        
    return render_template("register.html", 
                           error="Registration failed. Please check your input.", 
                           selected_role = role)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        role = request.form.get("role", "").lower()

        # Pull the correct identifier + password field
        if role == "customer":
            identifier = request.form.get("customer_identifier")
            password   = request.form.get("customer_password")
            query = "SELECT * FROM customers WHERE email = %s AND password = %s"
        elif role == "staff":
            identifier = request.form.get("staff_identifier")
            password   = request.form.get("staff_password")
            query = "SELECT * FROM airline_staff WHERE username = %s AND password = %s"
        else:
            return render_template("login.html",
                                   error="Invalid role selected.",
                                   selected_role=role)

        # Hash password
        if password is None or identifier is None:
            return render_template("login.html",
                                   error="Missing credentials.",
                                   selected_role=role)

        hashed_pw = hashlib.md5(password.encode()).hexdigest()

        print("Trying login with:", identifier, hashed_pw)

        # Run query
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)
        cursor.execute(query, (identifier, hashed_pw))
        user = cursor.fetchone()
        cursor.close()
        conn.close()

        # Handle success/failure
        if user:
            session["user_id"] = user["email"] if role == "customer" else user["username"]
            return redirect("/customer_home" if role == "customer" else "/staff/home")
        else:
            return render_template("login.html",
                                   error="Invalid credentials.",
                                   selected_role=role)

    # GET request
    return render_template("login.html", selected_role="customer")
