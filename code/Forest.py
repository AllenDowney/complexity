""" Code example from Complexity and Computation, a book about
exploring complexity science with Python.  Available free from

http://greenteapress.com/complexity

Copyright 2011 Allen B. Downey.
Distributed under the GNU General Public License at gnu.org/licenses/gpl.html.
"""

import numpy
import scipy.ndimage

def random_array(n, p=0.2):
    rand = numpy.random.rand(n, n)
    array = numpy.int8(rand < p)
    return array

def vfunc(con, rand):
    # tree + neighbor on fire = burning
    if con >= 110:
        return 10

    # no tree, check for a new tree
    if con < 100:
        if rand < 0.1:
            return 1
        else:
            return 0
    
    # otherwise, tree + no neighbor on fire, check spark
    if rand < 0.1:
        return 10
    else:
        return 0

update_func = numpy.vectorize(vfunc, [numpy.int8])
    

class Forest(object):
    """Implements the Bak-Chen-Tang forest fire model.

    n:     the number of rows and columns
    """

    def __init__(self, n=100, p=0.2):
        """Attributes:
        n:      number of rows and columns
        array:  the numpy array that contains the data.
        """
        self.n = n
        self.array = random_array(n, p)
        self.weights = numpy.array([[1,1,1],
                                    [1,100,1],
                                    [1,1,1]])

    def loop(self, steps=1):
        """Executes the given number of time steps."""
        [self.step() for i in xrange(steps)]

    def step(self):
        """Executes one time step by computing the next row of the array."""
        con = scipy.ndimage.filters.convolve(self.array, 
                                             self.weights, mode='wrap')
        rand = numpy.random.rand(self.n, self.n)
        new = update_func(con, rand)
        self.array = new

    def get_array(self, start=0, end=None):
        """Gets a slice of columns from the CA, with slice indices
        (start, end).  Avoid copying if possible.
        """
        if start==0 and end==None:
            return self.array
        else:
            return self.array[:, start:end]


def main(script, n=10, *args):
    import CADrawer

    n = int(n)

    forest = Forest(n)

    forest.step()

    if 'eps' in args:
        drawer = CADrawer.EPSDrawer()
    elif 'pil' in args:
        drawer = CADrawer.PILDrawer()
    else:
        drawer = CADrawer.PyplotDrawer()

    drawer.draw(forest)
    drawer.show()


if __name__ == '__main__':
    import sys
    main(*sys.argv)
