""" Code example from Complexity and Computation, a book about
exploring complexity science with Python.  Available free from

http://greenteapress.com/complexity

Copyright 2011 Allen B. Downey.
Distributed under the GNU General Public License at gnu.org/licenses/gpl.html.
"""

from CA import CA
import CADrawer

def figure1(rule=18, n=64):
    ca = CA(rule, n)
    ca.start_single()
    ca.loop(n-1)
    drawer = CADrawer.PyplotDrawer()
    drawer.draw(ca)
    drawer.show()

    drawer.draw(ca)
    drawer.save('rule18.png')
    


def main(script, rule=30, n=100, *args):

    figure1()
    return

    rule = int(rule)
    n = int(n)

    ca = CA(rule, n)

    if 'random' in args:
        ca.start_random()
    else:
        ca.start_single()

    ca.loop(n-1)

    if 'eps' in args:
        drawer = CADrawer.EPSDrawer()
    elif 'pil' in args:
        drawer = CADrawer.PILDrawer()
    else:
        drawer = CADrawer.PyplotDrawer()

    if 'trim' in args:
        drawer.draw(ca, start=n/2, end=3*n/2+1)
    else:
        drawer.draw(ca)

    drawer.show()
    drawer.save()


if __name__ == '__main__':
    import sys
    main(*sys.argv)
