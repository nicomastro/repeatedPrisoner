import numpy as np
"""
Prisoner superclass
"""
class randomPrisoner():

    """
    Constructor. Called once at the start of each match.
    If needed, override this method to initialize any 
    auxiliary data you want to use to determine your 
    Prisoner's strategy. This data will persist between
    rounds of a match but not between matches.
    """
    def __init__(self):
        pass
    
  
    def pick_strategy(self):
        return np.random.rand() >= 0.5
    
    def process_results(self, my_strategy, other_strategy):
        pass
