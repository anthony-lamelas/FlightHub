from flask import Blueprint, render_template, session, redirect

customer_bp = Blueprint('customer_bp', __name__)

@customer_bp.route("/customer_home")
def customer_home():
    if "user_id" not in session:
        return redirect("/login")
    return render_template("customer_home.html")

