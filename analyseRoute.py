import json
import os
from math import exp

outfile = '/Users/casa/Documents/FF/routeScoreFinal1.csv'
f = open(outfile,"w+")

    
def rankwords(fileContent):
    #fileContent = file.read()
    l = {}
    for word in fileContent.split():
        # make everything lowercase
        word = word.lower()
        
        # check for words in () or []
        if word.startswith('[') or word.startswith('('):
            word = word[1:]
        if word.endswith(']') or word.endswith(')'):
            word = word[:-1]
            
        # check for words that end with punctuation
        if word.endswith('.') or word.endswith(',') or word.endswith(';') or word.endswith(':'):
            word = word[:-1]
        # if word is in dictionary, increment the value
        # otherwise add the word to dictionary with value 1
        if word in l:
            l[word] += 1
        else:
            l[word] = 1
    for key, value in sorted(l.iteritems(), key=lambda (k,v): (v,k)):
        print '%s: %s' % (key, value)

def is_number(s):
    try:
        if float(s)!= 0.0:
            return True
    except ValueError:
        return False

def main():
    #results=""
    dmeters=0.0
    for root, dirs, files in os.walk("/Users/casa/Documents/FF/routes/"):  
        for filename in files:
            if not filename.startswith('.'):
                print(filename)
                distm=0
                with open('/Users/casa/Documents/FF/routes//'+filename) as json_file:  
                    data = json.load(json_file)
                    for p in data['routes']:
                        for r in p['legs']:
                            
                            for m in r['steps']:
                                weight=0
                                word = str(m['html_instructions'].encode('utf-8').strip()).lower()
                                word = word.replace('<b>','')
                                word = word.replace('</b>','')
                                word = word.replace('</div>','')
                                for i in range(len(word)):
                                    #if word.startswith('head',i) or word.startswith('toward',i) or word.startswith('continue',i) or word.startswith('follow',i) or word.startswith('straight',i)  or word.startswith('walk',i):
                                        #weight=weight+1
                                    if word.startswith('cross',i) or word.startswith('take',i):
                                        weight=weight+0.5
                                        break
                                    elif word.startswith('slight',i):
                                        weight=weight+1
                                        break
                                    elif word.startswith('turn',i):
                                        weight=weight+2
                                        break
                                    elif word.startswith('sharp',i):
                                        weight=weight+3
                                        break
                                    #elif word.startswith('upper',i):
                                        #weight=weight+4
                                        #break
                                    elif word.startswith('roundabout',i):
                                        weight=weight+4
                                        break
                                #print(m['distance']['text'].encode('utf-8').strip()[0:2])
                                if  is_number(m['distance']['text'].encode('utf-8').strip()[0:2]):
                                    dist=float(m['distance']['text'].encode('utf-8').strip()[0:2])
                                else:
                                    dist=float(m['distance']['text'].encode('utf-8').strip()[0:3])*1000   
                                #dmeters = dmeters + 1/(float(m['distance']['text'].encode('utf-8').strip()[0:shn])*weight)
                                #weight=weight*dist
                                distm=distm+dist
                                dmeters = dmeters + weight
                                #results = results + str(m['html_instructions'].encode('utf-8').strip())+" "+str(m['distance']['text'].encode('utf-8').strip())+" "
                #dmeters=dmeters/distm
                #dmeters=(dmeters**-1.25)*distm
                dmeters=dmeters*(1/distm)
                result = filename[:-5]+","+str(dmeters)+","+str(distm)
                dmeters=0.0
                distm=0
                f.write("%s\n" % result)                    
    f.close()
    #rankwords(results)

if __name__ == '__main__':
    main()