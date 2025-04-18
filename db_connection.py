import mysql.connector

# Database Conncetion
def get_db_connection():
    conn = mysql.connector.connect(
        host='10.18.208.31',
        port=3306,
        user='public',
        password='public',
        database='databases_project'  
    )
    return conn

# try:
#     conn = mysql.connector.connect(
#         host='10.18.208.31',
#         port=3306,
#         user='public',
#         password='public',
#         database='databases_project'
#     )
#     print("✅ Connected successfully!")
#     conn.close()
# except mysql.connector.Error as err:
#     print(f"❌ Connection failed: {err}")