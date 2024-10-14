import csv,sqlite3
import num2words

def is_lab(subject_id):
    conn = sqlite3.connect('subject.db')
    cursor = conn.cursor()

    query = f"""
    SELECT lab 
    FROM subject_details
    WHERE subject_id = ?
    """
    cursor.execute(query, (subject_id,))
    result = cursor.fetchone()

    conn.close()

    if result:
        return bool(result[0])
    else:
        return False

def recommended_hrs(subject_id):
    conn = sqlite3.connect('subject.db')
    cursor = conn.cursor()
    query = f"""
    SELECT recommended_hrs 
    FROM subject_details
    WHERE subject_id = ?
    """
    cursor.execute(query, (subject_id,))
    result = cursor.fetchone()

    conn.close()
    if result:
        return result[0]
    else:
        return None

def fetch_labs(sem):
    conn = sqlite3.connect('subject.db')
    cursor = conn.cursor()

    query = f"""
    SELECT subject_id
    FROM subject_details
    WHERE lab = 1 AND sem = "{sem}"
    """
    cursor.execute(query)
    result = cursor.fetchall()

    conn.close()

    subject_ids = [row[0] for row in result]
    return subject_ids

def fetch_others(sem):
 
    conn = sqlite3.connect('subject.db')
    cursor = conn.cursor()

    query = f"""
    SELECT subject_id
    FROM subject_details
    WHERE dept_name != 'CSE' AND lab = 0 AND sem = "{sem}"
    """
    cursor.execute(query)
    result = cursor.fetchall()

    conn.close()

    subject_ids = [row[0] for row in result]
    return subject_ids

def fetch_same(sem):
    
    conn = sqlite3.connect('subject.db')
    cursor = conn.cursor()

    
    query = f"""
    SELECT subject_id
    FROM subject_details
    WHERE dept_name = 'CSE' AND lab = 0 AND sem = "{sem}"
    """
    cursor.execute(query)
    result = cursor.fetchall()

  
    conn.close()

    subject_ids = [row[0] for row in result]
    return subject_ids

def fetch(sem):
    
    conn = sqlite3.connect('subject.db')
    cursor = conn.cursor()

    query = f"""
    SELECT subject_id,subject_name
    FROM subject_details
    WHERE sem = "{sem}"
    """
    cursor.execute(query)
    result = cursor.fetchall()

    conn.close()

    subject_ids = [[row[0],row[1]] for row in result]
    return subject_ids

def which_dept(subject_id):
    conn = sqlite3.connect('subject.db')
    cursor = conn.cursor()

    query = f"""
    SELECT dept_name
    FROM subject_details
    WHERE subject_id = "{subject_id}"
    """
    cursor.execute(query)
    result = cursor.fetchone()

    conn.close()
    if result:
        return result[0]
    
def subject_name(subject_id):
    conn = sqlite3.connect('subject.db')
    cursor = conn.cursor()

    query = f"""
    SELECT subject_name
    FROM subject_details
    WHERE subject_id = "{subject_id}"
    """
    cursor.execute(query)
    result = cursor.fetchone()

    conn.close()
    if result:
        return result[0]