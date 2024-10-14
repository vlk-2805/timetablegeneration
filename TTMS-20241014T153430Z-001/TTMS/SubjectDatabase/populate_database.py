import csv,sqlite3
conn = sqlite3.connect('subject.db')
cursor = conn.cursor()
class_filename = "assets/SubjectDatabase/CSV/subject.csv"

with open(class_filename, 'r') as csvfile:
    csv_reader = csv.reader(csvfile)
    next(csv_reader) 
    for row in csv_reader:
        cursor.execute('''
            INSERT INTO subject_details (subject_id, subject_name, dept_name, credit, recommended_hrs, lab,sem)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', row)

conn.commit()
conn.close()

