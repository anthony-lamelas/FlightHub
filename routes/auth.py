from flask import Blueprint, render_template, request, redirect, session
import hashlib 
from app import get_db_connection

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":  # checks if form has been submitted
        role = request.form.get("role")

        conn = get_db_connection()
        cursor = conn.cursor()

        if role == "customer" or role == "Customer":
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
                INSERT INTO Customer (
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
        
        elif role == "staff" or role == "Staff":
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
                INSERT INTO Airline_Staff (
                username, password, first_name, last_name, date_of_birth, airline_name)
                VALUES (%s, %s, %s, %s, %s, %s)
                """, (username, password, first_name, last_name, date_of_birth, airline_name))
            
            emails = request.form.getlist("email")  # supports multiple if form uses name="email"
            for email in emails:
                cursor.execute("INSERT INTO Staff_Email (username, email) VALUES (%s, %s)", (username, email))
            
            phones = request.form.getlist("phone_number")
            for phone in phones:
                cursor.execute("INSERT INTO Staff_Phone_Number (username, phone_number) VALUES (%s, %s)", (username, phone))
        
        conn.commit()
        cursor.close()
        conn.close()
        return redirect("/login")
    
    return render_template("register.html")



@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        role = request.form.get("role")
        identifier = request.form.get("identifier")  # email for customer, username for staff
        password = request.form.get("password")
        password = hashlib.md5(password.encode()).hexdigest()

        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

        if role == "customer" or role == "Customer":
            query = "SELECT * FROM Customer WHERE email = %s AND password = %s"
        elif role == "staff" or role == "Staff":
            query = "SELECT * FROM Airline_Staff WHERE username = %s AND password = %s"
        else:
            return render_template("login.html", error="Invalid role selected.")

        cursor.execute(query, (identifier, password))
        user = cursor.fetchone()

        cursor.close()
        conn.close()

        # if login is successful
        if user:
            if role == "customer" or role == "Customer":
                session["user_id"] = user["email"]
                return redirect("/customer_home")
            else:
                session["user_id"] = user["username"]
                return redirect("/airline_staff_home")
        else:
            return render_template("login.html", error="Invalid credentials.")
        
    return render_template("login.html")

