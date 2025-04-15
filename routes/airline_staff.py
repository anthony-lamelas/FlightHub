from flask import Blueprint, render_template, session, redirect

staff_bp = Blueprint('staff_bp', __name__)

@staff_bp.route("/airline_staff_home")
def airline_staff_home():
    if "user_id" not in session:
        return redirect("/login")
    return render_template("airline_staff_home.html")