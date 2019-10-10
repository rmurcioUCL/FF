# -*- coding: utf-8 -*-
"""
Created on Wed Nov 21 14:20:45 2018

@author: casa
"""

import jpype
import pandas as pd
import sqlite3
from sqlite3 import Error
from datetime import date
from dateutil.rrule import rrule, DAILY
from datetime import timedelta 
from timeit import default_timer as timer
import multiprocessing
from functools import partial



def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)
 
    return None

def startVM():
    # Change location of jar to match yours:
        #jarLocation = "\Users\casa\Documents\FF\infodynamics-dist-1.5\infodynamics.jar"
        jarLocation ="\Library\Java\Extensions\infodynamics.jar"
        # Start the JVM (add the "-Xmx" option with say 1024M if you get crashes due to not enough memory space)
        jpype.startJVM(jpype.getDefaultJVMPath(), "-ea", "-Djava.class.path=" + jarLocation)

def validate(s1,s2,dstr,tdate,d,conn):
    sql='select count(*) as total from counts where timestamp>=\''+dstr+'\''+' and timestamp<\''+tdate+'\''+' and location='+str(s1)
    df=pd.read_sql(sql,conn)
    sql='select count(*) as total from counts where timestamp>=\''+dstr+'\''+' and timestamp<\''+tdate+'\''+' and location='+str(s2)
    df1=pd.read_sql(sql,conn)
    if df['total'][0]>95 and df1['total'][0]>95:
        sql='select total from counts where timestamp>=\''+dstr+'\''+' and timestamp<\''+tdate+'\''+' and location='+str(s1)
        df=pd.read_sql(sql,conn)
        sql='select total from counts where timestamp>=\''+dstr+'\''+' and timestamp<\''+tdate+'\''+' and location='+str(s2)
        df1=pd.read_sql(sql,conn)
        if len(df)==len(df1):
            v=df*df1
        else:
            return []
        t=sum(x == 0 for x in v)
        if (t*100)/len(v)>80:
            return []
        else:
            results = dstr+","+str(s1)+","+str(s2)+","+str(df.corrwith(df1).total)+","+str(d)
            return results
            #print(df.corrwith(df1))
            #return 1
    else:
        return []
        
def checkzeros(s1,conn):
    sql='select strftime(\'%m\',timestamp),strftime(\'%d\',timestamp),strftime(\'%H\',timestamp) as H,sum(total) as total from counts where timestamp>=\'2017-09-11\' and timestamp<\'2017-09-12\' \
         and location='+s1+' group by strftime(\'%m\',timestamp),strftime(\'%d\',timestamp),strftime(\'%H\',timestamp);'
    df=pd.read_sql(sql,conn)
    i=0
    count=0
    while i<23:
        if df['total'][i]!=0:
            i=i+1
            while df['total'][i]==0 and i<23:
                i=i+1
                count=count+1
        else:
            i=i+1
    if count>2:
        return 0
    else:
        return 1
    
def main():
    database = "/Users/casa/Documents/sqlite-tools-osx-x86-3260000/ff.db"
    conn = create_connection(database)
    #Get sensors pairs that are less than 5 min walking distance from each other
    sql='select froml,tol,timew from distance where timew>=60 and timew<296;'
    dfp = pd.read_sql(sql,conn)
    startVM()
    #utility files
    #  f2= open("/Users/casa/Documents/FF/teResultsYX.csv","w+")
    f1= open("/Users/casa/Documents/FF/results.csv","w+")
    f= open("/Users/casa/Documents/FF/resultsTE.csv","w+")

    start = timer()

    for name, row in dfp.iterrows():
        ids=1
        a = date(2017, 4, 1)
        b = date(2017, 4, 2)
        for dt in rrule(DAILY, dtstart=a, until=b):
            c=dt+timedelta(days=1)

            flag=validate(row["froml"],row["tol"],dt.strftime("%Y-%m-%d"),c.strftime("%Y-%m-%d"),row["timew"],conn)
            if flag:
                flag=flag+","+str(ids)
                print(flag)
                f1.write("%s\n" % str(flag))               
                lst = '('+str(row["froml"])+','+str(row["tol"])+')'
                sql='select location,total from counts where location in ' +lst+ ' and timestamp>=\''+dt.strftime("%Y-%m-%d")+'\''+' and timestamp<\''+c.strftime("%Y-%m-%d")+'\''
                df = pd.read_sql(sql,conn)
                #if (df.empty==False):
                    #print(lst)
                    #a=df[df.location==row["froml"]].total.values.tolist()
                    #b=df[df.location==row["tol"]].total.values.tolist()         
                    #if a and b:
                #flag=checkzeros(str(row["froml"]),conn)
                #flag1=checkzeros(str(row["tol"]),conn)
                #flag=flag*flag1;
                #print(lst)
                teCalcClass = jpype.JPackage("infodynamics.measures.continuous.kernel").TransferEntropyCalculatorKernel
                teCalc = teCalcClass()
                teCalc.setProperty("NORMALISE", "true") # Normalise the individual variables
                teCalc.initialise(1, 0.5) # Use history length 1 (Schreiber k=1), kernel width of 0.5 normalised units
                j=df[df.columns[0]].tolist()
                k=df[df.columns[1]].tolist()
                teCalc.setObservations(jpype.JArray(jpype.JDouble, 1)(j), jpype.JArray(jpype.JDouble, 1)(k))
                # For copied source, should give something close to 1 bit:
                #result = teCalc.computeAverageLocalOfObservations()
                #print(result) 
                #f.write("\n" % result)
                localTEs=teCalc.computeLocalOfPreviousObservations()
                results = dt.strftime("%Y-%m-%d")+","+str(row["froml"])+","+str(row["tol"])+","+str(localTEs)+","+str(ids)
                f.write("%s\n" % str(results))
                ids=ids+1
                #teCalc.setObservations(jpype.JArray(jpype.JDouble, 1)(b), jpype.JArray(jpype.JDouble, 1)(a))
                #localTEs=teCalc.computeLocalOfPreviousObservations()
                #results = str(row["froml"])+","+str(row["tol"])+","+str(localTEs)
                #f2.write("%s\n" % str(results))               
                #if flag:
                #results = str(row["froml"])+","+str(row["tol"])+","+str(df.corr().iloc[1][0])+","+str(row["timew"])
                #print(results)

                #else:
                 #   f1.write("%s\n" % str(lst))
                #results = str(row["froml"])+","+str(row["tol"])+","+str(localTEs)
                #f1.write("%s\n" % str(results))
            #else:
                #f1.write("%s\n" % str(lst))
    end = timer()
    print(end - start) 
    f.close()
    f1.close()
    conn.close()
if __name__ == '__main__':
    main()