import pandas as pd
import numpy as np
import sqlite3
from sqlite3 import Error
import operator
from datetime import date
from dateutil.rrule import rrule, DAILY
from datetime import timedelta 


conn = sqlite3.connect("/Users/casa/Documents/sqlite-tools-osx-x86-3260000/ff.db")
sql = 'select * from flowd'
df = pd.read_sql(sql,conn)


def groupbyHour(mydata):
    agglist = [-1]*24
    c=0
   
    for i in range(0,278,12):
        s0=mydata[i:i+12].tolist().count(0)
        s1=mydata[i:i+12].tolist().count(1)
        s2=mydata[i:i+12].tolist().count(2)
        s3=mydata[i:i+12].tolist().count(3)
        stats = {'0':s0,'1':s1,'2':s2,'3':s3}
        sorted_x = sorted(stats.items(), key=operator.itemgetter(1),reverse=True)
        values = [i[1] for i in sorted_x]
        nkeys = [i[0] for i in sorted_x]
        if values[1:] == values[:-1]:
            agglist[c]=0
        elif values[0]==values[1] and values[1]==values[2]:
            agglist[c]=0
        elif values[0]==values[1]:
            agglist[c]=0
        else:
            agglist[c]=int(nkeys[0])

        c=c+1

    return agglist

def main():

    outfile1 = '/Users/casa/Documents/FF/flowdh.csv'
    f2 = open(outfile1,"w+")
    lsth = 's1,s2,timestamp,dweek,month,t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11,t12,t13,t14,t15,t16,t17,t18,t19,t20,t21,t22,t23,t24'
    f2.write("%s\n" % lsth)
    for name, row in df.iterrows():
        print(str(row['s1'])+','+str(row['s2']))
        results = row[5:292]
        rgroup = groupbyHour(results)
        rgroup=str(rgroup).replace("[","")
        rgroup=str(rgroup).replace("]","")
        rgroup=str(row['s1'])+","+str(row['s2'])+","+str(row['dweek'])+","+str(row['month'])+","+str(row['timestamp'])+","+rgroup
        f2.write("%s\n" % str(rgroup))
    f2.close()
    df1 = pd.read_csv('/Users/casa/Documents/FF/flowdh.csv')
    df1.to_sql('flowdh',con=conn,if_exists='append',index=False)


if __name__ == '__main__':
    main()
