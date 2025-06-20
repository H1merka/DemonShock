import sqlite3
import os
from src.models.settings import DB_PATH
from typing import Optional, Dict, Any


class SaveManager:
    """Manages saving and loading game data using SQLite."""

    def __init__(self) -> None:
        """Initialize the database and ensure the save_data table exists."""
        self._init_db()

    def _init_db(self) -> None:
        """Create database directory and table if they don't exist."""
        os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS save_data (
                    id INTEGER PRIMARY KEY,
                    level INTEGER,
                    health INTEGER,
                    weapon TEXT,
                    music_volume REAL
                )
            """)
            conn.commit()

    def save_game(self, level: int, health: int, weapon_name: str, music_volume: float) -> None:
        """
        Save the current game state to the database.
        Clears previous save data before inserting new.

        Args:
            level (int): Current game level.
            health (int): Player's health points.
            weapon_name (str): Name of the equipped weapon.
            music_volume (float): Music volume setting.
        """
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM save_data")
            cursor.execute("""
                INSERT INTO save_data (level, health, weapon, music_volume)
                VALUES (?, ?, ?, ?)
            """, (level, health, weapon_name, music_volume))
            conn.commit()

    def load_last_game(self) -> Optional[Dict[str, Any]]:
        """
        Load the last saved game state from the database.

        Returns:
            Optional[Dict[str, Any]]: A dictionary with keys 'level', 'health',
            'weapon', 'music_volume' if save exists, otherwise None.
        """
        with sqlite3.connect(DB_PATH) as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT level, health, weapon, music_volume FROM save_data LIMIT 1")
            result = cursor.fetchone()
            if result:
                return {
                    'level': result[0],
                    'health': result[1],
                    'weapon': result[2],
                    'music_volume': result[3]
                }
        return None
