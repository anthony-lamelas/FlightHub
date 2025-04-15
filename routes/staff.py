from flask import Blueprint, render_template, request
import mysql.connector

# Database Conncetion
def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',
        port=8889,
        user='root',
        password='root',
        database='air_ticket_db'  # use your actual DB name
    )
    return conn

@staff_bp.route('/')
def future_flights():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = '''
        SELECT * FROM flights
        WHERE xxxxx
        ORDER BY TIME ASC
    '''

    

