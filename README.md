# FlightHub ✈️

**FlightHub** is a full-stack web application that simulates an airline management system. It allows both **customers** and **airline staff** to interact with flight data — from booking and rating flights to creating new routes and managing fleets.

## 🧠 Features

### 👥 For Customers:
- Register and log in
- Search for upcoming flights
- Purchase tickets
- View past and future bookings
- Rate and review completed flights

### 🛫 For Airline Staff:
- Register as an airline staff member
- Create new flights, airplanes, and routes
- Update flight statuses (delayed, departed, arrived)
- View customer feedback and generate sales reports

## 🧰 Tech Stack

- 🐍 **Python** – Backend logic  
- 🌐 **Flask** – Web framework  
- 🛢 **MySQL** – Relational database  
- 🖥️ **HTML/CSS** – UI structure and styling  
- ⚙️ **JavaScript** – Frontend interactivity and validation

## 🔧 Getting Started

```bash
# Clone the repository
git clone https://github.com/yourusername/flighthub.git
cd flighthub

# Set up a virtual environment (optional)
python -m venv venv
source venv/bin/activate   # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up your MySQL database and update config in app.py or config.py

# Run the Flask server
flask run
