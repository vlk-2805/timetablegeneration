import num2words,csv,sqlite3
from OneForAll import queries as ofa
def allocate_hour_morning(id,day,allocated_id):
    """
    Allocate class to a particular id  on a specific day.

    :param id: The  ID
    :param day: The day of the week (1-5)
    :allocated_id: The Allocated ID
    """
    conn = sqlite3.connect('timetable.db')
    cursor = conn.cursor()

    table_name = f"day_{day}"

    query = f"""
    UPDATE {table_name}
    SET two = ?, three = ?, four = ?
    WHERE id = ?
    """
    cursor.execute(query, (allocated_id, allocated_id, allocated_id, id))
    conn.commit()
    conn.close()
    

def allocate_hour_evening(id,day,allocated_id):
    """
    Allocate class to a ID on a specific day.

    :param id: The  ID
    :param day: The day of the week (1-5)
    :allocated_id: The Allocated ID
    """
    conn = sqlite3.connect('timetable.db')
    cursor = conn.cursor()

    table_name = f"day_{day}"

    query = f"""
    UPDATE {table_name}
    SET five = ?, six = ?, seven = ?
    WHERE id = ?
    """
    cursor.execute(query, (allocated_id, allocated_id, allocated_id, id))
    conn.commit()
    conn.close()
    

def allocate_hour(id,day,hour,allocated_id):
    """
    Allocate class to a ID on a specific day.

    :param id: The  ID
    :param day: The day of the week (1-5)
    :param hour: Hour of class
    :allocated_id: The Allocated ID
    """
    
    conn = sqlite3.connect('timetable.db')
    cursor = conn.cursor()

    table_name = f"day_{day}"
    hour_name = num2words.num2words(hour)

    query = f"""
    UPDATE {table_name}
    SET {hour_name} = ?
    WHERE id = ?
    """
    cursor.execute(query, (allocated_id, id))
    conn.commit()
    conn.close()

def duplicate_subjects(class_id):
    """
    Returns subjects which occurs more than twice in a day.

    :param class_id: The class's ID
    :return: List of duplicate subjects
    """
    subjects = []
    conn = sqlite3.connect('timetable.db')
    cursor = conn.cursor()

    for i in range(1, 6):
        query = f"""
            SELECT *
            FROM day_{i}
            WHERE id = ?
        """
        cursor.execute(query, (class_id,))
        res = cursor.fetchone()

        if res:
            
            subjects += [subject for subject in res if (res.count(subject) > 2 and subject != "0")]

    cursor.close()
    conn.close()
    return list(set(subjects))

def fetch_class(staff_id):
    """
    Returns classes which taken by that staff .

    :param class_id: The class's ID
    :return: List of duplicate subjects
    """
    classes = []
    conn = sqlite3.connect('timetable.db')
    cursor = conn.cursor()

    for i in range(1, 6):
        query = f"""
            SELECT one,two,three,four,five,six,seven
            FROM day_{i}
            WHERE id = ?
        """
        cursor.execute(query, (staff_id,))
        res = cursor.fetchone()
        
        if res:
            for cls in res:
                temp_lst=[cls,ofa.cqueries.class_name(cls)]
                sub_id=find_sub(staff_id,cls) 
                temp_lst.append(sub_id)
                if temp_lst not in classes:
                    if (res.count(cls) > 0 and cls != "0") :
                        classes.append(temp_lst)
    print(classes)
    cursor.close()
    conn.close()
    return classes

