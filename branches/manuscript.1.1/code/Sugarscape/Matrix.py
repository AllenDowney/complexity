"""Written by Dan Kearney, Natalie Mattison, and Theodore Thompson
for Olin College Computational Modeling 2011."""

from numpy import array
from Location import Location

class Matrix:

    def __init__(self, length, width):
        '''contains a 2-D array of Locations.  On initializing, the Locations
        do not have any attributes besides column and row coordinates.
        Those can be set later, by the Sugarscape. '''
        self.array = array([[Location(x, y) for x in range(length+1)] for y in range(width+1)])
        self.length = length
        self.width = width

    def get_value(self, x, y):
        '''returns the Location object at an x,y coordinate in the Matrix.
        Useful for changing the Location object's attributes.
        We have no setter because there is no reason that the Location object 
        itself should ever change, only its attributes.'''
        return self.array[y, x]

    def __str__(self):
        retVal = ""
        for line in self.array:
            retVal = retVal + str(line) + "\n"
        return str(retVal)
