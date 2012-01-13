"""Molly Grossman, Mandy Korpusik, Philip Loh"""

"""Definitions
world = whole population
player = each player
boldness = constant of probability for cheating
vengefulness = constant of probability for punishing
fitness = measurement of fitness"""

import sys, random, math

"""Constant World-wide variables"""
R = 3   #Reward from cheating
P = 9  #Punishment
C = 2  #Cost of punishing
D = 1  #Damage from each offense
MAXBV = 7.0 #must be power of 2, less 1

if int(math.log((MAXBV + 1), 2)) != math.log((MAXBV + 1), 2):
    raise ValueError("MAXBV MUST BE A FLOAT AND A POWER OF 2, LESS 1")

class Stats(object):
    def __init__(self):
        self.stableBV = []
        
gameStats = Stats()


class Player(object):
    def __init__(self, idNum, b, v):
        self.idNum = idNum
        self.boldness = b
        self.vengefulness = v
        self.fitness = 0
        return

    def __str__(self):
        return "id {0:2} boldness {1:.2f} vengefulness {2:.2f} fitness {3:3}".format(self.idNum, self.boldness, self.vengefulness, self.fitness)

    def update(self, deltaHealth):
        self.fitness += deltaHealth
        return

    def clone(self):
        return Player(self.idNum, self.boldness, self.vengefulness)

    def getBoldnessInt(self):
        return self.boldness

    def getBoldness(self):
        return self.boldness / MAXBV

    def getVengefulnessInt(self):
        return self.vengefulness

    def getVengefulness(self):
        return self.vengefulness / MAXBV

    def getHealth(self):
        return self.fitness

    def setBoldness(self, b):
        self.boldness = int(b)
        return

    def setVengefulness(self, v):
        self.vengefulness = int(v)
        return

    def resetHealth(self):
        self.fitness = 0
        return

