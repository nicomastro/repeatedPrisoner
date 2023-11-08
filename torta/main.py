import random
import numpy as np
import sys

componentes = ['1', '2', '3']
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
        self.score1 = []
        self.score2 = []
        self.perfect_score1 = []
        self.perfect_score2 = []
        self.cut_sizes = []
        self.perfect_sizes = []

    def generar_torta(self):
        torta = ''
        for _ in range(self.T):
            torta += random.choice(componentes)
        
        return torta
    
    def jugar(self):
        utilidad1 = 0
        utilidad2 = 0
        cut_sizes = []
        for i in range(self.N):
            torta = self.generar_torta()

            corte = self.jugador1.cut(torta, self.jugador2)
            corte_perfecto = self.jugador1.perfect_cut(torta, self.jugador2)

            porcion1, porcion2 = Jugador.cortar(torta, corte)
            porcion1_perf, porcion2_perf = Jugador.cortar(torta, corte_perfecto)
         
            porcion_j2, porcion_j1 = self.jugador2.choose(porcion1, porcion2)
            porcion_j2_perf, porcion_j1_perf = self.jugador2.choose(porcion1_perf, porcion2_perf)


            self.perfect_sizes.append(len(porcion_j1_perf))
            self.cut_sizes.append(len(porcion_j1))
            #print("", porcion1_perf)

            self.score1.append(self.jugador1.utilidad(porcion_j1))
            self.score2.append(self.jugador2.utilidad(porcion_j2))

            self.perfect_score1.append(self.jugador1.utilidad(porcion_j1_perf))
            self.perfect_score2.append(self.jugador2.utilidad(porcion_j2_perf))
            
            #print(f"Iteracion: {i+1}")
            self.print_info("Algoritmo Heuristico: ", self.score1[-1], self.score2[-1])
            self.print_info("Algoritmo Perfecto: ", self.perfect_score1[-1], self.perfect_score2[-1])
            print("")

        self.print_info("Utilidad acumulada:", np.sum(self.score1), np.sum(self.score2))
        print("Perfectness", np.sum(self.score1)/np.sum(self.perfect_score1))

    def print_info(self, titulo, utilidad_j1, utilidad_j2):
        ### TODO: Completar bien esta funcion
        print(titulo)
        print(f'   Jugador 1: {utilidad_j1}')
        print(f'   Jugador 2: {utilidad_j2}')

