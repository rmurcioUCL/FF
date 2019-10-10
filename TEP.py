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
import multiprocessing as mp
from functools import partial

fn1= "/Users/casa/Documents/FF/results.csv"
fn= "/Users/casa/Documents/FF/resultsTE.csv"
conn = sqlite3.connect("/Users/casa/Documents/sqlite-tools-osx-x86-3260000/ff.db")

def create_connection(db_file):
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

def validate(s1,s2,dstr,tdate,d):
    sql='select location,total as total from counts where timestamp>=\''+dstr+'\''+' and timestamp<\''+tdate+'\''+' and location='+str(s1)+' and location='+str(s2)
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

def worker(s1,s2,t, q):
    ids=1
    a = date(2017, 4, 1)
    b = date(2017, 4, 2)
    for dt in rrule(DAILY, dtstart=a, until=b):
        c=dt+timedelta(days=1)
        #flag=validate(s1,s2,dt.strftime("%Y-%m-%d"),c.strftime("%Y-%m-%d"),t,conn)
        flag=1
        if flag:
            flag=flag+","+str(ids)
            print(flag)
            #f1.write("%s\n" % str(flag))               
            lst = '('+s1+','+s2+')'
            sql='select location,total from counts where location in ' +lst+ ' and timestamp>=\''+dt.strftime("%Y-%m-%d")+'\''+' and timestamp<\''+c.strftime("%Y-%m-%d")+'\''
            df = pd.read_sql(sql,conn)
            teCalcClass = jpype.JPackage("infodynamics.measures.continuous.kernel").TransferEntropyCalculatorKernel
            teCalc = teCalcClass()
            teCalc.setProperty("NORMALISE", "true") # Normalise the individual variables
            teCalc.initialise(1, 0.5) # Use history length 1 (Schreiber k=1), kernel width of 0.5 normalised units
            j=df[df.columns[0]].tolist()
            k=df[df.columns[1]].tolist()
            teCalc.setObservations(jpype.JArray(jpype.JDouble, 1)(j), jpype.JArray(jpype.JDouble, 1)(k))
            localTEs=teCalc.computeLocalOfPreviousObservations()
            results = str(ids)+","+s1+","+s2+","+str(localTEs)
            #f.write("%s\n" % str(results))
            ids=ids+1
            with open(fn1, 'rb') as f:
                size = len(fn1.read())
            #with open(fn, 'rb') as f:
                #size = len(f.read())
            q.put(flag)
            #q.put(results)
            return flag
    return flag

def listener(q):
    '''listens for messages on the q, writes to file. '''

    #f = open(fn, 'wb') 
    f1 = open(fn1, 'wb')
    while 1:
        m = q.get()
        if m == 'kill':
            #f.write('killed')
            f1.write('killed')
            break
        #f.write(str(m) + '\n')
        #f.flush()
        f1.write(str(m) + '\n')
        f1.flush()
    #f.close()
    f1.close()



def main():
    #database = "/Users/casa/Documents/sqlite-tools-osx-x86-3260000/ff.db"
    #conn = create_connection(database)
    #Get sensors pairs that are less than 5 min walking distance from each other
    sql='select froml,tol,timew from distance where timew>=60 and timew<61;'
    dfp = pd.read_sql(sql,conn)
    startVM()
    #utility files
    #  f2= open("/Users/casa/Documents/FF/teResultsYX.csv","w+")
    #f1= open("/Users/casa/Documents/FF/results.csv","w+")
    #f= open("/Users/casa/Documents/FF/resultsTE.csv","w+")

    manager = mp.Manager()
    q = manager.Queue()    
    pool = mp.Pool(mp.cpu_count() + 2)

    #put listener to work first
    watcher = pool.apply_async(listener, (q,))

    jobs = []
    for name, row in dfp.iterrows():
        s1=str(row["froml"])
        s2=str(row["tol"])
        t=str(row["timew"])
        print(s1)
        job = pool.apply_async(worker, (s1,s2,t, q))
        jobs.append(job)
        
    # collect results from the workers through the pool result queue
    for job in jobs: 
        job.get()

    #now we are done, kill the listener
    q.put('kill')
    pool.close()
    
 
if __name__ == '__main__':
    main()