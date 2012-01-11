"""Written by Dan Kearney, Natalie Mattison, and Theodore Thompson
for Olin College Computational Modeling 2011."""

from Location import Location
from Sugarscape import *
import random

class Agent(object):

    def __init__(self, xloc, yloc, vision, sugar_reserve, metabolism, sugarscape):
        '''a sugar-consuming agent on the Sugarscape'''
        self.vision = self.make_vision(vision)
        self.metabolism = self.make_metabolism(metabolism)
        self.sugar_reserve = sugar_reserve
        self.sugarscape = sugarscape
        self.location = self.sugarscape.get_location(xloc, yloc)
        self.location.set_has_agent(True)

    def make_vision(self, vision):
        '''generates random vision for agent'''
        vision = int(round(random.normalvariate(vision,2)))
        return vision if vision > 0 else 1
       
    def make_metabolism(self, metabolism):
        '''generates random metabolism for agent'''
        met = round(random.normalvariate(metabolism-1,1) + 1,2)
        return met if met >= 0 else .1

    def observe(self):
        '''returns the best Location that the agent should move to
        within its vision. If there's a tie, it picks randomly.'''
        nearby_locs = self.sugarscape.get_nearby_locations(self.vision, self.location)
        max_sugar = 0
        best_loc = [self.location]
        for location in nearby_locs:
            if location.sugar_amt > max_sugar and not location.get_has_agent():
                max_sugar = location.sugar_amt
                best_loc = [location]
            elif location.sugar_amt == max_sugar and not location.get_has_agent():
                best_loc.append(location)
        return random.choice(best_loc)

    def nextstep(self):
        '''figure out the next move, walk there, and metabolize sugar.'''
        self.walk(self.observe())
        self.sugar_reserve += self.location.sugar_amt
        self.location.set_sugar_amt(self.leave_behind())
        self.sugar_reserve -= self.metabolism
        if self.sugar_reserve <= 0 and self.sugarscape.timestamp > 1:
            self.die(self.location)

    def walk(self, location):
        '''move to the next spot'''
        self.location.set_has_agent(False)
        self.location = location
        self.location.set_has_agent(True)
        return True

    def die(self, location):
        '''agent is removed from sugarscape'''
        self.sugarscape.remove_agent(self)
        self.location.set_has_agent(False)
        return True

    def leave_behind(self):
        '''calculates how much sugar to leave behind'''
        if self.sugar_reserve < 0:
            return 0
        else:
            return abs(self.sugar_reserve* len(self.sugarscape.agents)/float(self.sugarscape.total_wealth+1))**1.1 / 5

    def set_sugar_reserve(self, amount):
        '''sets sugar reserve'''
        self.sugar_reserve = amount

    def get_vision(self):
        '''returns vision'''
        return self.vision

    def get_metabolism(self):
        '''returns metabolism'''
        return self.metabolism

    def get_location(self):
        '''returns the location the agent is at'''
        return self.location

    def get_sugar_reserve(self):
        '''returns sugar reserve'''
        return self.sugar_reserve

    def __str__(self):
        return "agent: sugar_reserve: %g, location: %d, %d, vision: %d, metabolism: %d" %(self.sugar_reserve, self.location.x, self.location.y, self.vision, self.metabolism)
