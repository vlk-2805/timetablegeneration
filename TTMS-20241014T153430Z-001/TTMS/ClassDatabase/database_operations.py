
import csv
import sqlite3
def create_table():
    
    conn = sqlite3.connect('class.db')
    cursor = conn.cursor()
    TABLES = {
        "class_details": 
        """CREATE TABLE IF NOT EXISTS class_details (
                class_id TEXT PRIMARY KEY,
                class_name TEXT NOT NULL,
                dept_name TEXT NOT NULL,
                max_hrs INTEGER NOT NULL,
                allocated_hrs INTEGER NOT NULL
                )
        """,
        "day_1": 
        """
                CREATE TABLE IF NOT EXISTS day_1 (
                class_id TEXT PRIMARY KEY,
                one INTEGER NOT NULL DEFAULT 0,
                two INTEGER NOT NULL DEFAULT 0,
                three INTEGER NOT NULL DEFAULT 0,
                four INTEGER NOT NULL DEFAULT 0,
                five INTEGER NOT NULL DEFAULT 0,
                six INTEGER NOT NULL DEFAULT 0,
                seven INTEGER NOT NULL DEFAULT 0,
                lab INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (class_id) REFERENCES class_details (class_id) ON DELETE CASCADE
                )
        """,
        "day_2": 
        """
                CREATE TABLE IF NOT EXISTS day_2 (
                class_id TEXT PRIMARY KEY,
                one INTEGER NOT NULL DEFAULT 0,
                two INTEGER NOT NULL DEFAULT 0,
                three INTEGER NOT NULL DEFAULT 0,
                four INTEGER NOT NULL DEFAULT 0,
                five INTEGER NOT NULL DEFAULT 0,
                six INTEGER NOT NULL DEFAULT 0,
                seven INTEGER NOT NULL DEFAULT 0,
                lab INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (class_id) REFERENCES class_details (class_id) ON DELETE CASCADE
                )
        """,
        "day_3": 
        """
                CREATE TABLE IF NOT EXISTS day_3 (
                class_id TEXT PRIMARY KEY,
                one INTEGER NOT NULL DEFAULT 0,
                two INTEGER NOT NULL DEFAULT 0,
                three INTEGER NOT NULL DEFAULT 0,
                four INTEGER NOT NULL DEFAULT 0,
                five INTEGER NOT NULL DEFAULT 0,
                six INTEGER NOT NULL DEFAULT 0,
                seven INTEGER NOT NULL DEFAULT 0,
                lab INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (class_id) REFERENCES class_details (class_id) ON DELETE CASCADE
                )
        """,
        "day_4": 
        """
                CREATE TABLE IF NOT EXISTS day_4 (
                class_id TEXT PRIMARY KEY,
                one INTEGER NOT NULL DEFAULT 0,
                two INTEGER NOT NULL DEFAULT 0,
                three INTEGER NOT NULL DEFAULT 0,
                four INTEGER NOT NULL DEFAULT 0,
                five INTEGER NOT NULL DEFAULT 0,
                six INTEGER NOT NULL DEFAULT 0,
                seven INTEGER NOT NULL DEFAULT 0,
                lab INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (class_id) REFERENCES class_details (class_id) ON DELETE CASCADE
                )
        """,
        "day_5": 
        """
                CREATE TABLE IF NOT EXISTS day_5 (
                class_id TEXT PRIMARY KEY,
                one INTEGER NOT NULL DEFAULT 0,
                two INTEGER NOT NULL DEFAULT 0,
                three INTEGER NOT NULL DEFAULT 0,
                four INTEGER NOT NULL DEFAULT 0,
                five INTEGER NOT NULL DEFAULT 0,
                six INTEGER NOT NULL DEFAULT 0,
                seven INTEGER NOT NULL DEFAULT 0,
                lab INTEGER NOT NULL DEFAULT 0,
                FOREIGN KEY (class_id) REFERENCES class_details (class_id) ON DELETE CASCADE
                )
        """,
    }

    for table_name, table_description in TABLES.items():
        cursor.execute(table_description)

    triggers = [
        """
        CREATE TRIGGER IF NOT EXISTS update_class_details_day_1
        AFTER UPDATE ON day_1
        FOR EACH ROW
        BEGIN
            UPDATE class_details
            SET allocated_hrs = allocated_hrs - (OLD.one + OLD.two + OLD.three + OLD.four + OLD.five + OLD.six + OLD.seven) + 
                                 (NEW.one + NEW.two + NEW.three + NEW.four + NEW.five + NEW.six + NEW.seven)
            WHERE class_id = NEW.class_id;
        END
        """,
        """
        CREATE TRIGGER IF NOT EXISTS update_class_details_day_2
        AFTER UPDATE ON day_2
        FOR EACH ROW
        BEGIN
            UPDATE class_details
            SET allocated_hrs = allocated_hrs - (OLD.one + OLD.two + OLD.three + OLD.four + OLD.five + OLD.six + OLD.seven) + 
                                 (NEW.one + NEW.two + NEW.three + NEW.four + NEW.five + NEW.six + NEW.seven)
            WHERE class_id = NEW.class_id;
        END
        """,
        """
        CREATE TRIGGER IF NOT EXISTS update_class_details_day_3
        AFTER UPDATE ON day_3
        FOR EACH ROW
        BEGIN
            UPDATE class_details
            SET allocated_hrs = allocated_hrs - (OLD.one + OLD.two + OLD.three + OLD.four + OLD.five + OLD.six + OLD.seven) + 
                                 (NEW.one + NEW.two + NEW.three + NEW.four + NEW.five + NEW.six + NEW.seven)
            WHERE class_id = NEW.class_id;
        END
        """,
        """
        CREATE TRIGGER IF NOT EXISTS update_class_details_day_4
        AFTER UPDATE ON day_4
        FOR EACH ROW
        BEGIN
            UPDATE class_details
            SET allocated_hrs = allocated_hrs - (OLD.one + OLD.two + OLD.three + OLD.four + OLD.five + OLD.six + OLD.seven) + 
                                 (NEW.one + NEW.two + NEW.three + NEW.four + NEW.five + NEW.six + NEW.seven)
            WHERE class_id = NEW.class_id;
        END
        """,
        """
        CREATE TRIGGER IF NOT EXISTS update_class_details_day_5
        AFTER UPDATE ON day_5
        FOR EACH ROW
        BEGIN
            UPDATE class_details
            SET allocated_hrs = allocated_hrs - (OLD.one + OLD.two + OLD.three + OLD.four + OLD.five + OLD.six + OLD.seven) + 
                                 (NEW.one + NEW.two + NEW.three + NEW.four + NEW.five + NEW.six + NEW.seven)
            WHERE class_id = NEW.class_id;
        END
        """
    ]

    for trigger in triggers:
        cursor.execute(trigger)
    conn.commit()
    conn.close()

