import pandas as pd
import numpy as np
import sqlite3
from sqlite3 import Error
import operator
from datetime import date
from dateutil.rrule import rrule, DAILY
from datetime import timedelta 


conn = sqlite3.connect("/Users/casa/Documents/sqlite-tools-osx-x86-3260000/ff.db")
sql="select s1,s2,dweek,month,timestamp,t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11,t12,t13,t14,t15,t16,t17,t18,t19,t20,t21,t22,t23,t24 from flowdh"
df = pd.read_sql(sql,conn)
outfile = '/Users/casa/Documents/FF/score.csv'
f = open(outfile,"w+")
head = 's1,s2,dweek,month,timestamp,value,corr'
f.write("%s\n" % head)

def main():
    for name, row in df.iterrows():
        lst = row['t1':'t24'].values[0:24].tolist()
        s0=lst.count(0)
        s1=lst.count(1)
        s2=lst.count(2)
        s3=lst.count(3)
        stats = {'0':s0,'1':s1,'2':s2,'3':s3}
        sorted_x = sorted(stats.items(), key=operator.itemgetter(1),reverse=True)
        values = [i[1] for i in sorted_x]
        nkeys = [i[0] for i in sorted_x]
        if values[1:] == values[:-1]:   
            val=0
        elif values[0]==values[1] and values[1]==values[2]:
            val=0
        elif values[0]==values[1]:
            val=0
        else:
            val=int(nkeys[0])
        ndate = str(row['timestamp'])
        #ndate = ndate[6:10]+'-'+ndate[3:5]+'-'+ndate[0:2]
        register = str(row['s1'])+","+str(row['s2'])+","+str(row['dweek'])+","+str(row['month'])+","+ndate+","+str(val)+","+"0.0"
        print(str(row['s1'])+','+str(row['s2']))
        f.write("%s\n" % register)
    f.close()
    df1 = pd.read_csv('/Users/casa/Documents/FF/score.csv')
    df1.to_sql('scores',con=conn,if_exists='append',index=False)

if __name__ == '__main__':
    main()