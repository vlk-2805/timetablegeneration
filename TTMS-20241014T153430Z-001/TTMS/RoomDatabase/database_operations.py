import sqlite3,csv
def create_table():
    conn = sqlite3.connect('room.db')
    cursor = conn.cursor()
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS room_details (
        room_id TEXT PRIMARY KEY,
        room_name TEXT NOT NULL,
        dept_name TEXT NOT NULL,
        max_hrs INTEGER NOT NULL,
        allocated_hrs INTEGER NOT NULL,
        lab INTEGER NOT NULL
    )
    ''')
    for day_num in range(1, 6):
        cursor.execute(f'''
        CREATE TABLE IF NOT EXISTS day_{day_num} (
            room_id TEXT PRIMARY KEY,
            one INTEGER NOT NULL DEFAULT 0,
            two INTEGER NOT NULL DEFAULT 0,
            three INTEGER NOT NULL DEFAULT 0,
            four INTEGER NOT NULL DEFAULT 0,
            five INTEGER NOT NULL DEFAULT 0,
            six INTEGER NOT NULL DEFAULT 0,
            seven INTEGER NOT NULL DEFAULT 0,
            FOREIGN KEY (room_id) REFERENCES room_details (room_id) ON DELETE CASCADE
        )
        ''')

    for day_num in range(1, 6):
        update_trigger = f'''
        CREATE TRIGGER IF NOT EXISTS update_room_details_day_{day_num}
        AFTER UPDATE ON day_{day_num}
        FOR EACH ROW
        BEGIN
            UPDATE room_details
            SET allocated_hrs = allocated_hrs -
                (OLD.one + OLD.two + OLD.three + OLD.four + OLD.five + OLD.six + OLD.seven) +
                (NEW.one + NEW.two + NEW.three + NEW.four + NEW.five + NEW.six + NEW.seven)
            WHERE room_id = NEW.room_id;
        END
        '''
        cursor.execute(update_trigger)

    conn.commit()
    conn.close()


def populate_table():
    conn = sqlite3.connect('room.db')
    cursor = conn.cursor()

    room_filename = "assets/RoomDatabase/CSV/room.csv"
    day_filenames = [
        "assets/RoomDatabase/CSV/day_1.csv",
        "assets/RoomDatabase/CSV/day_2.csv",
        "assets/RoomDatabase/CSV/day_3.csv",
        "assets/RoomDatabase/CSV/day_4.csv",
        "assets/RoomDatabase/CSV/day_5.csv"
    ]
    with open(room_filename, newline='') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader) 
        for row in csv_reader:
            cursor.execute('''
            INSERT INTO room_details (room_id, room_name, dept_name, max_hrs, allocated_hrs, lab)
            VALUES (?, ?, ?, ?, ?, ?)
            ''', row)

    for idx, day_filename in enumerate(day_filenames, start=1):
        with open(day_filename, newline='') as csvfile:
            csv_reader = csv.reader(csvfile)
            next(csv_reader)  
            for row in csv_reader:
                cursor.execute(f'''
                INSERT INTO day_{idx} (room_id, one, two, three, four, five, six, seven)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ''', row)

    conn.commit()
    conn.close()

def drop_tables():
    conn = sqlite3.connect('room.db')
    cursor = conn.cursor()

    tablenames = ["day_1", "day_2", "day_3", "day_4", "day_5", "room_details"]
    for table_name in tablenames:
        cursor.execute(f"DROP TABLE IF EXISTS {table_name}")
    conn.commit()
    conn.close()


