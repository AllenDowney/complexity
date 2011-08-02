
"""

Code example from _Computational_Modeling_
http://greenteapress.com/compmod

Copyright 2008 Allen B. Downey.
Distributed under the GNU General Public License at gnu.org/licenses/gpl.html.

"""

import math
import random

from TurtleWorld import TurtleWorld, Turtle
import color_list


def ReadColors():
    """Reads color names from rgb.txt (which is where Tk gets them).

    Returns:
        list of strings
    """
    colors, rgbs = color_list.read_colors()
    names = colors.keys()

    # for some reason DebianRed causes an error
    names.remove('DebianRed')
    return names


class Highway(TurtleWorld):
    """A TurtleWorld with a one-dimensional lane that spirals down the canvas.
    
    Each Turtle has a position
    attribute, which gets projected onto the canvas by Highway.project.
    (rows) is the number of rows that spiral down the canvas.
    """
    def __init__(self):
        TurtleWorld.__init__(self)
        self.rows = 5.0
        self.delay = 0.01
        self.colors = ReadColors()

    def get_colors(self):
        return self.colors

    def get_length(self):
        """Return the total length of this highway."""
        return self.ca_width * self.rows

    def project(self, turtle):
        """Project (turtle) onto the highway.

        Maps position onto the canvas and setting its x and y attributes"""
        p = 1.0 * turtle.position % self.get_length()
        turtle.x = p % self.ca_width
        turtle.y = p / self.ca_width * self.ca_height / self.rows

    def align(self, turtle):
        """Aligns the turtle so it faces along the lane."""
        x = self.ca_width
        y = 1.0 * self.ca_height / self.rows
        angle = math.atan2(y, x)
        turtle.heading = angle * 180 / math.pi

    def step(self):
        TurtleWorld.step(self)
        
        total = 0.0
        for turtle in self.animals:
            total += turtle.speed

        print total / len(self.animals)


class Driver(Turtle):
    """A Turtle with a random position, speed and color."""
    def __init__(self, *args, **kwds):
        Turtle.__init__(self, *args, **kwds)
        self.delay = 0
        self.position = random.randrange(0, self.world.get_length())

        self.speed_limit = 10
        self.speed = random.randrange(5,10)

        colors = self.world.get_colors()
        self.color = random.choice(colors)

        self.world.align(self)
        self.world.project(self)
        self.redraw()

    def get_speed(self):
        return self.speed

    def accelerate(self, change):
        """Speeds up the Turtle by the given amount, within bounds."""
        self.speed += change
        if self.speed < 0:
            self.speed = 0

        if self.speed > self.speed_limit:
            self.speed = self.speed_limit

    def brake(self, change):
        """Slows down the Turtle by the given amount, within bounds."""
        self.accelerate(-change)

    def step(self):
        """Checks the distance to the next driver, adjusts speed, and moves."""
        dist = find_distance(self)

        # get acceleration, add some randomness
        change = get_acceleration(self, dist)

        # Turtles have limited acceleration
        if change > 2:
            change = 2
        self.accelerate(change)

        # if the current speed would cause a collision, jam on the brakes
        if self.speed > dist:
            self.speed = 0

        # move
        self.position += self.speed

        # redraw
        self.world.project(self)
        self.redraw()


def find_distance(turtle):
    """Finds the distance between this Turtle and the next."""
    dist = turtle.next.position - turtle.position

    # deal with wrap-around
    if dist < 0:
        dist += turtle.world.get_length()
    return dist


def make_drivers(n, driver=Driver):
    """Make drivers at random positions.

    Args:
        n: number of Drivers
        driver: constructor

    Returns:
        a list of Drivers.
    """
    t = []
    for i in range(n):
        turtle = driver()
        t.append((turtle.position, turtle))

    # link up the drivers so each has an attribute (next) that
    # refers to the driver in front
    t.sort()
    turtles = [t[1] for t in t]
    for i in range(n-1):
        turtles[i].next = turtles[i+1]
    turtles[-1].next = turtles[0]

    return turtles


def make_highway(n, driver=Driver):
    """Make the highway and drivers, then run the simulation.

    Args:
        n: number of Drivers
        driver: constructor
    """

    # create the highway
    world = Highway()
    world.canvas.clear_transforms()
    world.setup_run()
    
    # create (n) drivers
    make_drivers(n, driver)

    # start the simulation, then wait for user events
    world.run()
    world.mainloop()


def get_acceleration(turtle, dist):
    """Adjusts the speed of the Driver."""
    return 1

    
def main(script, n=100):
    n = int(n)
    make_highway(n)


if __name__ == '__main__':
    import sys
    main(*sys.argv)
