import generate_timetable as gt
from PyQt5 import QtCore  
"""data={
    'LAB':{
    'UGE2197':['CSE116','JTL',"CSE1A",3], #PYL
    'UGS2197':['PHY301','JTL',"CSE1A",3], #PHYL
    },
    'OTHERS':{
    'UEN2176':['CSE110','LH45',"CSE1A",4], #ENG
    'UMA2176':['MATH201','LH45',"CSE1A",5],   #MATH
    'UPH2176':['PHY301','LH45',"CSE1A",3], #PHY
    'UCY2176':['CSE111','LH45',"CSE1A",3] #CHEM
    },
    'SAME':{
    
    'UGE2176':['CSE116','LH45',"CSE1A",3], #PY
    'UGE2177':['CSE122','LH45',"CSE1A",3]  #EG
    }
}
class_id="CSE1A" """
from OneForAll import queries as ofa
ofa.restart()
def pkp(data,class_id):
        print("$")
        QtCore.QCoreApplication.processEvents()
        if(gt.generate_timetable(data,class_id)==1):      
            print("Generation Successful\n")
            return 1
        else:
            print("Generate # Try again\n")
            return 0
   
#pkp(data,class_id)
#print(ofa.subqueries.fetch(1))




