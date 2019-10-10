import pandas as pd
import numpy as np
import sqlite3
from sqlite3 import Error
import operator
from datetime import date
from dateutil.rrule import rrule, DAILY
from datetime import timedelta 


conn = sqlite3.connect("/Users/casa/Documents/sqlite-tools-osx-x86-3260000/ff.db")
#sql='select TEavgwd1.*,TEavgwd2.* from TEavgwd1,TEavgwd2 where   TEavgwd1.s1=TEavgwd2.s1 and TEavgwd1.s2=TEavgwd2.s2 and TEavgwd1.month=TEavgwd2.month;'


def flow(s1,s2):
    #s1 = mydata.loc[1,'t1_1':'t1_288']
    #s2 = mydata.loc[2,'t2_1':'t2_288']
    mydata = [0]*288

    for i in range(0,288):
        if s1[s1.columns[i]].values[0]<=0 and s2[s2.columns[i]].values[0]<=0:
            mydata[i]=0
        elif s1[s1.columns[i]].values[0]<=0:
             mydata[i]=2
        elif s2[s2.columns[i]].values[0]<=0:
             mydata[i]=1
        elif abs(s1[s1.columns[i]].values[0]-s2[s2.columns[i]].values[0])>=0.02:
            if s1[s1.columns[i]].values[0]>s2[s2.columns[i]].values[0]:
                mydata[i]=1
            else:
                mydata[i]=2         
        else:
            mydata[i]=3           
    '''if s1.iloc[i]<=0 and s2.iloc[i]<=0:
        mydata[i]=0
    elif s1.iloc[i]<=0:
        mydata[i]=2
    elif s2.iloc[i]<=0:
        mydata[i]=1
    elif abs(s1.iloc[i]-s2.iloc[i])>=0.02:
        if s1.iloc[i]>s2.iloc[i]:
            mydata[i]=1
        else:
            mydata[i]=2
    else:
        mydata[i]=3'''
    return mydata


def groupbyHour(mydata):
    agglist = [-1]*24
    c=0
   
    for i in range(0,278,12):
        s0=mydata[i:i+12].count(0)
        s1=mydata[i:i+12].count(1)
        s2=mydata[i:i+12].count(2)
        s3=mydata[i:i+12].count(3)
        stats = {'0':s0,'1':s1,'2':s2,'3':s3}
        sorted_x = sorted(stats.items(), key=operator.itemgetter(1),reverse=True)
        values = [i[1] for i in sorted_x]
        nkeys = [i[0] for i in sorted_x]
        if values[1:] == values[:-1]:
            agglist[c]=0
        elif values[0]==values[1] and values[1]==values[2]:
            agglist[c]=0
        elif values[0]==values[1]:
            agglist[c]=0
        else:
            agglist[c]=int(nkeys[0])

        c=c+1

    return agglist

