import sqlite3
from sqlite3 import Error
import pandas as pd
import numpy as np

conn = sqlite3.connect("/Users/casa/Documents/sqlite-tools-osx-x86-3260000/ff.db")

def main():
    
    df = pd.read_csv('/Users/casa/Documents/FF/locpairs.csv')
    #j=12
    #for j in range(1,9):
    fdf = []
    for i in range(0,df.shape[0]):
        s1 = df.loc[i,'s1']
        s2 = df.loc[i,'s2']
        #sql='select strftime(\'%d\',timestamp) as D,strftime(\'%H\',timestamp) as H,sum(total) as T from counts where location='+str(s1)+' and timestamp>=\'2017-'+str(j)+'-01\' and timestamp<\'2018-01-01\' group by strftime(\'%d\',timestamp),strftime(\'%H\',timestamp);'
        sql = 'select strftime(\'%m\',timestamp) as D,strftime(\'%H\',timestamp) as H,avg(total) as T from counts where location='+str(s1)+' and dweek>=1 and dweek<6 group by strftime(\'%m\',timestamp),strftime(\'%H\',timestamp);' 
        dfs1=pd.read_sql(sql,conn)
        #sql='select strftime(\'%d\',timestamp) as D,strftime(\'%H\',timestamp) as H,sum(total) as T from counts where location='+str(s2)+' and timestamp>=\'2017-'+str(j)+'-01\' and timestamp<\'2018-01-01\' group by strftime(\'%d\',timestamp),strftime(\'%H\',timestamp);'
        sql = 'select strftime(\'%m\',timestamp) as D,strftime(\'%H\',timestamp) as H,avg(total) as T from counts where location='+str(s2)+' and dweek>=1 and dweek<6 group by strftime(\'%m\',timestamp),strftime(\'%H\',timestamp);' 
        dfs2=pd.read_sql(sql,conn)
        dfs1 = dfs1.assign(s1=s1)
        dfs1 = dfs1.assign(s2=s2)
        dfs1 = dfs1.assign(T2=dfs2.loc[:,'T'])
        dfs1 = dfs1.assign(r=dfs1['T']-dfs1['T2']) 
        conditions = [dfs1['r']>5,dfs1['r']<-5]
        choices = [1,2]
        dfs1['vol']=np.select(conditions, choices, default=0)
        fdf.append(dfs1)
        print(i)
    fdf = pd.concat(fdf)
    fdf.to_csv(path_or_buf='/Users/casa/Documents/FF/pairsbyHourAvg.csv')
if __name__ == '__main__':
    main()