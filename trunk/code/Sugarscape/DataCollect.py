"""Written by Dan Kearney, Natalie Mattison, and Theodore Thompson
for Olin College Computational Modeling 2011."""

import Sugarscape,Agent
import numpy

class DataCollect:
    
    def __init__(self,sugarscape):
        '''class for analyzing the sugarscape'''
        self.sugarscape=sugarscape
        self.wealths=[]
        self.Analyze()
        
    def Analyze(self):
        '''calculate characteristics of sugarscape'''
        for agent in self.sugarscape.agents:
            self.wealths.append(agent.sugar_reserve)
        self.sd=numpy.std(self.wealths)
        self.avg=numpy.average(self.wealths)
        self.med=numpy.median(self.wealths)
        self.total_wealth=sum(self.wealths)
        self.num_agents=len(self.sugarscape.agents)
        try:
            self.maximum = max(self.wealths)
            self.minimum = min(self.wealths)
        except:
            self.maximum = 0
            self.minimum = 0
        try:
            self.gini = self.calc_gini(self.wealths)
        except:
            self.gini = 0
        self.rnge = self.maximum - self.minimum
        self.bottom_quartile = self.calc_bottom_quartile(self.wealths)
        

    def Pack(self):
        '''return a packed list describing properties of the sugarscape'''
        return [self.sugarscape.tax_rate*100,self.sd,self.avg,self.med,self.maximum,self.minimum,self.rnge,self.total_wealth,self.gini, self.bottom_quartile]

    def calc_bottom_quartile(self, wealths):
        '''calculates the wealth of the 25th percentile'''
        sort_wealths=sorted(wealths)
        if len(sort_wealths)==0:
            return 0
        return sum(sort_wealths[:len(sort_wealths)/4])/(len(sort_wealths)/4.0) #average the bottom quartile

    def calc_gini(self, wealths):
        '''returns gini coefficient'''
        sort_wealths = sorted(wealths)  
        num_agents = len(sort_wealths)
        gini,count = 0,0
        for wealth in sort_wealths:
            gini += wealth * (num_agents - count) 
            count += 1
        gini /=  (num_agents*sum(sort_wealths))
        return num_agents**(-1) - 2*gini + 1

    def __str__(self):
        return "TAX RATE: " + str(self.sugarscape.tax_rate*100) + "%\n------\n  average: " + str(self.avg) + "\n  standard deviation: " + str(self.sd) + "\n  median: " + str(self.med) + "\n  maximum: " + str(self.maximum) + "\n  minimum: " + str(self.minimum) + "\n  range: " + str(self.rnge) + "\n  total wealth: " + str(self.total_wealth) + "\n  Number of agents: " + str(self.num_agents) + "\n  Gini: " + str(self.gini)

