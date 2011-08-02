

"""

Code example from _Computational_Modeling_
http://greenteapress.com/compmod

Original code by Matt Aasted, modified by Allen Downey.

Based on Reynolds, "Flocks, Herds and Schools" and
Flake, "The Computational Beauty of Nature."

Copyright 2008 Allen B. Downey.
Distributed under the GNU General Public License at gnu.org/licenses/gpl.html.

"""

from visual import *
import numpy

# size of the boids
b_radius = 0.1
b_length = 0.3

# radii for sensing different rules
r_avoid = 0.3
r_center = 3.0
r_copy = 1.5

# viewing angle for different rules, in radians
a_avoid = 2*pi
a_center = 2
a_copy = 2

# weights for various rules
w_avoid = 4
w_center = 3
w_copy = 1
w_love = 2

# time step
dt = 0.1

def random_vector(a, b):
    """Create a vector with each element uniformly distributed in [a, b)."""
    t = [numpy.random.uniform(a,b) for i in range(3)]
    return vector(t)

def limit_vector(vect):
    """if the magnitude is greater than 1, set it to 1"""
    if vect.mag > 1:
        vect.mag = 1
    return vect

null_vector = vector(0,0,0)

class Boid(cone):
    """A Boid is a VPython cone with a velocity"""

    def __init__(self, radius=b_radius, length=b_length):
        pos = random_vector(-1, 1)
        self.vel = random_vector(-1, 1).norm()
        cone.__init__(self, pos=pos, radius=radius)
        self.axis = length * self.vel.norm()

    def get_neighbors(self, others, radius, angle):
        """return the list of neighbors that are within the given
        radius and angle."""
        boids = []
        for other in others:
            if other is self: continue
            offset = other.pos - self.pos
            
            # if not in range, skip it
            if offset.mag > radius: continue

            # if not within viewing angle, skip it
            if self.vel.diff_angle(offset) > angle: continue

            # otherwise add it to the list
            boids.append(other)
            
        return boids

    def avoid(self, others, carrot):
        """find the center of mass of all objects in range and
        return a vector in the opposite direction, with magnitude
        proportional to the inverse of the distance (up to a limit)"""
        others = others + [carrot]
        close = self.get_neighbors(others, r_avoid, a_avoid)
        t = [other.pos for other in close]
        if t:
            center = sum(t)/len(t)
            away = self.pos - center
            away.mag = r_avoid / away.mag
            return limit_vector(away)
        else:
            return null_vector


    def center(self, others):
        """find the center of mass of other boids in range and
        return a vector pointing toward it."""
        close = self.get_neighbors(others, r_center, a_center)
        t = [other.pos for other in close]
        if t:
            center = sum(t)/len(t)
            toward = vector(center - self.pos)
            return limit_vector(toward)
        else:
            return null_vector


    def copy(self, others):
        """return the average heading of other boids in range"""
        close = self.get_neighbors(others, r_copy, a_copy)
        t = [other.vel for other in close]
        if t:
            center = sum(t)/len(t)
            away = self.pos - center
            return limit_vector(away)
        else:
            return null_vector


    def love(self, carrot):
        """return a vector pointing toward the carrot"""
        toward = carrot.pos - self.pos
        return limit_vector(toward)
        

    def set_goal(self, boids, carrot):
        """set the goal to be the weighted sum of the goal vectors"""
        self.goal = (w_avoid * self.avoid(boids, carrot) + 
                     w_center * self.center(boids) +
                     w_copy * self.copy(boids) + 
                     w_love * self.love(carrot))
        self.goal.mag = 1
        
    def move(self, mu=0.1):
        """update the velocity, position and axis vectors.
        mu controls how fast the boids can turn (maneuverability)"""

        self.vel = (1-mu) * self.vel + mu * self.goal
        self.vel.mag = 1

        self.pos += dt * self.vel
        self.axis = b_length * self.vel.norm()
        

class World(object):
    def __init__(self, n=10):
        """create (n) Boids and one carrot.  (tracking) indicates
        whether the carrot follows the position of the mouse."""
        self.boids = [Boid() for i in range(n)]
        self.carrot = sphere(pos=(1,0,0), radius=0.1, color=(1,0,0))
        self.tracking = False
        
    def iterate(self):
        # move the boids
        for boid in self.boids:
            boid.set_goal(self.boids, self.carrot)
            boid.move()

        # mouse click toggles tracking
        if scene.mouse.clicked:
            scene.mouse.getclick()
            self.tracking = not self.tracking

        # if we're tracking, move the carrot
        if self.tracking:
            self.carrot.pos = scene.mouse.pos
    

n = 30
scene = display(title='Boids', width=800, height=600)
world = World(n)
scene.center = world.carrot.pos
scene.autoscale = False

while 1:
    # update the screen once per time step
    rate(1/dt)
    world.iterate();

