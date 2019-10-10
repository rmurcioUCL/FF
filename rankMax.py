import pandas as pd
import sqlite3
from sqlite3 import Error

conn = sqlite3.connect("/Users/casa/Documents/sqlite-tools-osx-x86-3260000/ff.db")

#outfile='/Users/casa/Documents/FF/ranks.csv'
#f = open(outfile,"w+")
df = pd.read_csv('/Users/casa/Documents/FF/locpairs.csv')
dtf = pd.DataFrame({}, columns=['value','rank'])
posf=0
for i in range(0,df.shape[0]):
    s1 = df.loc[i,'s1']
    s2 = df.loc[i,'s2']
    print(str(s1)+"-"+str(s2))
    sql="select value,quad,pquad from scoresAgg where s1="+str(s1)+" and s2="+str(s2)+" order by pquad desc;"
    dfr=pd.read_sql(sql,conn)
    #rank=dfr.shape[0]
    rank=1
    pos=0
    dfr['rank']=0

    for name, row in dfr.iterrows():
        #dfr.loc[pos,'rank']=rank
        dtf.loc[posf,'value']=dfr.loc[pos,'value']
        dtf.loc[posf,'rank']=rank    
        rank=rank+1
        pos=pos+1
        posf=posf+1
dtf.to_csv(r'/Users/casa/Documents/FF/ranks.csv')
    
