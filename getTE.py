#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Fri Jan 11 11:26:23 2019

@author: root
"""
import jpype
import pandas as pd
import sqlite3
from timeit import default_timer as timer


month='02'
conn = sqlite3.connect("/Users/casa/Documents/sqlite-tools-osx-x86-3260000/ff.db")
sql='select s1,s2,timestamp from results where month='+month
print(sql)
dfp = pd.read_sql(sql,conn)

def startVM():
    # Change location of jar to match yours:
        #jarLocation = "\Users\casa\Documents\FF\infodynamics-dist-1.5\infodynamics.jar"
        jarLocation ="\Library\Java\Extensions\infodynamics.jar"
        # Start the JVM (add the "-Xmx" option with say 1024M if you get crashes due to not enough memory space)
        jpype.startJVM(jpype.getDefaultJVMPath(), "-ea", "-Djava.class.path=" + jarLocation)

def main():
    startVM()
    #utility files
    #  f2= open("/Users/casa/Documents/FF/teResultsYX.csv","w+")
    f1= open("/Users/casa/Documents/FF/lteFeb1YX.csv","w+")
    f= open("/Users/casa/Documents/FF/lteFeb1JanXY.csv","w+")
    start = timer()
    id=1
    for name, row in dfp.iterrows():  
        s1=str(row["s1"])
        s2=str(row["s2"])
        print (id)
        d=str(row["timestamp"][0:2])
        sql='select location,total,timestamp from counts where (location='+s1+' or location='+s2+') and strftime(\'%m\',timestamp)=\''+month+'\''+ ' and strftime(\'%d\',timestamp)=\''+d+'\' and strftime(\'%M\',timestamp)=\''+d+'\' '
        df = pd.read_sql(sql,conn)
        i=df.loc[df['location'] == int(s1), 'total'].tolist()
        j=df.loc[df['location'] == int(s2), 'total'].tolist()
        if len(i)==len(j):               
            teCalcClass = jpype.JPackage("infodynamics.measures.continuous.kernel").TransferEntropyCalculatorKernel
            teCalc = teCalcClass()
            teCalc.setProperty("NORMALISE", "true") # Normalise the individual variables
            teCalc.initialise(1, 0.5) # Use history length 1 (Schreiber k=1), kernel width of 0.5 normalised units
            teCalc.setObservations(jpype.JArray(jpype.JDouble, 1)(i), jpype.JArray(jpype.JDouble, 1)(j))
            localTEs=teCalc.computeLocalOfPreviousObservations()
            results = str(localTEs)+","+str(row['timestamp'])+','+s1+','+s2
            f.write("%s\n" % str(results))
            teCalc.setObservations(jpype.JArray(jpype.JDouble, 1)(j), jpype.JArray(jpype.JDouble, 1)(i))
            localTEs=teCalc.computeLocalOfPreviousObservations()
            results = str(localTEs)+","+str(row['timestamp'])+','+s1+','+s2
            f1.write("%s\n" % str(results))
            id=id+1
    end = timer()
    print(end - start)
    f.close()
    f1.close()
    conn.close()
if __name__ == '__main__':
    main()