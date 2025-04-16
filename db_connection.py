import mysql.connector

# Database Conncetion
def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',
        port=3306,
        user='databases_project',
        password='project1',
        database='databases_project'  
    )
    return conn