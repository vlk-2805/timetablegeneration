import num2words,csv,sqlite3
from OneForAll import queries as ofa

def is_free_hour(faculty_id, day, hour):
    """
    Check if a staff member is free at a specific hour on a specific day.

    :param faculty_id: The staff member's ID
    :param day: The day of the week (1-5)
    :param hour: The hour of the day (1-7)
    :return: True if the staff member is free, False otherwise
    """
    hour_name = num2words.num2words(hour)
    table_name = f"day_{day}"
    conn = sqlite3.connect('staff.db')
    cursor = conn.cursor()

    query1 = f"""
    SELECT 
        staff_id,
        CASE 
        WHEN {hour_name} = 0 THEN TRUE
        ELSE FALSE
        END AS is_free
    FROM 
        {table_name}
    WHERE 
        staff_id = ?
    """
    query2 = """
    SELECT 
        staff_id,
        CASE 
        WHEN allocated_hrs < max_hrs THEN TRUE
        ELSE FALSE
        END AS is_free
    FROM 
        staff_details
    WHERE 
        staff_id = ?
    """

    cursor.execute(query1, (faculty_id,))
    result1 = cursor.fetchone()  #
    cursor.execute(query2, (faculty_id,))
    result2 = cursor.fetchone()  
    cursor.close()
    conn.close()

    if result1 and result2:
        return result1[1] and result2[1]
    else:
        return False 


def is_free_in_morning(faculty_id, day):
    """
    Check if a staff member is free during a specific session on a specific day.

    :param faculty_id: The staff member's ID
    :param day: The day of the week (1-5)
    :return: True if the staff member is free, False otherwise
    """
    conn = sqlite3.connect('staff.db')
    cursor = conn.cursor()

    table_name = f"day_{day}"
    query1 = f"""
    SELECT 
        staff_id,
        CASE 
        WHEN two = 0 AND three = 0 AND four = 0 THEN 1
        ELSE 0
        END AS is_free
    FROM 
        {table_name}
    WHERE 
        staff_id = ?
    """
    cursor.execute(query1, (faculty_id,))
    result1 = cursor.fetchone()

    query2 = f"""
    SELECT 
        staff_id,
        CASE 
        WHEN allocated_hrs < max_hrs THEN 1
        ELSE 0
        END AS is_free
    FROM 
        staff_details
    WHERE 
        staff_id = ?
    """
    cursor.execute(query2, (faculty_id,))
    result2 = cursor.fetchone()
    conn.close()

    if result1 and result2:
        return bool(result1[1]) and bool(result2[1])
    else:
        return False

    

def is_free_in_evening(faculty_id, day):
    """
    Check if a staff member is free during a specific session on a specific day.

    :param faculty_id: The staff member's ID
    :param day: The day of the week (1-5)
    :return: True if the staff member is free, False otherwise
    """
    conn = sqlite3.connect('staff.db')
    cursor = conn.cursor()

    table_name = f"day_{day}"
    query1 = f"""
    SELECT 
        staff_id,
        CASE 
        WHEN five = 0 AND six = 0 AND seven = 0 THEN 1
        ELSE 0
        END AS is_free
    FROM 
        {table_name}
    WHERE 
        staff_id = ?
    """
    cursor.execute(query1, (faculty_id,))
    result1 = cursor.fetchone()

    query2 = f"""
    SELECT 
        staff_id,
        CASE 
        WHEN allocated_hrs < max_hrs THEN 1
        ELSE 0
        END AS is_free
    FROM 
        staff_details
    WHERE 
        staff_id = ?
    """
    cursor.execute(query2, (faculty_id,))
    result2 = cursor.fetchone()

    conn.close()

    if result1 and result2:
        return bool(result1[1]) and bool(result2[1])
    else:
        return False

def allocate_hour_morning(staff_id, day):
    """
    Allocate class to a staff on a specific day.

    :param staff_id: The staff member's ID
    :param day: The day of the week (1-5)
    """
    conn = sqlite3.connect('staff.db')
    cursor = conn.cursor()

    table_name = f"day_{day}"
    query = f"""
    UPDATE {table_name}
    SET two = 1, three = 1, four = 1
    WHERE staff_id = ?
    """
    cursor.execute(query, (staff_id,))
    conn.commit()
    conn.close()

def allocate_hour_evening(staff_id, day):
    """
    Allocate class to a staff on a specific day.

    :param staff_id: The staff member's ID
    :param day: The day of the week (1-5)
    """
    conn = sqlite3.connect('staff.db')
    cursor = conn.cursor()

    table_name = f"day_{day}"
    query = f"""
    UPDATE {table_name}
    SET five = 1, six = 1, seven = 1
    WHERE staff_id = ?
    """
    cursor.execute(query, (staff_id,))
    conn.commit()
    conn.close()


