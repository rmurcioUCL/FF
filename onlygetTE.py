import pandas as pd
from datetime import date
from dateutil.rrule import rrule, DAILY
from datetime import timedelta 
import jpype
import sqlite3
import numpy as np
from StringIO import StringIO

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
    df = pd.read_csv('/Users/casa/Documents/FF/ .csv')
    f1= open("/Users/casa/Documents/FF/lteJanXY.csv","w+")
    f2= open("/Users/casa/Documents/FF/lteJanYX.csv","w+")
    lst = 't1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11,t12,t13,t14,t15,t16,t17,t18,t19,t20,t21,t22,t23,t24,t25,t26,t27,t28,t29,t30,t31,' + \
        't32,t33,t34,t35,t36,t37,t38,t39,t40,t41,t42,t43,t44,t45,t46,t47,t48,t49,t50,t51,t52,t53,t54,t55,t56,t57,t58,t59,t60,t61,' + \
        't62,t63,t64,t65,t66,t67,t68,t69,t70,t71,t72,t73,t74,t75,t76,t77,t78,t79,t80,t81,t82,t83,t84,t85,t86,t87,t88,t89,t90,t91,t92,' + \
        't93,t94,t95,t96,t97,t98,t99,t100,t101,t102,t103,t104,t105,t106,t107,t108,t109,t110,t111,t112,t113,t114,t115,t116,t117,t118,t119,' + \
        't120,t121,t122,t123,t124,t125,t126,t127,t128,t129,t130,t131,t132,t133,t134,t135,t136,t137,t138,t139,t140,t141,t142,t143,t144,t145,' + \
        't146,t147,t148,t149,t150,t151,t152,t153,t154,t155,t156,t157,t158,t159,t160,t161,t162,t163,t164,t165,t166,t167,t168,t169,t170,t171,' + \
        't172,t173,t174,t175,t176,t177,t178,t179,t180,t181,t182,t183,t184,t185,t186,t187,t188,t189,t190,t191,t192,t193,t194,t195,t196,t197,' + \
        't198,t199,t200,t201,t202,t203,t204,t205,t206,t207,t208,t209,t210,t211,t212,t213,t214,t215,t216,t217,t218,t219,t220,t221,t222,t223,' + \
        't224,t225,t226,t227,t228,t229,t230,t231,t232,t233,t234,t235,t236,t237,t238,t239,t240,t241,t242,t243,t244,t245,t246,t247,t248,t249,' + \
        't250,t251,t252,t253,t254,t255,t256,t257,t258,t259,t260,t261,t262,t263,t264,t265,t266,t267,t268,t269,t270,t271,t272,t273,t274,t275,' + \
        't276,t277,t278,t279,t280,t281,t282,t283,t284,t285,t286,t287,t288,timestamp,s1,s2,direction'
    f1.write("%s\n" % lst)
    f2.write("%s\n" % lst)
    startVM()
    for i in range(0,df.shape[0]):
        s1 = df.loc[i,'s1']
        s2 = df.loc[i,'s2']
        print(str(s1)+'-'+str(s2))
        a = date(2017, 9, 1)
        b = date(2017, 9, 30)

        for dt in rrule(DAILY, dtstart=a, until=b):
            c=dt+timedelta(days=1)
            sql='select location,total,timestamp from counts where location in ('+str(s1)+','+str(s2)+') and timestamp>=\''+dt.strftime("%Y-%m-%d")+'\'' + \
                ' and timestamp<\''+c.strftime("%Y-%m-%d")+'\''
            
            df1=pd.read_sql(sql,conn)
            if (df1.empty==False):
                i=df1.loc[df1['location'] == int(s1), 'total'].tolist()
                j=df1.loc[df1['location'] == int(s2), 'total'].tolist()
                if len(i)==len(j):                                
                    teCalcClass = jpype.JPackage("infodynamics.measures.continuous.kernel").TransferEntropyCalculatorKernel
                    teCalc = teCalcClass()
                    teCalc.setProperty("NORMALISE", "true") # Normalise the individual variables
                    teCalc.initialise(1, 0.5) # Use history length 1 (Schreiber k=1), kernel width of 0.5 normalised units
                    #j=df1[df1.columns[0]].tolist()
                    #k=df1[df1.columns[1]].tolist()
                    teCalc.setObservations(jpype.JArray(jpype.JDouble, 1)(i), jpype.JArray(jpype.JDouble, 1)(j))
                    localTEs=teCalc.computeLocalOfPreviousObservations()
                    results = str(localTEs)+","+str(dt.strftime("%Y-%m-%d"))+","+str(s1)+","+str(s2)+",1"
                    results=results.replace("(","")
                    results=results.replace(")","")
                    f1.write("%s\n" % str(results))
                    teCalc.setObservations(jpype.JArray(jpype.JDouble, 1)(j), jpype.JArray(jpype.JDouble, 1)(i))
                    localTEs=teCalc.computeLocalOfPreviousObservations()
                    results = str(localTEs)+","+str(dt.strftime("%Y-%m-%d"))+","+str(s1)+","+str(s2)+",2"
                    results=results.replace("(","")
                    results=results.replace(")","")
                    f2.write("%s\n" % str(results))
    f1.close()
    f2.close()
    df = pd.read_csv('/Users/casa/Documents/FF/lteJanXY.csv')
    df.to_sql('TE',con=conn,if_exists='append',index=False)
    df = pd.read_csv('/Users/casa/Documents/FF/lteJanYX.csv')
    df.to_sql('TE',con=conn,if_exists='append',index=False)

if __name__ == '__main__':
    main()