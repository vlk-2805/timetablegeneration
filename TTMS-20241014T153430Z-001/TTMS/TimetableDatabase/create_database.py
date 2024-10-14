def create():
    import sqlite3
    conn = sqlite3.connect('timetable.db')
    cursor = conn.cursor()
    conn.commit()
    conn.close()
