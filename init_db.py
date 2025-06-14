import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="taolao",
    database="library"
)

cursor = conn.cursor()
cursor.execute("SHOW TABLES;")  # ví dụ kiểm tra kết nối
for x in cursor:
    print(x)

conn.close()
