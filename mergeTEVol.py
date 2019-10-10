import pandas as pd
import sqlite3
from sqlite3 import Error

conn = sqlite3.connect("/Users/casa/Documents/sqlite-tools-osx-x86-3260000/ff.db")
sql="select s1,s2,month,t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11,t12,t13,t14,t15,t16,t17,t18,t19,t20,t21,t22,t23,t24 from flowdh order by s1,s2,month"
df = pd.read_sql(sql,conn)
outfile = '/Users/casa/Documents/FF/results.csv'
f1 = open(outfile,"w+")

def retype(vol,flow):
    if vol==flow:
        return 1
    elif vol>flow:
        return 2
    else:
        return 3


for name, row in df.iterrows():   
    s1=str(float(row["s1"]))
    s2=str(float(row["s2"]))
    m=str(float(row["month"]))
    sql="select vol from volflow where s1="+s1+" and s2="+s2+" and D="+m
    df1 = pd.read_sql(sql,conn)
    lst = []
    for name1, row1 in df1.iterrows():
        areatype=retype(row1["vol"],row["t1"])
        lst.append(areatype) 
    print(s1+"-"+s2)
    register = m+","+s1+","+s2+","+str(lst)
    register=register.replace("[","")
    register=register.replace("]","")    
    f1.write("%s\n" % register)
f1.close()

    