class World(set):
    def __init__(self, N = 20):
        """begins World with 100 Persons by default"""
        self.population = 20
        for idNum in range(N):
            """random values near half"""
            b0 = random.normalvariate(MAXBV/2, 0.5)
            b0 = int(b0) if b0 - int(b0) < 0.5 else int(b0) + 1
            b = min(int(MAXBV), max(0, b0))
                        
            v0 = random.normalvariate(MAXBV/2, 0.5)
            v0 = int(v0) if v0 - int(v0) < 0.5 else int(v0) + 1
            v = min(int(MAXBV), max(0, v0))
            
            self.add(Player(idNum, b, v))
        return

    def __str__(self):
        hMean, hStDev = self.healthMeanStDev()
        bMean, vMean = self.bvMean()
        return "boldness {0:.2f} vengefulness {1:.2f} h {2:3}".format(bMean, vMean, hMean)

    def printDetails(self):
        s = ""
        for person in self:
            s += "\t" + str(person) + "\n"
        print s 

    def clone_update(self, persons):
        for person in persons:
            self.add(person.clone())
        return

    def _gameCheat(self, pbs):
        """first game: cheatORnot"""
        cheaters = set()
        for person in self:
            if person.getBoldness() >= pbs:
                person.update(R + D) # Reward plus what would be taken out as damage because we levy damage on everyone as a shortcut
                cheaters.add(person)
        for person in self:
            person.update(-len(cheaters) * D)
        return cheaters

    def _gamePunish(self, pbs, cheaters):
        """second game: punishORnot"""
        for cheater in cheaters:
            for observer in self - set([cheater]):
                if(slt(pbs) and slt(observer.getVengefulness())):
                    observer.update(-C) # Cost of punishing
                    cheater.update(-P) # Punishment
        return

    def gameSteps(self, steps=4):
        """each step has two games: cheatORnot and punishORnot; default 4 steps"""
        for step in range(steps):
            pbs = random.random() # probability of being seen (same for each person in the given round)
            cheaters = self._gameCheat(pbs)
            self._gamePunish(pbs, cheaters)
        return

    def _healthMean(self):
        """returns mean fitness in world"""
        healthSum = 0.0
        for person in self:
            healthSum += person.getHealth()
        return healthSum / len(self)
    
    def _healthStDev(self, hMean):
        """returns std deviation of fitness in world"""
        healthStD = 0.0
        for person in self:
            healthStD += (person.getHealth() - hMean) ** 2
        return (((1.0 / len(self)) * healthStD) ** 0.5)

    def bvMean(self):
        """returns mean boldness, vengefulness in world"""
        bSum = 0.0
        vSum = 0.0
        for person in self:
            bSum += person.getBoldness()
            vSum += person.getVengefulness()
        return bSum / len(self), vSum / len(self)

    def healthMeanStDev(self):
        """returns tuple(mean, std deviation of fitness in world)"""
        hMean = self._healthMean()
        return (hMean, self._healthStDev(hMean))

    def mutate(self):
        """at every generation, mutate based on prob"""
        """translate boldness and vengefulness into an n-bit binary number (which is why MAXBV is a power of 2 less 1)
        each mutation will involve the flipping of one bit"""
        p_mutation = 0.01
        for person in self:
            xorstr = ''
            power = int(MAXBV + 1)                      # power is the power of two analog for MAXBV
            vengefulness = person.getVengefulnessInt()  # vengefulness in int
            boldness = person.getBoldnessInt()          # boldness in int
            numBits = 2 * int(math.log(power, 2))       # power really needs to be a power of 2, safeguarding it not being a power of two, we ceil the log2
            for i in range(numBits):
                xorstr += str(int(slt(p_mutation)))
            xorstr = int(xorstr, 2)
            valsToXor = vengefulness + (boldness * power)
            newVals = xorstr ^ valsToXor
            person.setBoldness(int(newVals / 8))
            person.setVengefulness(int(newVals % 8))
        return
    
    def repopulate(self):
        """at every generation, repopulate"""
        mu, sigma = self.healthMeanStDev()
        newWorld = World()
        newWorld.clear()
        for person in self:
            health = person.getHealth()
            if health >= (mu - sigma):
                person.resetHealth()
                newWorld.add(person)
            if health >= (mu + sigma):
                newWorld.add(person.clone())
        if len(newWorld) < self.population:
            newWorld.clone_update(random.sample(self, self.population - len(newWorld)))
        elif len(newWorld) > self.population:
            newWorld.difference_update(random.sample(newWorld, len(newWorld) - self.population))
        assert(len(newWorld) == self.population)
        self.clear()
        self.update(newWorld)
        return

def slt(prob):
    """set less than"""
    return (random.random() < prob)

def plotStableBV(show=True):
    import matplotlib.pyplot as pyplot
    
    stableB, stableV = zip(*gameStats.stableBV)
    pyplot.scatter(stableB, stableV, alpha=0.7, label="B, V after 300 Generations")
    pyplot.title("Boldness, Vengefulness after 300 Generations")
    pyplot.xlabel("Boldness")
    pyplot.ylabel("Vengefulness")
    pyplot.axis([-0.1, 1.1, -0.1, 1.1])
    if show: pyplot.show()
    return

def runReplicate(trials=100):
    goodB = 0
    print "R {0} P {1} C {2} D {3}".format(R, P, C, D)
    for trial in range(trials):
        world = World()
        sys.stdout.write('.')
        
        for generation in range(300):
            world.gameSteps()
            world.mutate()
            world.repopulate()

        gameStats.stableBV.append(world.bvMean())
        goodB += 1 if world.bvMean()[0] <= 0.4 else 0

    sys.stdout.write('\n')
    
    return goodB/float(trials)

def main(script, *args):
    p = runReplicate()
    print "Probability of good outcome", p
    plotStableBV()
    return

if __name__ == "__main__":
    main(*sys.argv)
