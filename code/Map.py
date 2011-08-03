""" Code example from Complexity and Computation, a book about
exploring complexity science with Python.  Available free from

http://greenteapress.com/complexity

Copyright 2011 Allen B. Downey.
Distributed under the GNU General Public License at gnu.org/licenses/gpl.html.
"""

import string


class LinearMap(list):
    """A simple implementation of a map using a list of tuples
    where each tuple is a key-value pair."""

    def add(self, k, v):
        """Add a new item that maps from key (k) to value (v).
        Assumes that they keys are unique."""
        self.append((k, v))

    def get(self, k):
        """Loop up the key (k) and return the corresponding value,
        or raise KeyError if the key is not found."""
        for key, val in self:
            if key == k:
                return val
        raise KeyError


class BetterMap(list):
    """A faster implementation of a map using a list of LinearMaps
    and the built-in function hash() to determine which LinearMap
    to put each key into."""

    def __init__(self, n=100):
        self.add_maps(n)
        
    def add_maps(self, n):
        """append (n) LinearMaps onto (self)"""
        for i in range(n):
            self.append(LinearMap())

    def find_map(self, k):
        """find the right LinearMap for key (k)"""
        index = hash(k) % len(self)
        return self[index]

    def add(self, k, v):
        """Add a new item to the appropriate LinearMap for key (k)"""
        m = self.find_map(k)
        m.add(k, v)

    def get(self, k):
        """Find the right LinearMap for key (k) and look up (k) in it"""
        m = self.find_map(k)
        return m.get(k)


class HashMap(object):
    """An implementation of a hashtable using a list of LinearMaps
    that grows so that the number of items never exceeds the number
    of LinearMaps.

    The amortized cost of add should be O(1) provided that the
    implementation of sum in resize is linear."""

    def __init__(self):
        """Start with 2 LinearMaps and 0 items"""
        self.map = BetterMap(2)
        self.num = 0

    def get(self, k):
        return self.map.get(k)

    def add(self, k, v):
        """resize the list if necessary and then add the new item."""
        if self.num == len(self.map):
            self.resize()

        self.map.add(k, v)
        self.num += 1

    def resize(self):
        """resize the list by collecting all the items into one big
        list, doubling the number of LinearMaps, and then re-adding
        all of the items."""
        new_map = BetterMap(self.num * 2)

        for m in self.map:
            for k, v in m:
                new_map.add(k, v)

        self.map = new_map

def main(script):
    m = HashMap()
    s = string.ascii_lowercase

    for k, v in enumerate(s):
        m.add(k, v)

    for k in range(len(s)):
        print k, m.get(k)

if __name__ == '__main__':
    import sys
    main(*sys.argv)