class Jugador:

    # Dada una torta y un corte(tupla de dos enteros), devuelve las dos porciones que este define
    @staticmethod
    def cortar(torta, corte):
        i, j = corte
        porcion1 = torta[:i] + torta[j:]
        porcion2 = torta[i:j]
        return porcion1, porcion2

    @staticmethod
    def normalizar_gustos(gustos):
        suma = gustos["1"] + gustos["2"] + gustos["3"]
        gustos["1"] = gustos["1"] / suma
        gustos["2"] = gustos["2"] / suma
        gustos["3"] = gustos["3"] / suma
        return gustos

    def __init__(self, gustos, T):
        self.gustos = Jugador.normalizar_gustos(gustos)
        #self.gustos = gustos
        self.porcentaje_bin = 1/min(T, 128)
        self.T = T

    # Dada una porcion devuelve la utilidad de la misma para el jugador
    def utilidad(self, porcion):
        return sum([self.gustos[c] for c in porcion])

    def obtener_bins(self, torta, p_bins,start=0):
        bin_1, bin_2, bin_3 = [0], [0], [0]
        bin_size = round(len(torta)*p_bins)
        i = 0
        for i in range(len(torta)):
            i += 1
            if i > bin_size:
                i = 0
                start += bin_size
                bin_1.append(0)
                bin_2.append(0)
                bin_3.append(0)

            if torta[(start+i) % bin_size] == "1":
                bin_1[-1] += 1
            elif torta[(start+i) % bin_size] == "2":
                bin_2[-1] += 1
            elif torta[(start+i) % bin_size] == "3":
                bin_3[-1] += 1

        return bin_1, bin_2, bin_3

    def degustar_bins(self, bin_1, bin_2, bin_3):
        bin = []
        g = self.gustos
        for b1, b2, b3 in zip(bin_1, bin_2, bin_3):
            bin.append(g["1"]*b1 + g["2"]*b2 + g["3"]*b3)

        return bin

    def obtener_indices_del_bin_maximo(self, torta, bin, p_bins,start=0):
        maximo = max(bin)
        argmax = bin.index(maximo)
        bin_size = round(len(torta)*p_bins)
        return (start + bin_size*argmax, start + bin_size*(argmax+1))
        
    def encontrar_mejores_indices_en(self, torta, indices_maximo_bin, rival):
        mejor_temp = (0, 1)
        mejor_utilidad = 0
        for i in range(indices_maximo_bin[0], indices_maximo_bin[1]):
            for j in range(i+1, indices_maximo_bin[1]):
                corte1, corte2 = self.cortar(torta, (i, j))
                porcion_j2, porcion_j1 = jugador2.choose(corte1, corte2)
                if self.utilidad(porcion_j1) > mejor_utilidad:
                    mejor_temp = (i,j)
                    mejor_utilidad = self.utilidad(porcion_j1)
                
        return mejor_temp

    # Dada una torta y el rival devuelve un corte. La pienso asumiendo correlación negativa
    def cut(self, torta, jugador2):
        # Hago los bins y me fijo todos los posibles cortes en el mejor rango de bins
        ps = [(2**i)*self.porcentaje_bin for i in range(np.log2(1/self.porcentaje_bin).astype(int))]
        mejor_temp = (0, 1)
        mejor_utilidad = 0
        for p in ps:
            # Randomizar el X0 desde donde se toma la partición
            N_OFFSETS = 10
            for start in np.random.choice(len(torta), N_OFFSETS):
                bin_1, bin_2, bin_3 = self.obtener_bins(torta,p,start)
                bin = self.degustar_bins(bin_1, bin_2, bin_3)
                i, j = self.obtener_indices_del_bin_maximo(torta, bin,p,start)
                
                # No busco todos los subcortes en esta region, porque deberían ser peor?
                corte1, corte2 = self.cortar(torta, (i, j))
                porcion_j2, porcion_j1 = jugador2.choose(corte1, corte2)
                if self.utilidad(porcion_j1) > mejor_utilidad:
                    mejor_temp = (i,j)
                    mejor_utilidad = self.utilidad(porcion_j1)

        start, end = mejor_temp
        for k in range(end+1, end+N_OFFSETS):
            if k >= self.T:
                break
            corte1, corte2 = self.cortar(torta, (start, k))
            porcion_j2, porcion_j1 = jugador2.choose(corte1, corte2)
            if self.utilidad(porcion_j1) > mejor_utilidad:
                mejor_temp = (start,k)
                mejor_utilidad = self.utilidad(porcion_j1)

        for k in range(start-N_OFFSETS,start-1):
            if k <= 0:
                break 
            corte1, corte2 = self.cortar(torta, (k, end))
            porcion_j2, porcion_j1 = jugador2.choose(corte1, corte2)
            if self.utilidad(porcion_j1) > mejor_utilidad:
                mejor_temp = (k,end)
                mejor_utilidad = self.utilidad(porcion_j1)

        #print("Best:", mejor_temp[1], mejor_temp[0])
        return mejor_temp

    # con T = 1024 ya no tarda tiempo despreciable (en mi humilde notebook)
    def perfect_cut(self, torta, jugador2):
        mejor_temp = (0, 1)
        mejor_utilidad = 0
        for i in range(0, len(torta)-1):
            for j in range(i+1, len(torta)):
                corte1, corte2 = self.cortar(torta, (i, j))
                porcion_j2, porcion_j1 = jugador2.choose(corte1, corte2)
                if self.utilidad(porcion_j1) > mejor_utilidad:
                    mejor_temp = (i,j)
                    mejor_utilidad = self.utilidad(porcion_j1)

        return mejor_temp

    # Dadas dos porciones devuelve la que mas utilidad le genera al jugador
    def choose(self, porcion1, porcion2):
        utilidad1 = self.utilidad(porcion1)
        utilidad2 = self.utilidad(porcion2)
        if utilidad1 >= utilidad2:
            return porcion1, porcion2
        else:
            return porcion2, porcion1

def print_usage():
    print("Modo de uso: ./main.py T N")
    print("     T = Largo de la torta")
    print("     N = Cantidad de iteraciones")
    

if __name__ == "__main__":
    # Modificar estas varibles para alterar los gustos de cada jugador
    gustos_jugador1 = {'1': 0, '2': 10, '3': 10} 
    gustos_jugador2 = {'1': 1000, '2': 0, '3': 0}

    try:
        T = int(sys.argv[1])
        N = int(sys.argv[2])
    except Exception:
        print("Parametros incorrectos")
        print_usage()
        exit(1)
    
    jugador1 = Jugador(gustos_jugador1, T)
    jugador2 = Jugador(gustos_jugador2, T)
    juego = Juego(T, N, jugador1, jugador2)
    juego.jugar()
