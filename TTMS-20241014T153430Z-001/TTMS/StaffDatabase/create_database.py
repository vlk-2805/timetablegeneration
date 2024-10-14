def create():
    import sqlite3
    conn = sqlite3.connect('staff.db')
    cursor = conn.cursor()
    conn.commit()
    conn.close()