def main():
    #for j in range(2,12):
    
    #df = pd.read_csv('/Users/casa/Documents/FF/TEwd'+str(j)+'.csv')
    df = pd.read_csv('/Users/casa/Documents/FF/locpairs.csv')

    outfile = '/Users/casa/Documents/FF/flowd.csv'
    outfile1 = '/Users/casa/Documents/FF/flowdh.csv'
    f1 = open(outfile,"w+")
    f2 = open(outfile1,"w+")
    lst = 's1,s2,timestamp,dweek,month,t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11,t12,t13,t14,t15,t16,t17,t18,t19,t20,t21,t22,t23,t24,t25,t26,t27,t28,t29,t30,t31,' + \
    't32,t33,t34,t35,t36,t37,t38,t39,t40,t41,t42,t43,t44,t45,t46,t47,t48,t49,t50,t51,t52,t53,t54,t55,t56,t57,t58,t59,t60,t61,' + \
    't62,t63,t64,t65,t66,t67,t68,t69,t70,t71,t72,t73,t74,t75,t76,t77,t78,t79,t80,t81,t82,t83,t84,t85,t86,t87,t88,t89,t90,t91,t92,' + \
    't93,t94,t95,t96,t97,t98,t99,t100,t101,t102,t103,t104,t105,t106,t107,t108,t109,t110,t111,t112,t113,t114,t115,t116,t117,t118,t119,' + \
    't120,t121,t122,t123,t124,t125,t126,t127,t128,t129,t130,t131,t132,t133,t134,t135,t136,t137,t138,t139,t140,t141,t142,t143,t144,t145,' + \
    't146,t147,t148,t149,t150,t151,t152,t153,t154,t155,t156,t157,t158,t159,t160,t161,t162,t163,t164,t165,t166,t167,t168,t169,t170,t171,' + \
    't172,t173,t174,t175,t176,t177,t178,t179,t180,t181,t182,t183,t184,t185,t186,t187,t188,t189,t190,t191,t192,t193,t194,t195,t196,t197,' + \
    't198,t199,t200,t201,t202,t203,t204,t205,t206,t207,t208,t209,t210,t211,t212,t213,t214,t215,t216,t217,t218,t219,t220,t221,t222,t223,' + \
    't224,t225,t226,t227,t228,t229,t230,t231,t232,t233,t234,t235,t236,t237,t238,t239,t240,t241,t242,t243,t244,t245,t246,t247,t248,t249,' + \
    't250,t251,t252,t253,t254,t255,t256,t257,t258,t259,t260,t261,t262,t263,t264,t265,t266,t267,t268,t269,t270,t271,t272,t273,t274,t275,' + \
    't276,t277,t278,t279,t280,t281,t282,t283,t284,t285,t286,t287,t288'
    lsth = 's1,s2,timestamp,dweek,month,t1,t2,t3,t4,t5,t6,t7,t8,t9,t10,t11,t12,t13,t14,t15,t16,t17,t18,t19,t20,t21,t22,t23,t24'
    f1.write("%s\n" % lst)
    f2.write("%s\n" % lsth)
    for i in range(0,df.shape[0]):
        s1 = df.loc[i,'s1']
        s2 = df.loc[i,'s2']
        print(str(s1)+'-'+str(s2))
        for w in range(1,13):
            print(w)
            if w==1 or w==3 or w==5 or w==7 or w==8 or w==10 or w==12:
                di=31
            elif w==2:
                di=28
            else:
                di=30
            a = date(2017, w, 1)
            b = date(2017, w, di)
            #for name, row in df.iterrows():       
            #s1 = df.loc[i,'t1_1':'t1_288']
            #s2 = df.loc[i,'t2_1':'t2_288']
            #s1 = df.iloc[i,3:291]
            #s2 = df.iloc[i,294:582]
            for dt in rrule(DAILY, dtstart=a, until=b):
                #c=dt+timedelta(days=1)
                sql='select * from TE where s1='+str(s1)+' and s2='+str(s2)+' and timestamp=\''+dt.strftime("%Y-%m-%d")+'\''
                dfq = pd.read_sql(sql,conn)
                if (dfq.empty==False):
                    #if s1==45 and s2==43:
                        #print(dt.strftime("%Y-%m-%d"))
                    i=dfq.loc[dfq['direction'] == 1, 't1':'t288']
                    j=dfq.loc[dfq['direction'] == 2, 't1':'t288']
                    if len(i)==len(j):
                        results = flow(i,j)
                        rgroup = groupbyHour(results)
                        results=str(results).replace("[","")
                        results=str(results).replace("]","")
                        results=str(dfq[dfq.columns[289]].values[0])+","+str(dfq[dfq.columns[290]].values[0])+","+str(dfq[dfq.columns[288]].values[0])+","+str(dfq[dfq.columns[292]].values[0])+","+str(dfq[dfq.columns[293]].values[0])+","+results
                        f1.write("%s\n" % str(results))
                        rgroup=str(rgroup).replace("[","")
                        rgroup=str(rgroup).replace("]","")
                        rgroup=str(dfq[dfq.columns[289]].values[0])+","+str(dfq[dfq.columns[290]].values[0])+","+str(dfq[dfq.columns[288]].values[0])+","+str(dfq[dfq.columns[292]].values[0])+","+str(dfq[dfq.columns[293]].values[0])+","+rgroup
                        f2.write("%s\n" % str(rgroup))
    f1.close()
    f2.close()
    df1 = pd.read_csv('/Users/casa/Documents/FF/flowd.csv')
    df1.to_sql('flowd',con=conn,if_exists='append',index=False)
    df1 = pd.read_csv('/Users/casa/Documents/FF/flowdh.csv')
    df1.to_sql('flowdh',con=conn,if_exists='append',index=False)


if __name__ == '__main__':
    main()
