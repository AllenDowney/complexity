""" Code example from Complexity and Computation, a book about
exploring complexity science with Python.  Available free from

http://greenteapress.com/complexity

Copyright 2011 Allen B. Downey.
Distributed under the GNU General Public License at gnu.org/licenses/gpl.html.

Safe use of eval() and exec() based on the discussion at
http://lybniz2.sourceforge.net/safeeval.html
"""

import glob
import math
import random
import os

safe_builtins = """
abs	divmod	staticmethod
all	enumerate	int	ord	str
any	isinstance	pow	sum
basestring	issubclass	print	super
bin	iter	property	tuple
bool	filter	len	range	type
bytearray	float	list   	unichr
callable	format	reduce	unicode
chr	frozenset	long	vars
classmethod	getattr	map	repr	xrange
cmp	max	reversed	zip
compile	hasattr	round
complex	hash	min	set	apply
delattr	help	next	setattr	buffer
dict	hex	object	slice	coerce
id	oct	sorted	intern
"""


class Player(object):
    """Represents a player.

    Attributes:
      filename: file the code was read from
      globs: global environment used to execute code
      locs: local environment used to execute code
    """
    def __init__(self, filename):
        self.filename = filename
        self.globs = self.make_globals()
        self.locs = self.make_locals()

    def make_globals(self):
        """Make the global environment."""
        t = [(k, getattr(__builtins__, k)) for k in safe_builtins.split()]
        safe_dict = dict(__builtins__=dict(t))

        safe_list = ['math', 'random']
        t = [(k, globals().get(k)) for k in safe_list]
        safe_dict.update(t)

        return safe_dict

    def make_locals(self):
        """Make the local environment."""
        return dict()


class Referee(object):
    def __init__(self, player_dir='.'):
        self.player_dir = player_dir

    def find_players(self, pattern='Player*.py'):
        """Find files that match pattern and read players.

        Returns a list of Player objects.
        """
        pattern = os.path.join(self.player_dir, pattern)
        filenames = glob.glob(pattern)
        filenames.sort()

        players = []
        for filename in filenames:
            player = Player(filename)
            players.append(player)

            execfile(filename, player.globs, player.locs)
            move = player.locs.get('move')

            if not move:
                print 'No move.'

        return players

    def run_tournament(self, players):
        """Run a tournament that runs each player against the others.

        Returns an array of scores.
        """
        for player1 in players:
            for player2 in players:
                self.run_head_to_head(player1, player2)

    def run_head_to_head(self, player1, player2, n=100):
        """Run players against each other n times.

        Returns a pair of scores.
        """
        moves1 = []
        moves2 = []
        for i in range(n):
            move1, move2 = self.one_round(player1, player2, moves1, moves2)
            print move1, move2
            moves1.append(move1)
            moves2.append(move2)

    def one_round(self, player1, player2, moves1, moves2):
        """Plays one round and updates the scores.

        Returns the players' moves.
        """
        print player1.filename, player2.filename
        move1 = self.call(player1, (moves1, moves2))
        move2 = self.call(player2, (moves2, moves1))
        return move1, move2

    def call(self, player, history):
        """Calls the player's move function and returns the result."""
        player.locs['history'] = history
        decision = eval('move(history)', player.globs, player.locs)
        return decision

def main(script, rule=30, n=100, *args):

    ref = Referee()
    players = ref.find_players()
    results = ref.run_tournament(players)


if __name__ == '__main__':
    import sys
    main(*sys.argv)
