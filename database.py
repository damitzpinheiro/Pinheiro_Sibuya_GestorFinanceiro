# FILE: database.py

import sqlite3
import bcrypt

class Database:
    def __init__(self, db_name='cards.db'):
        self.conn = sqlite3.connect(db_name)
        self.create_card_table()
        self.create_user_table()

    def create_card_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS cards (
                            id INTEGER PRIMARY KEY,
                            name TEXT,
                            number TEXT,
                            credit_limit REAL,
                            balance REAL DEFAULT 0)''')
        self.conn.commit()

    def create_user_table(self):
        cursor = self.conn.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                            id INTEGER PRIMARY KEY,
                            username TEXT UNIQUE,
                            password BLOB)''')  # Alterado para BLOB para armazenar hashes
        self.conn.commit()

    def get_all(self, table_name):
        cursor = self.conn.cursor()
        cursor.execute(f"SELECT * FROM {table_name}")
        return cursor.fetchall()

    def insert(self, table_name, data):
        cursor = self.conn.cursor()
        columns = ', '.join(data.keys())
        placeholders = ', '.join('?' for _ in data)
        values = tuple(data.values())
        cursor.execute(f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})", values)
        self.conn.commit()
        return cursor.lastrowid

    def delete(self, table_name, row_id):
        cursor = self.conn.cursor()
        cursor.execute(f"DELETE FROM {table_name} WHERE id = ?", (row_id,))
        self.conn.commit()

    def add_user(self, username, password):
        hashed_password = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        try:
            self.insert('users', {'username': username, 'password': hashed_password})
            return True
        except sqlite3.IntegrityError:
            return False

    def verify_user(self, username, password):
        cursor = self.conn.cursor()
        cursor.execute("SELECT password FROM users WHERE username = ?", (username,))
        result = cursor.fetchone()
        if result:
            stored_password = result[0]
            return bcrypt.checkpw(password.encode(), stored_password)
        return False