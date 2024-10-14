import sqlite3,csv

def create_table():
    conn = sqlite3.connect('staff.db')
    cursor = conn.cursor()
    TABLES = {
        "staff_details": 
        """CREATE TABLE IF NOT EXISTS staff_details (
                staff_id TEXT PRIMARY KEY,
                staff_name TEXT NOT NULL,
                dept_name TEXT NOT NULL,
                max_hrs INT NOT NULL,
                allocated_hrs INT NOT NULL,
                first_hr INT NOT NULL,
                morning_hrs INT NOT NULL,
                evening_hrs INT NOT NULL
                )
        """,
        "day_1": 
        """
                CREATE TABLE IF NOT EXISTS day_1 (
                staff_id TEXT PRIMARY KEY,
                one INT NOT NULL DEFAULT 0,
                two INT NOT NULL DEFAULT 0,
                three INT NOT NULL DEFAULT 0,
                four INT NOT NULL DEFAULT 0,
                five INT NOT NULL DEFAULT 0,
                six INT NOT NULL DEFAULT 0,
                seven INT NOT NULL DEFAULT 0,
                FOREIGN KEY (staff_id) REFERENCES staff_details (staff_id) ON DELETE CASCADE
                )
        """,
        "day_2": 
        """
                CREATE TABLE IF NOT EXISTS day_2 (
                staff_id TEXT PRIMARY KEY,
                one INT NOT NULL DEFAULT 0,
                two INT NOT NULL DEFAULT 0,
                three INT NOT NULL DEFAULT 0,
                four INT NOT NULL DEFAULT 0,
                five INT NOT NULL DEFAULT 0,
                six INT NOT NULL DEFAULT 0,
                seven INT NOT NULL DEFAULT 0,
                FOREIGN KEY (staff_id) REFERENCES staff_details (staff_id) ON DELETE CASCADE
                )
        """,
        "day_3": 
        """
                CREATE TABLE IF NOT EXISTS day_3 (
                staff_id TEXT PRIMARY KEY,
                one INT NOT NULL DEFAULT 0,
                two INT NOT NULL DEFAULT 0,
                three INT NOT NULL DEFAULT 0,
                four INT NOT NULL DEFAULT 0,
                five INT NOT NULL DEFAULT 0,
                six INT NOT NULL DEFAULT 0,
                seven INT NOT NULL DEFAULT 0,
                FOREIGN KEY (staff_id) REFERENCES staff_details (staff_id) ON DELETE CASCADE
                )
        """,
        "day_4": 
        """
                CREATE TABLE IF NOT EXISTS day_4 (
                staff_id TEXT PRIMARY KEY,
                one INT NOT NULL DEFAULT 0,
                two INT NOT NULL DEFAULT 0,
                three INT NOT NULL DEFAULT 0,
                four INT NOT NULL DEFAULT 0,
                five INT NOT NULL DEFAULT 0,
                six INT NOT NULL DEFAULT 0,
                seven INT NOT NULL DEFAULT 0,
                FOREIGN KEY (staff_id) REFERENCES staff_details (staff_id) ON DELETE CASCADE
                )
        """,
        "day_5": 
        """
                CREATE TABLE IF NOT EXISTS day_5 (
                staff_id TEXT PRIMARY KEY,
                one INT NOT NULL DEFAULT 0,
                two INT NOT NULL DEFAULT 0,
                three INT NOT NULL DEFAULT 0,
                four INT NOT NULL DEFAULT 0,
                five INT NOT NULL DEFAULT 0,
                six INT NOT NULL DEFAULT 0,
                seven INT NOT NULL DEFAULT 0,
                FOREIGN KEY (staff_id) REFERENCES staff_details (staff_id) ON DELETE CASCADE
                )
        """,
    }
    for table_name in TABLES:
        table_description = TABLES[table_name]
        cursor.execute(table_description)
    for day_num in range(1, 6):
        update_trigger = f'''
        CREATE TRIGGER IF NOT EXISTS update_staff_details_day_{day_num}
        AFTER UPDATE ON day_{day_num}
        FOR EACH ROW
        BEGIN
            UPDATE staff_details
            SET allocated_hrs = allocated_hrs -
                (OLD.one + OLD.two + OLD.three + OLD.four + OLD.five + OLD.six + OLD.seven) +
                (NEW.one + NEW.two + NEW.three + NEW.four + NEW.five + NEW.six + NEW.seven)
            WHERE staff_id = NEW.staff_id;
        END
        '''
        cursor.execute(update_trigger)

    conn.commit()
    conn.close()

def populate_table():
    conn = sqlite3.connect('staff.db')
    cursor = conn.cursor()

    filename_staff = "assets/StaffDatabase/CSV/staff.csv"
    day_filenames = [
        "assets/StaffDatabase/CSV/day_1.csv",
        "assets/StaffDatabase/CSV/day_2.csv",
        "assets/StaffDatabase/CSV/day_3.csv",
        "assets/StaffDatabase/CSV/day_4.csv",
        "assets/StaffDatabase/CSV/day_5.csv"
    ]

  
    with open(filename_staff, newline='', encoding='utf-8') as csvfile:
        csvreader = csv.reader(csvfile)
        next(csvreader)  
        staff_data = [(row[0], row[1], row[2], int(row[3]), int(row[4]), int(row[5]), int(row[6]), int(row[7])) for row in csvreader]

    insert_query_staff = """
    INSERT INTO staff_details (staff_id, staff_name, dept_name, max_hrs, allocated_hrs, first_hr, morning_hrs, evening_hrs)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """

    cursor.executemany(insert_query_staff, staff_data)

    for idx, filename_day in enumerate(day_filenames, start=1):
        with open(filename_day, newline='', encoding='utf-8') as csvfile_day:
            csvreader_day = csv.reader(csvfile_day)
            next(csvreader_day)  
            day_data = [(row[0], int(row[1]), int(row[2]), int(row[3]), int(row[4]), int(row[5]), int(row[6]), int(row[7])) for row in csvreader_day]
        insert_query_day = f"""
        INSERT INTO day_{idx} (staff_id, one, two, three, four, five, six, seven)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """

        cursor.executemany(insert_query_day, day_data)
    conn.commit()
    conn.close()



def drop_tables():
    conn = sqlite3.connect('staff.db')
    cursor = conn.cursor()
    tablenames = ["day_1", "day_2", "day_3", "day_4", "day_5", "staff_details"]
    for tablename in tablenames:
        query = f"DROP TABLE IF EXISTS {tablename}"
        cursor.execute(query)

    conn.commit()
    conn.close()   