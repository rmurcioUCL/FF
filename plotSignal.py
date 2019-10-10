# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
import sqlite3
from sqlite3 import Error

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect("/Users/casa/Documents/sqlite-tools-osx-x86-3260000/ff.db")
        return conn
    except Error as e:
        print(e)
 
    return None

def main():
    database = "/Users/casa/Documents/sqlite-tools-osx-x86-3260000/ff.db"
        # create a database connection
    conn = create_connection(database)
    '''lst = '(117,800,112,144,358,831,801,875,832,116,145,114,146,113,829,802,115)'
    colsn = ['117','800','112','144','358','831','801','875','832','116','145','114','146','113','829','802','115']'''
    '''lst = '(117,112,144,116,145,114,146,113,115)'
    colsn = ['117','112','144','116','145','114','146','113','115']'''
    lst = '(84,2)'
    colsn = ['84','2']
    
    #sql='select location,strftime(\'%H\',timestamp) as H,sum(total) as total from counts where location in '+lst+' and timestamp>=\'2017-01-06\' and timestamp<\'2017-01-07\' group  by location,strftime(\'%H\',timestamp) order by location,strftime(\'%H\',timestamp)'
    #sql='select location,total from counts where location in ' +lst+ ' and timestamp>=\'2017-01-10\' and timestamp<\'2017-01-11\';'
    sql='select location,strftime(\'%H\',timestamp) as H,avg(total) as total from counts where location in '+lst+' and dweek>6 and \
       (timestamp>=\'2017-01-01\' and timestamp<\'2018-01-01\') group by location,strftime(\'%H\',timestamp),strftime(\'%H\',timestamp);'
    #sql='select location,strftime(\'%H\',timestamp) as H,avg(total) as total from counts where location in '+lst+' and dweek<6 and  \
     #   (timestamp>=\'2017-03-01\' and timestamp<\'2017-04-01\') group by location,strftime(\'%H\',timestamp);'
    print (sql)
    df = pd.read_sql(sql,conn)
    #print(df.corr())
    tdf = pd.DataFrame([], columns=colsn) 
    for s in colsn:
        n=float(s)
        '''print(n)'''
        v=df[df.location==n].total.values
        tdf[s]=v
             #  tdf=tdf[tdf['341']!=0]
           # tdf=tdf[tdf['439']!=0]
          #  tdf=tdf.iloc[83:215]
    ''' del df['dweek'] '''
    '''styles=['y^-','g+-','y^-','go-','ys-','gv-','y<-','g>-','y1-','g2-','y3-','g4-','yD-','gd-','yh-','gH-','yx-','g*-','y|-']'''
    styles=['ys-','go-']
    #tdf[tdf['902']!=0].plot(legend=True,style=styles,linewidth=3)
    
    ''' ax=df.plot(legend=True,style='ro-') '''
    tdf.plot(legend=False,style=styles,linewidth=3,figsize=(35.5, 10.5),fontsize=20,xticks=range(0,24,1))
    ax = plt.axes()
    ax.grid( axis='y')
   # ax.xaxis.set_major_locator(plt.MaxNLocator(23))
    conn.close() 
    fig = matplotlib.pyplot.gcf()
    fig.legend(loc='upper right', bbox_to_anchor=(0.9, 0.88),prop={'size': 25})
    #fig.suptitle('FF Signal Monday - December', fontsize=40)  
    '''fig.set_size_inches(18.5, 10.5)'''
    fig.set_size_inches(35.5, 10.5)
    plt.show()
    #fig.savefig('/Users/casa/Documents/FF/84_2.png', dpi=200)
    
if __name__ == '__main__':  
    main()