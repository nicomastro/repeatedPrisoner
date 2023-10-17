import random

componentes = ['1', '2', '3']
torta = ""
# Glosario:
    # gusto: es un diccionario con claves {'1', '2', '3'}
    # torta: es una lista de caracteres {'1', '2', '3'}
    # corte: us una tupla de dos enteros (delimita dos cortes en la torta circular)
    # porcion: es un sub string del string de la torta circular
    # T: es el largo de la torta
    # N: es la cantidad de iteraciones que se repite el juego

class Juego:
    def __init__(self, T, N, jugador1, jugador2):
        self.T = T
        self.N = N
        self.jugador1 = jugador1
        self.jugador2 = jugador2

    def generar_torta(self):
        torta = ''
        for _ in self.T:
            torta += random.choice(componentes)
        
        return torta
    
    def jugar(self):
        utilidad1 = 0
        utilidad2 = 0
        for i in self.N:

            self.print_info()
        

    def print_info(self):
        print('Info')

class Jugador:
    def __init__(self, gustos):
        self.gustos = gustos
        
    # Dada una torta y un corte(tupla de dos enteros), devuelve las dos porciones que este define
    def cortar(self, torta, corte):
        i, j = corte
        porcion1 = torta[:i] + torta[j:]
        porcion2 = torta[i:j]
        return porcion1, porcion2

    # Dada una porcion devuelve la utilidad de la misma para el jugador
    def utilidad(self, porcion):
        return sum([self.gustos[c] for c in porcion])

    # Dada una torta devuelve un corte
    def cut(self, torta):
        # Esta funcion decide 
        pass

    # Dadas dos porciones devuelve la que mas utilidad le genera al jugador
    def choose(self, porcion1, porcion2):
        utilidad1 = self.utilidad(porcion1)
        utilidad2 = self.utilidad(porcion2)
        if utilidad1 >= utilidad2:
            return porcion1
        else:
            return porcion2
        
     
        
jugador1 = Jugador({'1': 1, '2': 1, '3': 1})
jugador2 = Jugador({'1': 1, '2': 2, '3': 0})
