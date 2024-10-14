def create():
    import sqlite3
    conn = sqlite3.connect('class.db')
    cursor = conn.cursor()
    conn.commit()
    conn.close()
