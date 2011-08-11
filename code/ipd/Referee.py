""" Code example from Complexity and Computation, a book about
exploring complexity science with Python.  Available free from

http://greenteapress.com/complexity

Copyright 2011 Allen B. Downey.
Distributed under the GNU General Public License at gnu.org/licenses/gpl.html.
"""

import glob
import math
import random

class Referee(object):
    def __init__(self):
        pass

    def find_players(self):
        filenames = glob.glob('Player*.py')
        filenames.sort()

        players = []
        for filename in filenames:
            globs = dict(__builtins__=None)
            locs = dict()
            execfile(filename, globs, locs)
            player = locs.get('move')

            if player:
                player.name = filename
                player.globs = self.make_globals()
                player.locs = self.make_locals(player)
                players.append(player)

        return players

    def run_tournament(self, players):
        for player1 in players:
            for player2 in players:
                self.compete(player1, player2)

    def compete(self, player1, player2):
        print player1.name, player2.name
        history = ['history']
        self.call(player1, history)
        
    def call(self, player, history):
        player.locs['history'] = history
        print player.globs
        print player.locs
        # decision = eval('player(history)', player.globs, player.locs)
        decision = eval('player(history)', player.globs, player.locs)
        print decision

    def make_globals(self):

        builtins = dict(abs=abs, len=len)
        safe_dict = dict(__builtins__=builtins)

        safe_list = ['math', 'random']
        t = [(k, globals().get(k)) for k in safe_list]
        safe_dict.update(t)

        return safe_dict

    def make_locals(self, player):
        safe_list = ['player']

        safe_dict = dict()
        t = [(k, locals().get(k)) for k in safe_list]
        safe_dict.update(t)

        return safe_dict

def main(script, rule=30, n=100, *args):

    ref = Referee()
    players = ref.find_players()
    results = ref.run_tournament(players)


if __name__ == '__main__':
    import sys
    main(*sys.argv)
