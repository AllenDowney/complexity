"""Written by Dan Kearney, Natalie Mattison, and Theodore Thompson
for Olin College Computational Modeling 2011."""

from Sugarscape import *

class Government:

    def __init__(self, tax_rate, sugarscape):
        '''collects and redistributes sugar'''
        self.tax_rate = tax_rate
        self.sugarscape = sugarscape
        self.collective = 0

    def collect_taxes(self):
        '''takes sugar from all agents'''
        for agent in self.sugarscape.agents:
            taken = self.tax_rate*agent.get_sugar_reserve()
            self.collective += taken
            agent.set_sugar_reserve(agent.get_sugar_reserve() - taken)
        return True

    def redistribute(self):
        '''redistributes sugar to the agents'''
        try: tax_return = self.collective/len(self.sugarscape.agents)
        except: tax_return = 0
        for agent in self.sugarscape.agents:
            agent.set_sugar_reserve(agent.get_sugar_reserve() + tax_return)
            self.collective -= tax_return
        return int(self.collective) == 0
    
    def tax(self):
        '''wrapper for taxation and redistribution'''
        self.collect_taxes()
        self.redistribute()
    
    def __str__(self):
        return 'government object'






