import mysql.connector

# Database Conncetion
def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',
        port=3306,
        user='public',
        password='public',
        database='databases_project'  
    )
    return conn