def fetch_subs(class_id):
    """
    Returns subject which are alotted for that .

    :param staff_id: The staff's ID
    :return: List of subjects
    """
    subs = []
    conn = sqlite3.connect('timetable.db')
    cursor = conn.cursor()

    for i in range(1, 6):
        query = f"""
            SELECT one,two,three,four,five,six,seven
            FROM day_{i}
            WHERE id = ?
        """
        cursor.execute(query, (class_id,))
        res = cursor.fetchone()
        fhours=["P&T","ICELL","Library","Mentor","PED","Project(IFSP)"]
        if res:
            for sub in res:
                if sub in fhours:
                    continue
                temp_lst=[sub,ofa.subqueries.subject_name(sub)]
                staff_id=find_staff_name(sub,class_id) 
                temp_lst.append(staff_id)
                if temp_lst not in subs:
                    if (res.count(sub) > 0 and sub != "0") :
                        subs.append(temp_lst)
    print(subs)
    cursor.close()
    conn.close()
    return subs

def morning_hrs(class_id, subject_id):
    res = 0
    conn = sqlite3.connect('timetable.db')
    cursor = conn.cursor()

    for j in range(1, 5):
        for i in range(1, 6):
            query = f"""
                    SELECT {num2words.num2words(j)} 
                    FROM day_{i}
                    WHERE
                    id="{class_id}" AND {num2words.num2words(j)} = "{subject_id}" 
                """
            cursor.execute(query)
            if cursor.fetchone():
                res += 1

    cursor.close()
    conn.close()

    return res

def evening_hrs(class_id,subject_id):
    res = 0
    conn = sqlite3.connect('timetable.db')
    cursor = conn.cursor()

    for j in range(5, 8):
        for i in range(1, 6):
            query = f"""
                    SELECT {num2words.num2words(j)} 
                    FROM day_{i}
                    WHERE
                    id="{class_id}" AND {num2words.num2words(j)} = "{subject_id}" 
                """
            cursor.execute(query)
            if cursor.fetchone():
                res += 1

    cursor.close()
    conn.close()

    return res

def continuous_subjects(class_id):
    """
    Returns subjects which occur continuously in a day.

    :param class_id: The class's ID
    :return: List of continuous subjects
    """
    result = []
    conn = sqlite3.connect('timetable.db')
    cursor = conn.cursor()

    for i in range(1, 6):
        query = f"""
        SELECT
            CASE WHEN one = two AND one != "0" THEN one
                 WHEN two = three AND two != "0" THEN two
                 WHEN three = four AND three != "0" THEN three
                 WHEN four = five AND four != "0" THEN four
                 WHEN five = six AND five != "0" THEN five
                 WHEN six = seven AND six != "0" THEN six
                 ELSE NULL
            END AS matched_subject
        FROM day_{i}
        WHERE id = ?
        """
        cursor.execute(query, (class_id,))
        res = cursor.fetchall()

        if res:
            for row in res:
                if row[0] is not None:
                    result.append(row[0])

    cursor.close()
    conn.close()

    return result

def update():
    filenames = [
        "assets/TimetableDatabase/CSV/day_1.csv",
        "assets/TimetableDatabase/CSV/day_2.csv",
        "assets/TimetableDatabase/CSV/day_3.csv",
        "assets/TimetableDatabase/CSV/day_4.csv",
        "assets/TimetableDatabase/CSV/day_5.csv"
    ]
    tablenames = ["day_1", "day_2", "day_3", "day_4", "day_5"]

    conn = sqlite3.connect('timetable.db')
    cursor = conn.cursor()

    for filename, tablename in zip(filenames, tablenames):
        query = f"SELECT * FROM {tablename}"
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

