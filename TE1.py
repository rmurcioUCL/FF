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
import numpy as np


conn = sqlite3.connect("/Users/casa/Documents/sqlite-tools-osx-x86-3260000/ff.db")
sql='select froml,tol,timew from distance where froml in (select location from counts where timestamp>=\'2017-01-01\' and timestamp<\'2017-02-01\') and tol in (select location from counts where timestamp>=\'2017-01-01\' and timestamp<\'2017-02-01\') and timew>=60 and timew<300;'
dfp = pd.read_sql(sql,conn)

def startVM():
    # Change location of jar to match yours:
        #jarLocation = "\Users\casa\Documents\FF\infodynamics-dist-1.5\infodynamics.jar"
        jarLocation ="\Library\Java\Extensions\infodynamics.jar"
        # Start the JVM (add the "-Xmx" option with say 1024M if you get crashes due to not enough memory space)
        jpype.startJVM(jpype.getDefaultJVMPath(), "-ea", "-Djava.class.path=" + jarLocation)

def validate(df,s1,s2):
    if len(df[df['location']==int(s1)]) == len(df[df['location']==int(s2)]):
        #v= df.loc[df['location'] == int(s1), 'total'].iloc[0] * df.loc[df['location'] == int(s2), 'total'].iloc[0] 
        i=df.loc[df['location'] == int(s1), 'total']
        j=df.loc[df['location'] == int(s2), 'total']
        v= [a*b for a,b in zip(i,j)]
        t=sum(x == 0 for x in v)
        if (t*100)/len(v)>80:
            return []
        else:
            results = s1+","+s2+","+str(np.corrcoef(i,j)[1,0])
            return results
    else:
        return []
       
    
def main():
    startVM()
    #utility files
    f2= open("/Users/casa/Documents/FF/teResultsYX.csv","w+")
    f1= open("/Users/casa/Documents/FF/resultsOct2.csv","w+")
    #f= open("/Users/casa/Documents/FF/resultsTEOct.csv","w+")

    start = timer()
    ids=1
    for name, row in dfp.iterrows():       
        a = date(2017, 1, 1)
        b = date(2017, 1, 31) 
        s1=str(row["froml"])
        s2=str(row["tol"])
        #print(s1+"-"+s2)
        for dt in rrule(DAILY, dtstart=a, until=b):
            c=dt+timedelta(days=1)
            sql='select location,total from counts where timestamp>=\''+dt.strftime("%Y-%m-%d")+'\''+' and timestamp<\''+c.strftime("%Y-%m-%d")+'\''+ \
            ' and (location='+s1+ ' or location='+s2+')'
            df=pd.read_sql(sql,conn)
            if (df.empty==False):        
                flag=validate(df,s1,s2)
                if flag:
                    flag=dt.strftime("%Y-%m-%d")+','+flag+","+str(row["timew"])+","+str(ids)
                    print(flag)
                    '''f1.write("%s\n" % str(flag))               
                    teCalcClass = jpype.JPackage("infodynamics.measures.continuous.kernel").TransferEntropyCalculatorKernel
                    teCalc = teCalcClass()
                    teCalc.setProperty("NORMALISE", "true") # Normalise the individual variables
                    teCalc.initialise(1, 0.5) # Use history length 1 (Schreiber k=1), kernel width of 0.5 normalised units
                    j=df[df.columns[0]].tolist()
                    k=df[df.columns[1]].tolist()
                    teCalc.setObservations(jpype.JArray(jpype.JDouble, 1)(j), jpype.JArray(jpype.JDouble, 1)(k))
                    localTEs=teCalc.computeLocalOfPreviousObservations()
                    results = str(localTEs)+","+str(ids)
                    f.write("%s\n" % str(results))'''
                    ids=ids+1
    end = timer()
    print(end - start) 
    #f.close()
    f1.close()
    conn.close()
if __name__ == '__main__':
    main()