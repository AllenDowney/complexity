"""Written by Dan Kearney, Natalie Mattison, and Theodore Thompson
for Olin College Computational Modeling 2011."""

class Location:

    def __init__(self, x, y, init_sugar=0, max_sugar=1, sugar_growth_rate=0):
        '''A Location in the Sugarscape grid'''
        self.x = x
        self.y = y
        self.sugar_amt = init_sugar
        self.max_sugar = max_sugar
        self.sugar_growth_rate = sugar_growth_rate
        self.has_agent = False
        self.is_rich = False

    def set_sugar_amt(self, amount):
        '''sets sugar amount, not allowing too much'''
        if amount > self.max_sugar:
            self.sugar_amt = self.max_sugar
        else:
            self.sugar_amt = amount 
        return True
    
    def set_max_sugar(self, amount):
        '''resets maximum sugar allowed at the Location'''
        self.max_sugar = amount
        return True
    
    def get_max_sugar(self):
        '''returns maximum sugar allowed at the Location'''
        return self.max_sugar
        
    def get_sugar_amt(self):
        '''returns amount of Sugar at the Location'''
        return self.sugar_amt
        
    def set_sugar_growth_rate(self, amount):
        '''resets the sugar growth rate at the Location'''
        self.sugar_growth_rate = amount
        return True

    def decrease_sugar(self, amount):
        '''decrease the Location's sugar by some amount.
        Useful for when an agent eats sugar'''
        self.sugar_amt -= amount
        return True

    def regrow_sugar(self):
        '''increase sugar by one time step's worth.
        Useful for when the sugar regrows on its own'''
        self.sugar_amt += self.sugar_growth_rate
        if self.sugar_amt > self.max_sugar:
             self.sugar_amt = self.max_sugar
        return True

    def set_has_agent(self, has_agent):
        ''' update if the Location has an agent or not'''
        self.has_agent = has_agent
        return True

    def get_has_agent(self):
        ''' gets if the Location has an agent or not'''
        return self.has_agent

    def __str__(self):
        return "x: %d, y: %d, sugar: %d, max: %d, growth: %d, hasAgent: %s" %(self.x, self.y, self.sugar_amt, self.max_sugar, self.sugar_growth_rate, self.has_agent)
