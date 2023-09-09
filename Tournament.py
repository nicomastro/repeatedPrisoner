from itertools import combinations
from random import shuffle
from dPrisoner import dPrisoner
from Prisoner import Prisoner
from randomPrisoner import randomPrisoner
from superPrisoner import superPrisoner
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
  def play_match(self, prisoner1, prisoner2, n_rounds = None):

    # Create instances of each prisoner
    p1 = prisoner1(window=5,p=0.5,buffer_init=10)
    p2 = prisoner2(window=5,p=0.5,buffer_init=10)

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
  def round_robin(self):

    # Create a list of all combinations of competing
    matches = list(combinations(range(len(self.competing)), 2))
    shuffle(matches)

    # Play all matches
    for match in matches:
      (score1, score2) = self.play_match(
        self.competing[match[0]],
        self.competing[match[1]])
      self.scores[match[0]] += score1
      self.scores[match[1]] += score2

def run():
  competing = [superPrisoner,randomPrisoner]
  a = Tournament(competing,1000)
  a.round_robin()
  print(a.scores)

  m=max(a.scores)
  winners=[]
  for i in range(len(competing)):
       if a.scores[i] == m:
         winners.extend([i])
  print("ganadores: ",winners)

run()
