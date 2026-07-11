import mysql.connector
from mysql.connector import Error
import os
from dotenv import load_dotenv
load_dotenv()


class MySQLDatabase:
    def __init__(self):
        try:
            self.connection = mysql.connector.connect(
                host="localhost",
                user=os.getenv("DATABASE_user"),
                password=os.getenv("DATABASE_PASSWORD"),
                database="library_management"
            )

            self.cursor = self.connection.cursor(dictionary=True)

            print("✅ MySQL Connected Successfully")

        except Error as e:
            print("Database Connection Error:", e)

    # ----------------------------
    # INSERT
    # ----------------------------
    def insert(self, query, values):
        try:
            self.cursor.execute(query, values)
            self.connection.commit()
            return self.cursor.lastrowid

        except Error as e:
            self.connection.rollback()
            print("Insert Error:", e)
            return None

    # ----------------------------
    # SELECT ONE
    # ----------------------------
    def fetch_one(self, query, values=None):
        try:
            self.cursor.execute(query, values or ())
            return self.cursor.fetchone()

        except Error as e:
            print("Fetch One Error:", e)
            return None

    # ----------------------------
    # SELECT ALL
    # ----------------------------
    def fetch_all(self, query, values=None):
        try:
            self.cursor.execute(query, values or ())
            return self.cursor.fetchall()

        except Error as e:
            print("Fetch All Error:", e)
            return []

    # ----------------------------
    # UPDATE
    # ----------------------------
    def update(self, query, values):
        try:
            self.cursor.execute(query, values)
            self.connection.commit()
            return self.cursor.rowcount

        except Error as e:
            self.connection.rollback()
            print("Update Error:", e)
            return 0

    # ----------------------------
    # DELETE
    # ----------------------------
    def delete(self, query, values):
        try:
            self.cursor.execute(query, values)
            self.connection.commit()
            return self.cursor.rowcount

        except Error as e:
            self.connection.rollback()
            print("Delete Error:", e)
            return 0

    # ----------------------------
    # EXECUTE CUSTOM QUERY
    # ----------------------------
    def execute(self, query, values=None):
        try:
            self.cursor.execute(query, values or ())
            self.connection.commit()

        except Error as e:
            self.connection.rollback()
            print("Execute Error:", e)

    # ----------------------------
    # CLOSE CONNECTION
    # ----------------------------
    def close(self):
        if self.connection.is_connected():
            self.cursor.close()
            self.connection.close()
            print("Database Closed")