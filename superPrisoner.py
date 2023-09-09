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
        self.k = 4 # Parametro de largo maximo del patron a buscar

    def pick_strategy(self):
        patron = self.__there_is_a_patron()
        if patron is None:
          # Aca va la estrategia si no hay patron
          return False
        else:
          # Nuestra prediccion es que La proxima jugada del rival va a ser patron[0]

          ### Rvisar si queremos hacer esa jugada
          return patron[0]


    def there_is_a_patron(self):
        res = None
        for i in range(1, self.k):
          res = self.__serch_patron_of_lenght(i)
          if res is not None:
            return res
        return res

    def __serch_patron_of_lenght(self, k):
      for i in range(0, k):
        patron = self.op_history[i:i+k]
        patron_fit = True
        for j in range(i, len(self.op_history), k):
          if not self.__is_included_in_start(patron, self.op_history[j:]):
            patron_fit = False
            break;
        if patron_fit:
          return patron
      
      return None

    def __is_included_in_start(self, x, xs):
      if len(xs) < len(x):
        return False

      res = True
      for i, e in enumerate(x):
        if e != xs[i]:
          return False

      return res


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