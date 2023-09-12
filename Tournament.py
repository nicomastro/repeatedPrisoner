from itertools import combinations
from random import shuffle
from dPrisoner import dPrisoner
from Prisoner import Prisoner
from randomPrisoner import randomPrisoner
from superPrisoner import superPrisoner
from ElGuason import ElGuason
import numpy as np
"""
Prisoners' dilemma tournament
"""
class Tournament():

    """
    Initialize the tournament

    Parameters
    ----------
    competing: list of competing Prisoner subclasses
    n_rounds: rounds per match
    """
    def __init__(self, competing, n_rounds):
        self.competing = competing
        self.scores = len(competing)*[0]
        self.n_rounds = n_rounds

    """
    Score a single round

    Parameters
    ----------
    strategy1: bool
    First Prisoner's strategy

    strategy2: bool
    Second Prisoner's strategy

    Returns
    -------
    (score1, score2): (int, int)
    (3,3) if both cooperate,
    (1,1) if both defect, and
    (5,0) or (0,5) if one cooperates and one defects
    """
    def score(self, strategy1, strategy2):

        if strategy1 and strategy2:
          return (1, 1)
        elif not strategy1 and strategy2:
          return (2, -1)
        elif strategy1 and not strategy2:
          return (-1, 2)
        else:
              return (0, 0)

    """
    Play a single match

    Parameters
    ----------
    prisoner1: subclass of Prisoner
    First prisoner competing in the match

    prisoner2: subclass of Prisoner
    Second prisoner competing in the match

    n_rounds: int, optional
    Number of rounds in the match. If no value is
    provided, the number of rounds defaults to
    the default value for the tournament.

    Returns
    -------
    (int, int): scores for prisoner1 and prisoner2
        """
    def play_match(self, prisoner1, prisoner2, params,n_rounds = None,):

        # Create instances of each prisoner

        p1 = prisoner1(budget=params['budget'],window=params['window'],
                       p=params['p'],buffer_init=params['buffer_init'],k=4, 
                       streak_size=params['streak_size'],tolerance=params['tolerance'],
                       initiative=params['initiative'],
                       update_tolerance=params['update_tolerance'],
                       update_initiative=params['update_initiative'],
                       op_initiative_low=0.2,op_initiative_high=0.8)
        p2 = prisoner2()

        # Initialize scores
        score1 = 0
        score2 = 0

        # Play all rounds
        if not n_rounds:
          n_rounds = self.n_rounds
        for n in range(n_rounds):
          strategy1 = p1.pick_strategy()
          strategy2 = p2.pick_strategy()
          scores = self.score(strategy1, strategy2)
          score1 += scores[0]
          score2 += scores[1]
          p1.process_results(strategy1, strategy2)
          p2.process_results(strategy2, strategy1)

        # Return scores
        return (score1, score2)

    """
     Play a round robin
    """
    def round_robin(self,params):

        # Create a list of all combinations of competing
        matches = list(combinations(range(len(self.competing)), 2))
        shuffle(matches)

        # Play all matches
        for match in matches:
          (score1, score2) = self.play_match(
            self.competing[match[0]],
            self.competing[match[1]],
            params)
          self.scores[match[0]] += score1
          self.scores[match[1]] += score2

def run(params):
    competing = [superPrisoner,ElGuason]
    a = Tournament(competing,300)
    a.round_robin(params)
    #print(a.scores)
    m=max(a.scores)
    winners=[]
    for i in range(len(competing)):
         if a.scores[i] == m:
           winners.extend([i])
    #print("ganadores: ",winners)
    return winners, a.scores[0]

# asumo partidas de 300 rondas en promedio

scores = []
strategy = []
results = []
for budget in [0,25,125,300]: # mas grande, más agresivo
  for window in [5,10,20,40]: # ventana para iniciativa oponente, no debería ser tan grande
    print(budget, window)
    for p in [1,0.5]: # 1 mete toda la gancia al budget, 0.5 mete 1 cuando gana 2 unicamente
        for buffer_init in [10,20,40,80,160]: # mas grande más conservador
            for streak_size in [5,10,20,40]:
                for tolerance in [1,2,4,8]:
                    for initiative in [0.1,0.15,0.3]:
                        for update_tolerance in [1.2, 2]:
                            for update_initiative in [0.99,0.9, 0.8]:
                                params ={'budget':budget,'window': window,'p' : p,
                                         'buffer_init': buffer_init,'streak_size': streak_size,
                                         'tolerance': tolerance, 'initiative': initiative,
                                         'update_tolerance': update_tolerance, 
                                         'update_initiative': update_initiative}
                                winners, score = run(params)
                                scores.append(-score)
                                strategy.append(params)
                                results.append(winners[0] == 0)
ix = np.argsort(scores)
top_10 = np.array(strategy)[ix][:10]
print(top_10, -1*np.sort(scores)[:10], np.array(results)[ix])




