import scipy
import scipy.stats

import matplotlib
import matplotlib.pyplot as plt
import pandas as pd
class Distribution(object):
    
    def __init__(self,dist_names_list = []):
        self.dist_names = ['norm','lognorm','expon','powerlaw']
        self.dist_results = []
        self.params = {}
        
        self.DistributionName = ""
        self.PValue = 0
        self.Param = None
        
        self.isFitted = False
        
        
    def Fit(self, y):
        self.dist_results = []
        self.params = {}
        for dist_name in self.dist_names:
            dist = getattr(scipy.stats, dist_name)
            param = dist.fit(y)
            print(param)
            self.params[dist_name] = param
            #Applying the Kolmogorov-Smirnov test
            D, p = scipy.stats.kstest(y, dist_name, args=param)
            self.dist_results.append((dist_name,p))

        #select the best fitted distribution
        sel_dist,p = (max(self.dist_results,key=lambda item:item[1]))
        #store the name of the best fit and its p value
        self.DistributionName = sel_dist
        self.PValue = p
        
        self.isFitted = True
        return self.DistributionName,self.PValue
    
    def Random(self, n = 1):
        if self.isFitted:
            dist_name = self.DistributionName
            print(dist_name)
            param = self.params[dist_name]
            #initiate the scipy distribution
            dist = getattr(scipy.stats, dist_name)
            print(self.PValue)
            return dist.rvs(*param[:-2], loc=param[-2], scale=param[-1], size=n)
        else:
            raise ValueError('Must first run the Fit method.')
            
    def Plot(self,y):
        x = self.Random(n=len(y))
        plt.hist(x, alpha=0.5, label='Fitted')
        plt.hist(y, alpha=0.5, label='Actual')
        plt.legend(loc='upper right')
        plt.show()
    

from scipy.stats import lognorm
mu, sigma = 0.2951, 0.4816
r = lognorm.rvs(mu,sigma,size=5000)
r=[0.16666666666666666,
 0.16666666666666666,
 0.25,
 0.3333333333333333,
 0.5,
 0.5,
 0.5,
 0.5833333333333334,
 0.5833333333333334,
 0.6666666666666666,
 0.5833333333333334,
 0.75,
 0.75,
 0.6666666666666666,
 0.75,
 0.8333333333333334,
 0.9166666666666666,
 0.75,
 0.75,
 0.9166666666666666,
 0.6666666666666666,
 0.8333333333333334,
 0.75,
 0.9166666666666666,
 0.9166666666666666,
 0.9166666666666666,
 0.9166666666666666,
 0.8333333333333334,
 0.9166666666666666,
 0.9166666666666666,
 0.75,
 0.9166666666666666,
 1.0,
 0.9166666666666666,
 0.8333333333333334,
 0.9166666666666666,
 0.9166666666666666,
 1.0,
 0.9166666666666666,
 0.75,
 0.8333333333333334,
 0.9166666666666666,
 0.9166666666666666,
 1.0,
 0.9166666666666666,
 0.9166666666666666,
 1.0,
 1.0,
 1.0,
 1.0,
 0.9090909090909091,
 1.0,
 0.9090909090909091,
 1.0,
 1.0,
 0.9090909090909091,
 0.9090909090909091,
 0.9090909090909091,
 0.9090909090909091,
 1.0,
 1.0,
 1.0,
 1.0,
 1.0,
 1.0,
 1.0,
 1.0,
 1.0,
 1.0,
 1.0,
 1.0,
 1.0,
 1.0,
 0.9090909090909091,
 1.0,
 1.0,
 1.0,
 0.9090909090909091,
 0.9090909090909091,
 1.0,
 1.0,
 1.0,
 1.0,
 1.0,
 1.0,
 1.0,
 0.8888888888888888,
 1.0,
 1.0,
 1.0,
 0.8888888888888888,
 1.0,
 1.0,
 1.0,
 0.8888888888888888,
 1.0,
 0.8888888888888888,
 1.0,
 1.0]
#df = pd.read_csv('/Users/casa/Documents/FF/routeScorePlaw.csv')
df = pd.read_csv('/Users/casa/Documents/fsquare/freqpairs.csv')
dst = Distribution()
#dst.Fit(df['score'][1:])
#dst.Plot(df['score'][1:])
#dst.Fit(df['checks'][1:10])
#dst.Plot(df['checks'][1:10])
dst.Fit(r)
dst.Plot(r)