def ratio(class_id, subject_id, recommended_hrs):
    conn = sqlite3.connect('timetable.db')
    cursor = conn.cursor()

    query_lab = f"SELECT subject_id FROM subject_details WHERE lab = 1"
    cursor.execute(query_lab)
    lab_subjects = cursor.fetchall()

    if (subject_id,) in lab_subjects:
        cursor.close()
        conn.close()
        return 1
    else:
        if recommended_hrs == 5:
            m = morning_hrs(class_id, subject_id, cursor)
            e = evening_hrs(class_id, subject_id, cursor)
            if e > 0:
                if m / e == 3 / 2:
                    cursor.close()
                    conn.close()
                    return 1
        if recommended_hrs == 4:
            m = morning_hrs(class_id, subject_id, cursor)
            e = evening_hrs(class_id, subject_id, cursor)
            if e > 0:
                if m / e == 1 or m / e == 3 / 1:
                    cursor.close()
                    conn.close()
                    return 1
            return 0
        elif recommended_hrs == 3:
            m = morning_hrs(class_id, subject_id, cursor)
            e = evening_hrs(class_id, subject_id, cursor)
            if e > 0:
                if m / e == 2 or m / e == 1 / 2:
                    cursor.close()
                    conn.close()
                    return 1
            else:
                cursor.close()
                conn.close()
                return 1
            return 0

    cursor.close()
    conn.close()
    return 1

def fetch_timetable(id):
    conn = sqlite3.connect('timetable.db')
    cursor = conn.cursor()
    timetable = [['', '8:00 AM - 8:50 AM', '8:50 AM - 9:40 AM', '10:00 AM - 10:50 AM', '10:50 AM - 11:40 AM', '12:45 PM - 1:35 PM','1:35 PM - 2:25 PM','2:50 PM - 3:40 PM'],
                    ['Monday', '0', '0', '0', '0', '0','0','0'],
                    ['Tuesday', '0', '0', '0', '0', '0','0','0'],
                    ['Wednesday', '0', '0', '0', '0', '0','0','0'],
                    ['Thursday', '0', '0', '0', '0', '0','0','0'],
                    ['Friday', '0', '0', '0', '0', '0','0','0']]
    for i in range(1,6):
        query=f"""
        SELECT one,two,three,four,five,six,seven 
        FROM day_{i}
        WHERE id="{id}"
        """
        cursor.execute(query)
        res=cursor.fetchall()
        k=1
        for j in res[0]:
            timetable[i][k]=j
            k+=1
    print(timetable)
    return timetable

def find_first_occurence(class_id,staff_id):
    conn = sqlite3.connect('timetable.db')
    cursor = conn.cursor()
    for i in range(1,6):
        for j in range(1,8):
            hour_name= num2words.num2words(j)
            query=f"""
            SELECT {hour_name}
            FROM day_{i}
            WHERE id = "{staff_id}" and "{hour_name}"= "{class_id}"
            """
            cursor.execute(query)
            res=cursor.fetchone()
            print(res)
            if res:
                return i,hour_name

def find_subject(class_id,day,hour_name):
    conn = sqlite3.connect('timetable.db')
    cursor = conn.cursor()
    query=f"""
            SELECT {hour_name}
            FROM day_{day}
            WHERE id = "{class_id}"
            """
    cursor.execute(query)
    res=cursor.fetchone()
    print(res)
    if res:
        return res[0]

def find_sub(staff_id,class_id):
    day,hour=find_first_occurence(class_id,staff_id)
    subject_id=find_subject(class_id,day,hour)
    return subject_id

def find_first_occurence_subject(class_id,subject_id):
    conn = sqlite3.connect('timetable.db')
    cursor = conn.cursor()
    for i in range(1,6):
        for j in range(1,8):
            hour_name= num2words.num2words(j)
            query=f"""
            SELECT {hour_name}
            FROM day_{i}
            WHERE id = "{class_id}" and "{hour_name}"= "{subject_id}"
            """
            cursor.execute(query)
            res=cursor.fetchone()
            print(res)
            if res:
                return i,hour_name

def find_staff(class_id,day,hour_name):
    conn = sqlite3.connect('timetable.db')
    cursor = conn.cursor()
    query=f"""
            SELECT id
            FROM day_{day}
            WHERE {hour_name}="{class_id}"
            """
    cursor.execute(query)
    res=cursor.fetchone()
    print(res)
    if res:
        return res[0]
    
def find_staff_name(subject_id,class_id):
    day,hour=find_first_occurence_subject(class_id,subject_id)
    staff_id=find_staff(class_id,day,hour)
    return staff_id