import sqlite3,num2words,csv

def create_table():
    # Connect to the SQLite database
    conn = sqlite3.connect('timetable.db')
    cursor = conn.cursor()

    TABLES = {
        "day_1": 
        """
                CREATE TABLE IF NOT EXISTS day_1 (
                id VARCHAR(255) PRIMARY KEY,
                passwd VARCHAR(255) DEFAULT "ssn",
                one VARCHAR(255) NOT NULL DEFAULT 0,
                two VARCHAR(255) NOT NULL DEFAULT 0,
                three VARCHAR(255) NOT NULL DEFAULT 0,
                four VARCHAR(255) NOT NULL DEFAULT 0,
                five VARCHAR(255) NOT NULL DEFAULT 0,
                six VARCHAR(255) NOT NULL DEFAULT 0,
                seven VARCHAR(255) NOT NULL DEFAULT 0,
                role VARCHAR(255) NOT NULL DEFAULT 0
                )
        """,
        "day_2": 
        """
                CREATE TABLE IF NOT EXISTS day_2 (
                id VARCHAR(255) PRIMARY KEY,
                passwd VARCHAR(255) DEFAULT "ssn",
                one VARCHAR(255) NOT NULL DEFAULT 0,
                two VARCHAR(255) NOT NULL DEFAULT 0,
                three VARCHAR(255) NOT NULL DEFAULT 0,
                four VARCHAR(255) NOT NULL DEFAULT 0,
                five VARCHAR(255) NOT NULL DEFAULT 0,
                six VARCHAR(255) NOT NULL DEFAULT 0,
                seven VARCHAR(255) NOT NULL DEFAULT 0,
                role VARCHAR(255) NOT NULL DEFAULT 0
                )
        """,
        "day_3": 
        """
                CREATE TABLE IF NOT EXISTS day_3 (
                id VARCHAR(255) PRIMARY KEY,
                passwd VARCHAR(255) DEFAULT "ssn",
                one VARCHAR(255) NOT NULL DEFAULT 0,
                two VARCHAR(255) NOT NULL DEFAULT 0,
                three VARCHAR(255) NOT NULL DEFAULT 0,
                four VARCHAR(255) NOT NULL DEFAULT 0,
                five VARCHAR(255) NOT NULL DEFAULT 0,
                six VARCHAR(255) NOT NULL DEFAULT 0,
                seven VARCHAR(255) NOT NULL DEFAULT 0,
                role VARCHAR(255) NOT NULL DEFAULT 0
                )
        """,
        "day_4": 
        """
                CREATE TABLE IF NOT EXISTS day_4 (
                id VARCHAR(255) PRIMARY KEY,
                passwd VARCHAR(255) DEFAULT "ssn",
                one VARCHAR(255) NOT NULL DEFAULT 0,
                two VARCHAR(255) NOT NULL DEFAULT 0,
                three VARCHAR(255) NOT NULL DEFAULT 0,
                four VARCHAR(255) NOT NULL DEFAULT 0,
                five VARCHAR(255) NOT NULL DEFAULT 0,
                six VARCHAR(255) NOT NULL DEFAULT 0,
                seven VARCHAR(255) NOT NULL DEFAULT 0,
                role VARCHAR(255) NOT NULL DEFAULT 0
                )
        """,
        "day_5": 
        """
                CREATE TABLE IF NOT EXISTS day_5 (
                id VARCHAR(255) PRIMARY KEY,
                passwd VARCHAR(255) DEFAULT "ssn",
                one VARCHAR(255) NOT NULL DEFAULT 0,
                two VARCHAR(255) NOT NULL DEFAULT 0,
                three VARCHAR(255) NOT NULL DEFAULT 0,
                four VARCHAR(255) NOT NULL DEFAULT 0,
                five VARCHAR(255) NOT NULL DEFAULT 0,
                six VARCHAR(255) NOT NULL DEFAULT 0,
                seven VARCHAR(255) NOT NULL DEFAULT 0,
                role VARCHAR(255) NOT NULL DEFAULT 0
                )
        """,
    }

    for table_name in TABLES:
        table_description = TABLES[table_name]
        cursor.execute(table_description)
    conn.commit()
    conn.close()

def populate_table():
    conn = sqlite3.connect('timetable.db')
    cursor = conn.cursor()
    day_filenames = [
        "assets/TimetableDatabase/CSV/day_1.csv",
        "assets/TimetableDatabase/CSV/day_2.csv",
        "assets/TimetableDatabase/CSV/day_3.csv",
        "assets/TimetableDatabase/CSV/day_4.csv",
        "assets/TimetableDatabase/CSV/day_5.csv"
    ]

    for idx, day_filename in enumerate(day_filenames, start=1):
        
        with open(day_filename, 'r', newline='') as csvfile:
            csv_reader = csv.reader(csvfile)
            next(csv_reader)  
            for row in csv_reader:
                cursor.execute(f"INSERT INTO day_{idx} (id, passwd, one, two, three, four, five, six, seven, role) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", row)
    conn.commit()
    conn.close()

    

def delete_table():
    conn = sqlite3.connect('timetable.db')
    cursor = conn.cursor()
    tablenames = ["day_1", "day_2", "day_3", "day_4", "day_5"]

    for tablename in tablenames:
        drop_query = f"DROP TABLE IF EXISTS {tablename}"
        cursor.execute(drop_query)
        print("^") 
    conn.commit()
    conn.close()
        
