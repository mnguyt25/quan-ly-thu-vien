import pyodbc
from datetime import datetime

class Database:
    def __init__(self):
        self.server = 'localhost'
        self.database = 'library'
        self.username = 'tv'
        self.password = '12345'
        self.driver = '{ODBC Driver 17 for SQL Server}'

        try:
            self.conn = pyodbc.connect(
                f'DRIVER={self.driver};SERVER={self.server};DATABASE={self.database};UID={self.username};PWD={self.password}'
            )
            self.cursor = self.conn.cursor()
            print("✅ Kết nối SQL Server thành công")
        except Exception as e:
            print("❌ Lỗi kết nối SQL Server:", e)

    def fetch_one(self, query, params=()):
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchone()
        except Exception as e:
            print("❌ Lỗi khi truy vấn fetch_one:", e)
            return None

    def fetch_all(self, query, params=()):
        try:
            self.cursor.execute(query, params)
            return self.cursor.fetchall()
        except Exception as e:
            print("❌ Lỗi khi truy vấn fetch_all:", e)
            return []

    def execute_query(self, query, params=()):
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
        except Exception as e:
            print("❌ Lỗi khi thực thi truy vấn:", e)

    def close(self):
        try:
            self.cursor.close()
            self.conn.close()
        except Exception as e:
            print("❌ Lỗi khi đóng kết nối:", e)
