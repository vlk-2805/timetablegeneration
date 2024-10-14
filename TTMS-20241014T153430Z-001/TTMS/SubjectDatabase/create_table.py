import sqlite3

def create_tables():
    conn = sqlite3.connect('subject.db')
    cursor = conn.cursor()

    TABLES = {
        "subject_details": 
        """CREATE TABLE subject_details (
                subject_id TEXT PRIMARY KEY,
                subject_name TEXT NOT NULL,
                dept_name TEXT NOT NULL,
                credit INT NOT NULL,
                recommended_hrs INT NOT NULL,
                lab INT NOT NULL,
                sem INT NOT NULL
                )
        """
    }

    for table_name, table_description in TABLES.items():
        print(f"Creating table {table_name}: ", end="")
        cursor.execute(table_description)
        print("Done")

    conn.commit()
    conn.close()

create_tables()