def populate_database():
    conn = sqlite3.connect('class.db')
    cursor = conn.cursor()
    class_filename = "assets/ClassDatabase/CSV/class.csv"
    day_filenames = [
        "assets/ClassDatabase/CSV/day_1.csv",
        "assets/ClassDatabase/CSV/day_2.csv",
        "assets/ClassDatabase/CSV/day_3.csv",
        "assets/ClassDatabase/CSV/day_4.csv",
        "assets/ClassDatabase/CSV/day_5.csv"
    ]
    def load_csv_to_table(csv_file, table_name, columns):
        with open(csv_file, 'r') as file:
            reader = csv.reader(file)
            next(reader)  
            for row in reader:
                placeholders = ', '.join(['?'] * len(row))
                query = f'INSERT INTO {table_name} ({columns}) VALUES ({placeholders})'
                cursor.execute(query, row)

    load_csv_to_table(class_filename, 'class_details', 'class_id, class_name, dept_name, max_hrs, allocated_hrs')
    for idx, day_filename in enumerate(day_filenames, start=1):
        load_csv_to_table(day_filename, f'day_{idx}', 'class_id, one, two, three, four, five, six, seven, lab')

    conn.commit()
    conn.close()
    
def drop_tables():
    conn = sqlite3.connect('class.db')
    cursor = conn.cursor()
    tablenames = ["day_1", "day_2", "day_3", "day_4", "day_5", "class_details"]
    for tablename in tablenames:
        query = f"DROP TABLE IF EXISTS {tablename}"
        cursor.execute(query)

    conn.commit()
    conn.close()
