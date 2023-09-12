#import numpy as np
import random 
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
        self.name = "superPrisoner"
        self.budget = kwargs['budget'] # Cuanto puedo apostar (veces que arriesgo con C)
        self.window = kwargs['window']
        self.p = kwargs['p']
        self.buffer = kwargs['buffer_init']
        self.k = 4 # Parametro de largo maximo del patron a buscar
        self.streak = []
        self.streak_size = kwargs['streak_size'] # Longitud de cada segudilla [C....C X X X X]
        self.tolerance = kwargs['tolerance'] # Cuantas Cs seguidas juego para invitar al otro
        self.initiative = kwargs['initiative'] # Que tan propenso soy a intercalar Cs en la parte "alta" de la seguidilla
        self.update_tolerance = kwargs['update_tolerance']
        self.update_initiative = kwargs['update_initiative']
        self.op_initiative_low = 0.2
        self.op_initiative_high = 0.8


    def pick_strategy(self):
        patron = self.__there_is_a_patron()
        if patron is None or patron is not None: # Lo ignoro por ahora
            return self.__the_strategy()
        else:
          # Nuestra prediccion es que La proxima jugada del rival va a ser patron[0]
          ### Si hace patron, la mejora jugada siempre es D!
          return False 

    def __the_strategy(self):
        # Jugar Ds para aumentar el budget inicial
        if self.buffer > 0:
            self.buffer -= 1
            return False 
        else:
            if self.streak == []:                
                # Actualizar sensbilidad para apuestas
                #print(self.tolerance, self.initiative, self.budget)
                if len(self.op_history)  > self.streak_size:
                    op_initiative = sum(self.op_history[-self.window:])
                    if op_initiative < self.op_initiative_low*self.streak_size:
                        self.tolerance = int(min(self.tolerance*self.update_tolerance, self.streak_size))
                        self.initiative *= (2-self.update_initiative)
                    elif op_initiative > self.op_initiative_high*self.streak_size:
                        self.initiative *= self.update_initiative
                        self.tolerance = int(min((1/(self.update_tolerance))*self.tolerance, 1))

                # Generar la seguidilla de proximas jugadas (streak) 
                
                # Numpy
                #cs = np.repeat(True,max(min(self.tolerance, self.budget),0)) #Cs consecutivas
                #mixed_ds = np.logical_and(np.random.rand(max(self.streak_size - self.tolerance,0)) < self.initiative, self.budget > 0)
                #np.random.shuffle(mixed_ds)
                #new_streak = cs.tolist() + mixed_ds.tolist()
                #self.streak = new_streak if cs.size != 0 else [False]*10 # Si el oponente no juega Cs, generamos solo Ds
                
                # Python puro
                cs = [True] * max(min(self.tolerance, self.budget), 0) 
                mixed_ds = [random.random() < self.initiative and self.budget > 0 for _ in range(max(self.streak_size - self.tolerance, 0))]
                random.shuffle(mixed_ds)
                new_streak = cs + mixed_ds
                self.streak = new_streak if len(cs) != 0 else [False] * 10  


            return self.streak.pop()


    def __there_is_a_patron(self):
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
        self.budget -= -1 if earn < 0 else int(earn * self.p) 

    def __score(self, strategy1, strategy2):
        if strategy1 and strategy2:
          return 1
        elif not strategy1 and strategy2:
          return 2
        elif strategy1 and not strategy2:
          return -1
        else:
          return 0