""" Code example from Complexity and Computation, a book about
exploring complexity science with Python.  Available free from

http://greenteapress.com/complexity

Copyright 2011 Allen B. Downey.
Distributed under the GNU General Public License at gnu.org/licenses/gpl.html.
"""

import os
import matplotlib.pyplot as pyplot

def etime():
    """see how much user and system time this process has used
    so far and return the sum"""
    user, sys, chuser, chsys, real = os.times()
    return user+sys


def sum_plus(t, init):
    """Concatenates a list of lists into a single list using +="""
    total = init
    for x in t:
        total += x
    return total


def sum_extend(t, init):
    """Concatenates a list of lists into a single list using list.extend"""
    total = init
    for x in t:
        total.extend(x)
    return total


def sum_sum(t, init):
    """Concatenates a list of lists into a single list using sum"""
    return sum(t, init)


def test_func(f, n):
    """Tests the function (f) with a list of lists of length (n)
    and return the elapsed time."""
    t = [[1]] * n

    start = etime()
    f(t, [])
    end = etime()
    elapsed = end - start
    return elapsed


def test(name):
    """Test the given function with a range of values for n.

    Returns a list of ns and a list of run times.
    """
    # look up the string (name) and get the function object
    f = eval(name)

    # depending on which function we are testing, we need to
    # use a different order of magnitude for (n)
    d = dict(sum_sum=1000,
             sum_plus=100000,
             sum_extend=100000)
    factor = d[name]

    # test (f) over a range of values for (n)
    ns = []
    ts = []
    for i in range(2, 25):
        n = factor * i
        t = test_func(f, n)
        print n, t
        ns.append(n)
        ts.append(t)

    return ns, ts


def plot(ns, ts, label, color='blue', exp=1.0):
    tfit = fit(ns, ts, exp)
    pyplot.plot(ns, tfit, color='0.7', linewidth=2)
    pyplot.plot(ns, ts, label=label, color=color, linewidth=3)


def fit(ns, ts, exp=1.0, index=-1):
    """Fits a curve with the given exponent.

    Use the given index as a reference point, and scale all other
    points accordingly.
    """
    nref = ns[index]
    tref = ts[index]

    tfit = []
    for n in ns:
        ratio = float(n) / nref
        t = ratio**exp * tref
        tfit.append(t)

    return tfit


def save(root, exts=['eps', 'pdf']):
    for ext in exts:
        filename = '%s.%s' % (root, ext)
        print 'Writing', filename
        pyplot.savefig(filename)


def make_fig(funcs, scale='log', exp=1.0, filename=''):
    pyplot.clf()
    pyplot.xscale(scale)
    pyplot.yscale(scale)
    pyplot.title('')
    pyplot.xlabel('n')
    pyplot.ylabel('run time (s)')

    colors = ['blue', 'green', 'red']
    for func, color in zip(funcs, colors):
        data = test(func)
        plot(*data, label=func, color=color, exp=exp)

    pyplot.legend(loc=4)

    if filename:
        save(filename)
    else:
        pyplot.show()


def main(script):
    make_fig(['sum_extend', 'sum_plus'], exp=1.0, filename='listsum1')
    # make_fig(['sum_sum'], exp=2.0, filename='listsum2')


if __name__ == '__main__':
    import sys
    main(*sys.argv)
