from RoomDatabase import queries as rqueries
from StaffDatabase import queries as squeries
from ClassDatabase import  queries as cqueries
from TimetableDatabase import queries as tqueries
from SubjectDatabase import queries as subqueries
from RoomDatabase import database_operations as rdb
from StaffDatabase import database_operations as sdb
from ClassDatabase import  database_operations as cdb
from TimetableDatabase import database_operations as tdb
import time
from PyQt5 import QtCore, QtGui, QtWidgets
import threading
import queue
Q = queue.Queue()


def is_free_hour(faculty_id,room_id,class_id,day,hour):
    return ((squeries.is_free_hour(faculty_id,day,hour)) and (rqueries.is_free_hour(room_id,day,hour)) and (cqueries.is_free_hour(class_id,day,hour)))

def is_free_in_morning(faculty_id,room_id,class_id,day):
    return ((cqueries.is_free_in_morning(class_id,day)) and (squeries.is_free_in_morning(faculty_id,day)) and (rqueries.is_free_in_morning(room_id,day)))

def is_free_in_evening(faculty_id,room_id,class_id,day):
    return ((cqueries.is_free_in_morning(class_id,day)) and squeries.is_free_in_evening(faculty_id,day) and (rqueries.is_free_in_evening(room_id,day)))

def allocate_hour(subject_id,faculty_id,room_id,class_id,day,hour):
    squeries.allocate_hour(faculty_id,day,hour)
    rqueries.allocate_hour(room_id,day,hour)
    cqueries.allocate_hour(class_id,day,hour)
    tqueries.allocate_hour(class_id,day,hour,subject_id)
    tqueries.allocate_hour(faculty_id,day,hour,class_id)

def allocate_hour_morning(subject_id,faculty_id,room_id,class_id,day):
    squeries.allocate_hour_morning(faculty_id,day)
    rqueries.allocate_hour_morning(room_id,day)
    cqueries.allocate_hour_morning(class_id,day)
    tqueries.allocate_hour_morning(class_id,day,subject_id)
    tqueries.allocate_hour_morning(faculty_id,day,class_id)

def allocate_hour_evening(subject_id,faculty_id,room_id,class_id,day):
    squeries.allocate_hour_evening(faculty_id,day)
    rqueries.allocate_hour_evening(room_id,day)
    cqueries.allocate_hour_evening(class_id,day)
    tqueries.allocate_hour_evening(class_id,day,subject_id)
    tqueries.allocate_hour_evening(faculty_id,day,class_id)

def duplicate_class(class_id):
    res=tqueries.duplicate_subjects(class_id)
    time.sleep(1)
    for i in res:
        if(not(subqueries.is_lab(i))):
            if i!='0':
                Q.put(0)
                return
    Q.put(1)
    return 

def continuous_class(class_id):
    res=tqueries.continuous_subjects(class_id)
    time.sleep(1)
    for i in res:
        if(not(subqueries.is_lab(i))):
                Q.put(0)
                return 
    Q.put(1)
    return 



def check_ratio(data):
    QtCore.QCoreApplication.processEvents()
    r=[]
    skip=[0,1,2,3]
    
    for i in data:
        time.sleep(1)
        if i in skip:
            continue
        for j in data[i]:
            r.append(tqueries.ratio(data,data[i][j][2],j,data[i][j][3]))

    if sum(r)>=(0.5*(len(r))):
        Q.put(1)
        return
    Q.put(0)
    return

def updatecsv():
    squeries.update()
    rqueries.update()
    cqueries.update()
    tqueries.update()

def restart_class():
        print("Starting delete operations")
        cdb.drop_tables()
        print("cdb.delete_database done")
        
        cdb.create_table()
        print("cdb.create_table done")
        
        cdb.populate_database()
        print("cdb.populate_database done")
        

def restart_room():
        
        rdb.drop_tables()
        print("rdb.delete_database done")
        
        rdb.create_table()
        print("rdb.create_table done")
        
        rdb.populate_table()
        print("rdb.populate_table done")
        

def restart_staff():

      
        sdb.drop_tables()
        print("sdb.delete_database done")
        
        sdb.create_table()
        print("sdb.create_table done")
        
        sdb.populate_table()
        print("sdb.populate_table done")
       
        print("DONE")

def restart_tt():
        
        tdb.delete_table()
        print("tdb.delete_database done")
        print("Starting create operations")
        
        tdb.create_table()
        print("tdb.create_table done")
        print("Create Done")
      
        tdb.populate_table()
        print("Starting populate operations")
        
        print("DONE")


def restart():
    restart_tt()
    restart_class()
    restart_room()
    restart_staff()
