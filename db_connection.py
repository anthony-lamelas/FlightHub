import mysql.connector

# Database Conncetion
# Anthony
# def get_db_connection():
#     conn = mysql.connector.connect(
#         host='localhost',
#         port=3306,
#         user='public',
#         password='public',
#         database='databases_project'  
#     )
#     return conn

# Cindy
def get_db_connection():
    conn = mysql.connector.connect(
        host='localhost',
        port=8889,
        user='root',
        password='root',
        database='databases_project'  
    )
    return conn


# try:
#     conn = get_db_connection()
#     print("✅ Connected to MySQL successfully!")
#     conn.close()
# except mysql.connector.Error as err:
#     print(f"❌ Connection failed: {err}")
