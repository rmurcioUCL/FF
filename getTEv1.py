import pandas as pd
from datetime import datetime as dt
from dateutil.rrule import rrule, DAILY
from datetime import timedelta 
import jpype
import sqlite3
import numpy as np
from StringIO import StringIO
from scipy.spatial import distance
from scipy.stats import spearmanr
from scipy.stats import energy_distance

conn = sqlite3.connect("/Users/casa/Documents/sqlite-tools-osx-x86-3260000/ff.db")

'''Generates the TE values for each pair of timeseries 
'''
def startVM():
    # Change location of jar to match yours:
        #jarLocation = "\Users\casa\Documents\FF\infodynamics-dist-1.5\infodynamics.jar"
        jarLocation ="\Library\Java\Extensions\infodynamics.jar"
        # Start the JVM (add the "-Xmx" option with say 1024M if you get crashes due to not enough memory space)
        jpype.startJVM(jpype.getDefaultJVMPath(), "-ea", "-Djava.class.path=" + jarLocation)

def main():

    df = pd.read_csv('/Users/casa/Documents/FF/pairsF.csv')
    dft = pd.read_csv('/Users/casa/Documents/FF/timestamps.csv')

    f1= open("/Users/casa/Documents/FF/teXYW.csv","w+")
    #f2= open("/Users/casa/Documents/FF/teYX.csv","w+")
    f3= open("/Users/casa/Documents/FF/teFW.csv","w+")
    lst1 = 's1,s2,te,timestamp,direction'
    lst3 = 's1,s2,distc,pearc,speac,te,direction,timestamp'
    f1.write("%s\n" % lst1)
    #f2.write("%s\n" % lst)
    f3.write("%s\n" % lst3)
    startVM()

            
        print(str(row['s1'])+','+str(row['s2']))
        for index1, row1 in dft.iterrows():
            a=dt.strptime(row1['timestamp'], "%d/%m/%Y").date()
            b=a+timedelta(days=1)
            
            sql='select location,(adjusted_local+counts_global) as total,timestamp from counts where location in ('+str(row['s1'])+','+str(row['s2'])+') and timestamp>=\''+a.strftime("%Y-%m-%d")+'\'' + \
                    ' and timestamp<\''+b.strftime("%Y-%m-%d")+'\''
            df1=pd.read_sql(sql,conn)
            if (df1.empty==False):
                i=df1.loc[df1['location'] == row['s1'], 'total'].tolist()
                j=df1.loc[df1['location'] == row['s2'], 'total'].tolist()

                if len(i)==len(j):                                
                    teCalcClass = jpype.JPackage("infodynamics.measures.continuous.kernel").TransferEntropyCalculatorKernel
                    teCalc = teCalcClass()
                    teCalc.setProperty("NORMALISE", "true") # Normalise the individual variables
                    teCalc.initialise(1, 0.5) # Use history length 1 (Schreiber k=1), kernel width of 0.5 normalised units
                    teCalc.setObservations(jpype.JArray(jpype.JDouble, 1)(i), jpype.JArray(jpype.JDouble, 1)(j))
                    localTEs=teCalc.computeAverageLocalOfObservations()
                    results=str(row['s1'])+","+str(row['s2'])+","+str(localTEs)+","+str(row1['timestamp'])+",1"
                    f1.write("%s\n" % str(results))
                    teCalc.initialise(1, 0.5) # Use history length 1 (Schreiber k=1), kernel width of 0.5 normalised unit  
                    teCalc.setObservations(jpype.JArray(jpype.JDouble, 1)(j), jpype.JArray(jpype.JDouble, 1)(i))
                    localTEs1=teCalc.computeAverageLocalOfObservations()
                    results=str(row['s1'])+","+str(row['s2'])+","+str(localTEs1)+","+str(row1['timestamp'])+",2"
                    f1.write("%s\n" % str(results))
                    if abs(localTEs-localTEs1) > 0.01:
                        if localTEs>localTEs1:
                            direction=1
                            te=localTEs
                        else:
                            direction=2
                            te=localTEs1
                    else:
                        direction=0
                        te=0
                    distc =  distance.correlation(i,j)
                    pearc =  np.corrcoef(i,j)[1,0]
                    speac =  spearmanr(i,j)
                    results = str(row['s1'])+","+str(row['s2'])+","+str(distc)+","+str(pearc)+","+str(speac.correlation) +","+ \
                    str(te)+","+str(direction)+","+str(row1['timestamp'])
                    f3.write("%s\n" % str(results))
    f1.close()
    #f2.close()
    f3.close()
    #df = pd.read_csv('/Users/casa/Documents/FF/teXY.csv')
    #df.to_sql('TEn',con=conn,if_exists='append',index=False)
    #df = pd.read_csv('/Users/casa/Documents/FF/teYX.csv')
    #df.to_sql('TEn',con=conn,if_exists='append',index=False)
    #df = pd.read_csv('/Users/casa/Documents/FF/teF.csv')
    #df.to_sql('TEf',con=conn,if_exists='append',index=False)

if __name__ == '__main__':
    main()