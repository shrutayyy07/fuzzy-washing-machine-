import sqlite3
import os

# Create database file paths logically
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(base_dir, 'database', 'washing_history.db')

def init_db():
    """Initializes the SQLite Database. Called on app startup."""
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            dirt_level REAL NOT NULL,
            load_size REAL NOT NULL,
            cycle_time REAL NOT NULL,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def save_history(dirt_level, load_size, cycle_time):
    """Saves a new run to the database."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO history (dirt_level, load_size, cycle_time)
        VALUES (?, ?, ?)
    ''', (dirt_level, load_size, cycle_time))
    conn.commit()
    conn.close()

def get_history():
    """Fetches the past 10 executions."""
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row # This allows us to access columns by name
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM history ORDER BY timestamp DESC LIMIT 10')
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]
