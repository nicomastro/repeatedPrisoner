"""
Prisoner superclass
"""
import random
class Prisoner():


    def __init__(self,**kwargs):
        self.N = self.C = self.ci = 0 # inicializo los totales
        self.eC = 0
        self.other_strategy = True # asumo (arbitrariamente) que el oponente arranca cooperando
        self.name="El Guasón" # nombre completo a imprimir

    """
    N : nro. total de rondas hasta ahora
    C : cantidad de veces que cooperé
    ci : nro. total de veces seguidas que cooperé
    eC : nro. total de veces que el (mismo) oponente cooperó
    """

#Esta función determina la estrategia a usar en cada ronda, pudiendo mirar cualquier
#atributo propio del objeto definido como jugador, en este caso ElGuason.

    def pick_strategy(self):
 
        if self.ci > 2: # si cooperé muchas veces seguidas
            if self.C/self.N > 0.5: # y cooperé muchas veces en total
                return False # disiente
            else:
                return True # coopera

        else:
            r = random.randint(0,9) # genera un número aleatorio de 0 a 9
            if r < 4: # esta proporción de veces
                return self.other_strategy # hago la última estrategia del oponente
            else:
                return True # coopero

#Esta función procesa los resultados, y se llama después de cada "partida". Los parámetros son dos booleanos:
#my_strategy = última estrategia usada por mí, other_strategy = última usada por el oponente.

#En este ejemplo, el prisionero sólo recordará la última estrategia del oponente. Si necesitan recordar más,
#pueden hacerlo, incluso armar el historial (en una lista, tupla, diccionario, etc.)

    def process_results(self, my_strategy, other_strategy):
        self.N += 1
        if my_strategy == True: # si la última vez cooperé, decido cooperar
            self.C += 1 # incremento la cantidad total de veces que cooperé
            self.ci += 1 # y la cantidad de veces seguidas que cooperé

        elif my_strategy == False: # en caso contrario
            self.ci = 0 # pongo en 0 la cantidad de veces seguidas que cooperé

        self.other_strategy = other_strategy # actualizo la última estrategia del oponente con la actual
        if other_strategy == True: # si el oponente la última vez cooperó
            self.eC += 1 # incremento la cantidad total de veces que cooperó
