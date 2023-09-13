#import numpy as np
import random 
"""
Prisoner superclass
"""
class superPrisoner():


    def __init__(self):
        self.op_history = []
        self.my_history = []
        self.name = "superPrisoner"
        self.budget = 0 # Cuanto puedo apostar (veces que arriesgo con C)
        self.window = 5
        self.p = 0.5
        self.buffer = 40
        self.k = 4 # Parametro de largo maximo del patron a buscar
        self.streak = []
        self.streak_size = 10 # Longitud de cada segudilla [C....C X X X X]
        self.tolerance = 8 # Cuantas Cs seguidas juego para invitar al otro
        self.initiative = 0.3 # Que tan propenso soy a intercalar Cs en la parte "alta" de la seguidilla
        self.update_tolerance = 2
        self.update_initiative = 0.9
        self.op_initiative_low = 0.2
        self.op_initiative_high = 0.8

    def pick_strategy(self):
        patron = self.__there_is_a_patron()
        if patron is None or patron is not None: # Lo ignoro por ahora
            return self.__the_strategy()
        else:
          # Si el rival juega un patron, no lo podemos invitar a hacer C
          # La mejora jugada siempre es D!
          return False 

    def __the_strategy(self):

        # Jugar Ds para aumentar el budget inicial
        if self.buffer > 0:
            self.buffer -= 1
            return False 
        else:
            if self.streak == []:      

                # Actualizar sensbilidad para apuestas (tolerance, initiative)
                if len(self.op_history)  > self.streak_size:
                    op_initiative = sum(self.op_history[-self.window:])
                    if op_initiative < self.op_initiative_low*self.streak_size:
                        self.tolerance = int(min(self.tolerance*self.update_tolerance, self.streak_size))
                        self.initiative *= (2-self.update_initiative)
                    elif op_initiative > self.op_initiative_high*self.streak_size:
                        self.initiative *= self.update_initiative
                        self.tolerance = int(min((1/(self.update_tolerance))*self.tolerance, 1))

                # Generar la seguidilla de proximas jugadas (streak)
                # Cada seguidilla comienza con tantas Cs como indica tolerance
                # Luego llenamos con, mayormente, Ds hasta alcanzar streak_size
                # Dentro de esta última parte, generar algunas Cs para generar algo de ruido
                # Una initiative mayor admite una secuencia más impura de Ds

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