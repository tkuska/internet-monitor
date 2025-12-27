import sqlite3

DB_PATH = "/data/speedtest.db"

def get_conn():
    return sqlite3.connect(DB_PATH, check_same_thread=False)

def init_db():
    conn = get_conn()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS speedtests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
            download REAL,
            upload REAL,
            ping REAL,
	    connection TEXT
        )
    """)
    conn.commit()
    conn.close()
