import csv,random,secrets
from OneForAll import queries as ofa
import sys
from PyQt5 import QtCore

def write_timetable(filename,timetable):
    with open(filename, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(timetable)
    print(f"Timetable created successfully and saved as '{filename}'")

def dept_class_allocation(timetable,subject_id,faculty_id,room_id,class_id,recommended_hrs,to_exclude):
    QtCore.QCoreApplication.processEvents()
    try:
        day = secrets.randbelow(5)+1
        while day in to_exclude:
            day = random.randint(1, 5)
        
        if(ofa.tqueries.morning_hrs(class_id,subject_id)<(int(recommended_hrs/2)+1)):
            if (ofa.is_free_hour(faculty_id,room_id,class_id,day,1)) :
                ofa.allocate_hour(subject_id,faculty_id,room_id,class_id,day,1)
                to_exclude.append(day)
                return timetable,to_exclude
            else:
                hour=random.randint(1,4)
                if (ofa.is_free_hour(faculty_id,room_id,class_id,day,hour)) :
                    ofa.allocate_hour(subject_id,faculty_id,room_id,class_id,day,hour)
                    to_exclude.append(day)
                    return timetable,to_exclude
                else:
                    timetable,to_exclude=dept_class_allocation(timetable,subject_id,faculty_id,room_id,class_id,recommended_hrs,to_exclude)
                    return timetable,to_exclude
        else:
            hour=random.randint(5,7)
            if (ofa.is_free_hour(faculty_id,room_id,class_id,day,hour)) :
                ofa.allocate_hour(subject_id,faculty_id,room_id,class_id,day,hour)
                to_exclude.append(day)
                return timetable,to_exclude
            else:
                timetable,to_exclude=dept_class_allocation(timetable,subject_id,faculty_id,room_id,class_id,recommended_hrs,to_exclude)
                return timetable,to_exclude
    except RecursionError:
        return 0,0
    
def other_dept_class_allocation(timetable,subject_id,faculty_id,room_id,class_id,recommended_hrs,to_exclude):
    QtCore.QCoreApplication.processEvents()
    try:
        day = secrets.randbelow(5)+1
        while day in to_exclude:
            day = random.randint(1, 5)
        if(ofa.tqueries.morning_hrs(class_id,subject_id)<(int(recommended_hrs/2)+1)):
            hour=random.randint(2,4)
            if (ofa.is_free_hour(faculty_id,room_id,class_id,day,hour)) :
                ofa.allocate_hour(subject_id,faculty_id,room_id,class_id,day,hour)
                to_exclude.append(day)
                return timetable,to_exclude
            else:
                timetable,to_exclude=other_dept_class_allocation(timetable,subject_id,faculty_id,room_id,class_id,recommended_hrs,to_exclude)
                return timetable,to_exclude
        else:
            hour=random.randint(5,7)
            if (ofa.is_free_hour(faculty_id,room_id,class_id,day,hour)) :
                ofa.allocate_hour(subject_id,faculty_id,room_id,class_id,day,hour)
                to_exclude.append(day)
                return timetable,to_exclude
            else:
                timetable,to_exclude=other_dept_class_allocation(timetable,subject_id,faculty_id,room_id,class_id,recommended_hrs,to_exclude)
                return timetable,to_exclude
    except RecursionError:
        return 0,0

def lab_allocation(timetable,subject_id,faculty_id,room_id,class_id):
    QtCore.QCoreApplication.processEvents()
    day=secrets.randbelow(5)+1
    session=random.randint(1,2)
    if session==1:
        if (ofa.is_free_in_morning(faculty_id,room_id,class_id,day)) :
            ofa.allocate_hour_morning(subject_id,faculty_id,room_id,class_id,day)
            return timetable
        else:
            timetable=lab_allocation(timetable, subject_id,faculty_id,room_id,class_id)
            return timetable
    else:
        if (ofa.is_free_in_evening(faculty_id,room_id,class_id,day)) :
            ofa.allocate_hour_evening(subject_id,faculty_id,room_id,class_id,day)
            return timetable
        else:
            timetable=lab_allocation(timetable, subject_id,faculty_id,room_id,class_id)
            return timetable
        
        

def start_generation(data,timetable):
    QtCore.QCoreApplication.processEvents()
    for i in data['LAB']:
        timetable=lab_allocation(timetable,i,data['LAB'][i][0],data['LAB'][i][1],data['LAB'][i][2])
        
       
    for i in data['OTHERS']:
        to_exclude=[]
        for j in range(data['OTHERS'][i][3]):
            timetable,to_exclude=other_dept_class_allocation(timetable,i,data['OTHERS'][i][0],data['OTHERS'][i][1],data['OTHERS'][i][2],data['OTHERS'][i][3],to_exclude)
            if (timetable == 0 and to_exclude== 0 ):
                return 0
           
        
    for i in data['SAME']:
        to_exclude=[]
        for j in range(data['SAME'][i][3]):
            timetable,to_exclude=dept_class_allocation(timetable,i,data['SAME'][i][0],data['SAME'][i][1],data['SAME'][i][2],data['SAME'][i][3],to_exclude)
            if (timetable == 0 and to_exclude== 0 ):
                return 0
    return timetable

def free_allocate(class_id):
    data=ofa.tqueries.fetch_timetable(class_id)
    to_exclude=[]
    fhours=["P&T","ICELL","Library","Mentor","PED","Project(IFSP)"]
    for i in range(len(data)):
        for j in range(len(data[i])):
            if data[i][j]=="0":
                print(i,j)
                id=random.choice(list(set(fhours)-set(to_exclude)))
                ofa.tqueries.allocate_hour(class_id,i,j,id)
                to_exclude.append(id)



def generate_timetable(data,class_id):
    sys.setrecursionlimit(300)
    QtCore.QCoreApplication.processEvents()
    filename="timetable.csv"
    timetable = [['', '8:00 AM - 8:50 AM', '8:50 AM - 9:40 AM', '10:00 AM - 10:50 AM', '10:50 AM - 11:40 AM', '12:45 PM - 1:35 PM','1:35 PM - 2:25 PM','2:50 PM - 3:40 PM'],
                    ['Monday', '0', '0', '0', '0', '0','0','0'],
                    ['Tuesday', '0', '0', '0', '0', '0','0','0'],
                    ['Wednesday', '0', '0', '0', '0', '0','0','0'],
                    ['Thursday', '0', '0', '0', '0', '0','0','0'],
                    ['Friday', '0', '0', '0', '0', '0','0','0']]
    timetable=start_generation(data,timetable)
    
    if timetable==0 :
        return -1
    free_allocate(class_id)
    print("DONE")
    #ofa.duplicate_class(class_id)
    #ofa.continuous_class(class_id)
    #print(ofa.Q.get())
    """print(ofa.Q.get(),ofa.Q.get(),ofa.Q.get())"""
    write_timetable(filename,timetable)
    """if ( (x==1) and (y==1) and (z==1) ):
        return 1"""
    return 1