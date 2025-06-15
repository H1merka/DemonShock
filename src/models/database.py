# database.py
import sqlite3
import os
from src.models.settings import DB_PATH


class SaveManager:
    def __init__(self):
        self.conn = None
        self.cursor = None
        self.init_db()

    def init_db(self):
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        self.conn = sqlite3.connect(DB_PATH)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS save_data (
                id INTEGER PRIMARY KEY,
                level INTEGER,
                wave INTEGER,
                health INTEGER,
                weapon TEXT,
                music_volume REAL
            )
        """)
        self.conn.commit()

    def save_game(self, level, wave, health, weapon_name, music_volume):
        self.cursor.execute("DELETE FROM save_data")
        self.cursor.execute("""
            INSERT INTO save_data (level, wave, health, weapon, music_volume)
            VALUES (?, ?, ?, ?, ?)
        """, (level, wave, health, weapon_name, music_volume))
        self.conn.commit()

    def load_last_game(self):
        self.cursor.execute("SELECT level, wave, health, weapon, music_volume FROM save_data LIMIT 1")
        result = self.cursor.fetchone()
        if result:
            return {
                'level': result[0],
                'wave': result[1],
                'health': result[2],
                'weapon': result[3],
                'music_volume': result[4]
            }
        return None

    def close(self):
        if self.conn:
            self.conn.close()
