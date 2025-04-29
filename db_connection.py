import mysql.connector

# Database Conncetion
# Anthony
def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',
        port=3306,
        user='public',
        password='public',
        database='databases_project'  
    )
    return conn

# # Cindy
# def get_db_connection():
#     conn = mysql.connector.connect(
#         host='localhost',
#         port=8889,
#         user='root',
#         password='root',
#         database='databases_project'  
#     )
#     return conn