def allocate_hour(staff_id, day, hour):
    """
    Allocate class to a staff on a specific day.

    :param staff_id: The staff member's ID
    :param day: The day of the week (1-5)
    :param hour: Hour of class
    """
    conn = sqlite3.connect('staff.db')
    cursor = conn.cursor()

    table_name = f"day_{day}"
    hour_name = num2words.num2words(hour)
    
    if hour == 1:
        cursor.execute("""
        UPDATE staff_details
        SET first_hr = first_hr + 1
        WHERE staff_id = ?
        """, (staff_id,))
    
    query = f"""
    UPDATE {table_name}
    SET {hour_name} = 1
    WHERE staff_id = ?
    """
    cursor.execute(query, (staff_id,))
    
    conn.commit()
    conn.close()

def most_free(dept_name, no_of):
    conn = sqlite3.connect('staff.db')
    cursor = conn.cursor()

    query = f"""
    SELECT staff_id
    FROM staff_details
    WHERE dept_name = ?
    ORDER BY allocated_hrs 
    LIMIT ?
    """
    cursor.execute(query, (dept_name, no_of))
    result = cursor.fetchall()
    conn.close()
    staff_ids = [row[0] for row in result]
    return staff_ids
    

def fetch_same():
    conn = sqlite3.connect('staff.db')
    cursor = conn.cursor()

    query = """
    SELECT staff_id
    FROM staff_details
    WHERE dept_name = 'CSE'
    """
    cursor.execute(query)
    result = cursor.fetchall()

    conn.close()
    staff_ids = [row[0] for row in result]
    return staff_ids

def fetch_others():
    """
    Fetch all staff IDs from the database where the department name is not 'CSE'.

    :return: List of staff IDs from departments other than CSE
    """
    conn = sqlite3.connect('staff.db')
    cursor = conn.cursor()

    query = """
    SELECT staff_id
    FROM staff_details
    WHERE dept_name != 'CSE'
    """
    cursor.execute(query)
    result = cursor.fetchall()

    conn.close()
    staff_ids = [row[0] for row in result]
    return staff_ids

def fetch():
    """
    Fetch all staff IDs from the database.

    :return: List of all staff IDs
    """
    conn = sqlite3.connect('staff.db')
    cursor = conn.cursor()

    query = """
    SELECT staff_id
    FROM staff_details
    """
    cursor.execute(query)
    result = cursor.fetchall()

    conn.close()
    staff_ids = [row[0] for row in result]
    return staff_ids

def update():
    filenames = [
        "assets/StaffDatabase/CSV/staff.csv",
        "assets/StaffDatabase/CSV/day_1.csv",
        "assets/StaffDatabase/CSV/day_2.csv",
        "assets/StaffDatabase/CSV/day_3.csv",
        "assets/StaffDatabase/CSV/day_4.csv",
        "assets/StaffDatabase/CSV/day_5.csv"
    ]
    tablenames = ["staff_details", "day_1", "day_2", "day_3", "day_4", "day_5"]
    conn = sqlite3.connect('staff.db')
    cursor = conn.cursor()

    for filename, tablename in zip(filenames, tablenames):
        query = f"SELECT * FROM {tablename}"
        cursor.execute(query)
        result = cursor.fetchall()

        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            header = [description[0] for description in cursor.description]
            writer.writerow(header)
            print(header)
            writer.writerows(result)

    cursor.close()
    conn.commit()
    conn.close()

def add_staff(staff_name,staff_id,dept_name):
    f= [
        "assets/TimetableDatabase/CSV/day_1.csv",
        "assets/TimetableDatabase/CSV/day_2.csv",
        "assets/TimetableDatabase/CSV/day_3.csv",
        "assets/TimetableDatabase/CSV/day_4.csv",
        "assets/TimetableDatabase/CSV/day_5.csv"
    ]
    filenames = [
        "assets/StaffDatabase/CSV/staff.csv",
        "assets/StaffDatabase/CSV/day_1.csv",
        "assets/StaffDatabase/CSV/day_2.csv",
        "assets/StaffDatabase/CSV/day_3.csv",
        "assets/StaffDatabase/CSV/day_4.csv",
        "assets/StaffDatabase/CSV/day_5.csv"
    ]
    staff=[dept_name+str(staff_id),'ssn',0,0,0,0,0,0,0,'staff']
    for i in range(0,5):
        with open(f[i],'a',newline='\n') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(staff)
    staff=[dept_name+str(staff_id),staff_name,dept_name,10,0,0,0,0]
    with open(filenames[0],'a',newline='\n') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(staff)
    staff=[dept_name+str(staff_id),0,0,0,0,0,0,0]
    for i in range(1,6):
        with open(filenames[i],'a',newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(staff)
    ofa.restart_staff()
    ofa.restart_tt()
    