import num2words,csv,sqlite3

def is_free_hour(room_id, day, hour):
    """
    Check if a room is free at a specific hour on a specific day.

    :param room_id: The room's ID
    :param day: The day of the week (1-5)
    :param hour: The hour of the day (1-7)
    :return: True if the room is free, False otherwise
    """
    hour_name = num2words.num2words(hour)  
    table_name = f"day_{day}"

    conn = sqlite3.connect('room.db')
    cursor = conn.cursor()
    cursor.execute(f'''
    SELECT 
        room_id,
        CASE 
        WHEN {hour_name} = 0 THEN 1
        ELSE 0
        END AS is_free
    FROM 
        {table_name}
    WHERE 
        room_id = ?
    ''', (room_id,))
    result1 = cursor.fetchone()  
    cursor.execute('''
    SELECT 
        room_id,
        CASE 
        WHEN allocated_hrs < max_hrs THEN 1
        ELSE 0
        END AS is_free
    FROM 
        room_details
    WHERE 
        room_id = ?
    ''', (room_id,))
    result2 = cursor.fetchone()  

    conn.close()
    if result1 and result2:
        return bool(result1[1]) and bool(result2[1])
    else:
        return False 

def is_free_in_morning(room_id, day):
    """
    Check if a room is free during the morning session on a specific day.

    :param room_id: The room's ID
    :param day: The day of the week (1-5)
    :return: True if the room is free, False otherwise
    """
    table_name = f"day_{day}"
    conn = sqlite3.connect('room.db')
    cursor = conn.cursor()
    cursor.execute(f'''
    SELECT 
        room_id,
        CASE 
        WHEN one = 0 AND two = 0 AND three = 0 AND four = 0 THEN 1
        ELSE 0
        END AS is_free
    FROM 
        {table_name}
    WHERE 
        room_id = ?
    ''', (room_id,))
    result1 = cursor.fetchone()  
    cursor.execute('''
    SELECT 
        room_id,
        CASE 
        WHEN allocated_hrs < max_hrs THEN 1
        ELSE 0
        END AS is_free
    FROM 
        room_details
    WHERE 
        room_id = ?
    ''', (room_id,))
    result2 = cursor.fetchone() 

    conn.close()
    if result1 and result2:
        return bool(result1[1]) and bool(result2[1])
    else:
        return False  
    
def is_free_in_evening(room_id, day):
    """
    Check if a room is free during the evening session on a specific day.

    :param room_id: The room's ID
    :param day: The day of the week (1-5)
    :return: True if the room is free, False otherwise
    """
    table_name = f"day_{day}"
    conn = sqlite3.connect('room.db')
    cursor = conn.cursor()
    cursor.execute(f'''
    SELECT 
        room_id,
        CASE 
        WHEN five = 0 AND six = 0 AND seven = 0 THEN 1
        ELSE 0
        END AS is_free
    FROM 
        {table_name}
    WHERE 
        room_id = ?
    ''', (room_id,))
    result1 = cursor.fetchone()  
    cursor.execute('''
    SELECT 
        room_id,
        CASE 
        WHEN allocated_hrs < max_hrs THEN 1
        ELSE 0
        END AS is_free
    FROM 
        room_details
    WHERE 
        room_id = ?
    ''', (room_id,))
    result2 = cursor.fetchone()  
    conn.close()
    if result1 and result2:
        return bool(result1[1]) and bool(result2[1])
    else:
        return False


def allocate_hour_morning(room_id, day):
    """
    Allocate room to a subject on a specific day during the morning hours.

    :param room_id: The room's ID
    :param day: The day of the week (1-5)
    """
    table_name = f"day_{day}"
    conn = sqlite3.connect('room.db')
    cursor = conn.cursor()
    query = f"""
    UPDATE {table_name}
    SET two = 1, three = 1, four = 1
    WHERE room_id = ?
    """
    cursor.execute(query, (room_id,))
    conn.commit()
    conn.close()


def allocate_hour_evening(room_id, day):
    """
    Allocate room to a subject on a specific day during the evening hours.

    :param room_id: The room's ID
    :param day: The day of the week (1-5)
    """
    table_name = f"day_{day}"
    conn = sqlite3.connect('room.db')
    cursor = conn.cursor()
    query = f"""
    UPDATE {table_name}
    SET five = 1, six = 1, seven = 1
    WHERE room_id = ?
    """
    cursor.execute(query, (room_id,))
    conn.commit()
    conn.close()


def allocate_hour(room_id, day, hour):
    """
    Allocate a room to a class on a specific day and hour.

    :param room_id: The room's ID
    :param day: The day of the week (1-5)
    :param hour: The hour of the day (1-7)
    """
    table_name = f"day_{day}"
    hour_name = num2words.num2words(hour)  
    conn = sqlite3.connect('room.db')
    cursor = conn.cursor()
    query = f"""
    UPDATE {table_name}
    SET {hour_name} = 1
    WHERE room_id = ?
    """
    cursor.execute(query, (room_id,))
    conn.commit()
    conn.close()

def update():
    filenames = [
        "assets/RoomDatabase/CSV/room.csv",
        "assets/RoomDatabase/CSV/day_1.csv",
        "assets/RoomDatabase/CSV/day_2.csv",
        "assets/RoomDatabase/CSV/day_3.csv",
        "assets/RoomDatabase/CSV/day_4.csv",
        "assets/RoomDatabase/CSV/day_5.csv"
    ]
    tablenames = ["room_details", "day_1", "day_2", "day_3", "day_4", "day_5"]

    conn = sqlite3.connect('room.db')
    cursor = conn.cursor()

    for filename, tablename in zip(filenames, tablenames):
        query = f"SELECT * FROM {tablename}"
        cursor.execute(query)
        result = cursor.fetchall()

        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            header = [description[0] for description in cursor.description]
            writer.writerow(header)
            writer.writerows(result)

    conn.close()

def fetch():
    """
    Fetch all room IDs from the database.

    :return: List of room IDs
    """
    conn = sqlite3.connect('room.db')
    cursor = conn.cursor()
    query = """
    SELECT room_id
    FROM room_details
    """
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    room_ids = [row[0] for row in result]
    return room_ids

def fetch_lab():
    """
    Fetch all room IDs from the database where the room is a lab.

    :return: List of room IDs that are labs
    """
    conn = sqlite3.connect('room.db')
    cursor = conn.cursor()
    query = """
    SELECT room_id
    FROM room_details
    WHERE lab = 1
    """
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    lab_room_ids = [row[0] for row in result]
    return lab_room_ids

def fetch_lh():
    """
    Fetch all room IDs from the database where the room is not a lab.

    :return: List of room IDs that are not labs
    """
    conn = sqlite3.connect('room.db')
    cursor = conn.cursor()
    query = """
    SELECT room_id
    FROM room_details
    WHERE lab = 0
    """
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    lh_room_ids = [row[0] for row in result]
    return lh_room_ids