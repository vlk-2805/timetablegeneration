def create():
    import sqlite3
    conn = sqlite3.connect('room.db')
    cursor = conn.cursor()
    conn.commit()
    conn.close()
