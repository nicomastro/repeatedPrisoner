import numpy as np
"""
Prisoner superclass
"""
class superPrisoner():

    """
    Constructor. Called once at the start of each match.
    If needed, override this method to initialize any 
    auxiliary data you want to use to determine your 
    Prisoner's strategy. This data will persist between
    rounds of a match but not between matches.
    """
    def __init__(self, **kwargs):
        self.op_history = []
        self.my_history = []
        self.budget = 0
        self.window = kwargs['window']
        self.p = kwargs['p']
        self.init_buffer = kwargs['buffer_init']
  
    def pick_strategy(self):
        return False
    
    def process_results(self, my_strategy, other_strategy):
        self.op_history.append(other_strategy)
        self.my_history.append(my_strategy)
        earn  = self.__score(my_strategy, other_strategy)
        self.budget += earn * self.p

    def __score(self, strategy1, strategy2):
        if strategy1 and strategy2:
          return 1
        elif not strategy1 and strategy2:
          return 2
        elif strategy1 and not strategy2:
          return -1
        else:
          return 0
            
