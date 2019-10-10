import multiprocessing
import timeit
import jpype
import pandas as pd
import sqlite3
from sqlite3 import Error
from datetime import date
from dateutil.rrule import rrule, DAILY

start_time = timeit.default_timer()
conn = sqlite3.connect("/Users/casa/Documents/sqlite-tools-osx-x86-3260000/ff.db")
sql='select froml,tol,timew from distance where timew>=60 and timew<296;'
dfp = pd.read_sql(sql,conn)
dfpd=dfp.to_dict()


def startVM():
    # Change location of jar to match yours:
        #jarLocation = "\Users\casa\Documents\FF\infodynamics-dist-1.5\infodynamics.jar"
        jarLocation ="\Library\Java\Extensions\infodynamics.jar"
        # Start the JVM (add the "-Xmx" option with say 1024M if you get crashes due to not enough memory space)
        jpype.startJVM(jpype.getDefaultJVMPath(), "-ea", "-Djava.class.path=" + jarLocation)

def fun1(gn):
    x= dfpd['froml'][gn]
    y= dfpd['tol'][gn]
    z= dfpd['timew'][gn]
    ids=1
    a = date(2017, 4, 1)
    b = date(2017, 4, 2)
    
if __name__ == '__main__':

   for name, row in dfp.iterrows():       
        a = date(2017, 4, 1)
        b = date(2017, 4, 30) 
        s1=str(row["froml"])
        s2=str(row["tol"])
        p = multiprocessing.Pool(4)
        start_time = timeit.default_timer()
        p.map(fun1, for dt in rrule(DAILY, dtstart=a, until=b))
        stop_time = timeit.default_timer()
        print(stop_time - start_time)
        p.close()
        p.join()