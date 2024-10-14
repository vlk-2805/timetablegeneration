import num2words,csv,sqlite3

def is_free_hour(class_id, day, hour):
    """
    Check if a class is free at a specific hour on a specific day.

    :param class_id: The class's ID
    :param day: The day of the week (1-5)
    :param hour: The hour of the day (1-7)
    :return: True if the class is free, False otherwise
    """
    
    hour_name = num2words.num2words(hour).replace('-', '_')
    table_name = f"day_{day}"
    conn = sqlite3.connect('class.db')
    cursor = conn.cursor()

    query1 = f"""
    SELECT 
        CASE 
        WHEN {hour_name} = 0 THEN 1
        ELSE 0
        END AS is_free
    FROM 
        {table_name}
    WHERE 
        class_id = ?
    """
   
    query2 = f"""
    SELECT 
        CASE 
        WHEN allocated_hrs < max_hrs THEN 1
        ELSE 0
        END AS is_free
    FROM 
        class_details
    WHERE 
        class_id = ?
    """

    cursor.execute(query1, (class_id,))
    result1 = cursor.fetchone()
    
    cursor.execute(query2, (class_id,))
    result2 = cursor.fetchone()

    conn.close()

  
    return (result1 is not None and result1[0] == 1) and (result2 is not None and result2[0] == 1)

def is_free_in_morning(class_id, day):
    """
    Check if a class is free during a specific session on a specific day.

    :param class_id: The class's ID
    :param day: The day of the week (1-5)
    :return: True if the class is free, False otherwise
    """
    table_name = f"day_{day}"
    conn = sqlite3.connect('class.db')
    cursor = conn.cursor()

    query1 = f"""
    SELECT 
        CASE 
        WHEN one = 0 AND two = 0 AND three = 0 AND four = 0 AND lab = 0 THEN 1
        ELSE 0
        END AS is_free
    FROM 
        {table_name}
    WHERE 
        class_id = ?
    """
    
    query2 = f"""
    SELECT 
        CASE 
        WHEN allocated_hrs < max_hrs THEN 1
        ELSE 0
        END AS is_free
    FROM 
        class_details
    WHERE 
        class_id = ?
    """

    cursor.execute(query1, (class_id,))
    result1 = cursor.fetchone()
 
    cursor.execute(query2, (class_id,))
    result2 = cursor.fetchone()

    conn.close()

    return (result1 is not None and result1[0] == 1) and (result2 is not None and result2[0] == 1)

def is_free_in_evening(class_id, day):
    """
    Check if a class is free during a specific session on a specific day.

    :param class_id: The class's ID
    :param day: The day of the week (1-5)
    :return: True if the class is free, False otherwise
    """
    table_name = f"day_{day}"
    conn = sqlite3.connect('class.db')
    cursor = conn.cursor()
    query1 = f"""
    SELECT 
        CASE 
        WHEN five = 0 AND six = 0 AND seven = 0 AND lab = 0 THEN 1
        ELSE 0
        END AS is_free
    FROM 
        {table_name}
    WHERE 
        class_id = ?
    """
    query2 = f"""
    SELECT 
        CASE 
        WHEN allocated_hrs < max_hrs THEN 1
        ELSE 0
        END AS is_free
    FROM 
        class_details
    WHERE 
        class_id = ?
    """
    cursor.execute(query1, (class_id,))
    result1 = cursor.fetchone()
    
    cursor.execute(query2, (class_id,))
    result2 = cursor.fetchone()

    conn.close()

    return (result1 is not None and result1[0] == 1) and (result2 is not None and result2[0] == 1)

def allocate_hour_morning(class_id, day):
    """
    Allocate class to a subject on a specific day.

    :param class_id: The class's ID
    :param day: The day of the week (1-5)
    """
    table_name = f"day_{day}"
    conn = sqlite3.connect('class.db')
    cursor = conn.cursor()
    query = f"""
    UPDATE {table_name}
    SET two = 1, three = 1, four = 1, lab = 1
    WHERE class_id = ?
    """
    cursor.execute(query, (class_id,))

    conn.commit()

    conn.close()
    

def allocate_hour_evening(class_id, day):
    """
    Allocate class to a subject on a specific day.

    :param class_id: The class's ID
    :param day: The day of the week (1-5)
    """
    table_name = f"day_{day}"
    conn = sqlite3.connect('class.db')
    cursor = conn.cursor()

    query = f"""
    UPDATE {table_name}
    SET five = 1, six = 1, seven = 1, lab = 1
    WHERE class_id = ?
    """

    cursor.execute(query, (class_id,))

    conn.commit()

    conn.close()
    

def allocate_hour(class_id, day, hour):
    """
    Allocate class to a specific hour on a specific day.

    :param class_id: The class's ID
    :param day: The day of the week (1-5)
    :param hour: Hour of class (1-7)
    """
    table_name = f"day_{day}"
    hour_name = num2words.num2words(hour).replace('-', '_')
    conn = sqlite3.connect('class.db')
    cursor = conn.cursor()

    query = f"""
    UPDATE {table_name}
    SET {hour_name} = 1
    WHERE class_id = ?
    """

    cursor.execute(query, (class_id,))

    conn.commit()


    conn.close()
def class_name(class_id):
    """
    Returns class name for that class id.

    :return: class name
    """
    conn = sqlite3.connect('class.db')
    cursor = conn.cursor()
    query = f"""
    SELECT class_name
    FROM class_details
    WHERE class_id = "{class_id}"
    """
    cursor.execute(query)
    result = cursor.fetchone()
    conn.close()
    if result:
        class_ids = result[0]
        return class_ids

def fetch():
    """
    Fetch all class IDs from the database.

    :return: List of class IDs
    """
    conn = sqlite3.connect('class.db')
    cursor = conn.cursor()
    query = """
    SELECT class_id
    FROM class_details
    """
    cursor.execute(query)
    result = cursor.fetchall()
    conn.close()
    class_ids = [row[0] for row in result]
    return class_ids

def update():
    filenames = [
        "assets/ClassDatabase/CSV/class.csv",
        "assets/ClassDatabase/CSV/day_1.csv",
        "assets/ClassDatabase/CSV/day_2.csv",
        "assets/ClassDatabase/CSV/day_3.csv",
        "assets/ClassDatabase/CSV/day_4.csv",
        "assets/ClassDatabase/CSV/day_5.csv"
    ]
    tablenames = ["class_details", "day_1", "day_2", "day_3", "day_4", "day_5"]
    conn = sqlite3.connect('class.db')
    cursor = conn.cursor()

    for filename, tablename in zip(filenames, tablenames):
        query = f"""SELECT * FROM {tablename}"""
        cursor.execute(query)
        result = cursor.fetchall()
        with open(filename, 'w', newline='') as csvfile:
            writer = csv.writer(csvfile)
            header = [description[0] for description in cursor.description]
            writer.writerow(header)
            for row in result:
                writer.writerow(row)

    cursor.close()
    conn.commit()
    conn.close()