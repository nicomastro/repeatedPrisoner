import random

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

    def generar_torta(self):
        torta = ''
        for _ in range(self.T):
            torta += random.choice(componentes)
        
        return torta
    
    def jugar(self):
        utilidad1 = 0
        utilidad2 = 0
        for i in range(self.N):
            torta = self.generar_torta()
            corte = jugador1.cut(torta, jugador2)
            porcion1, porcion2 = Jugador.cortar(torta, corte)

            porcion_j2, porcion_j1 = jugador2.choose(porcion1, porcion2)
            utilidad_j1 = jugador1.utilidad(porcion_j1)
            utilidad_j2 = jugador2.utilidad(porcion_j2)


            ### TODO: Completar bien esta funcion
            self.print_info(utilidad_j1, utilidad_j2)
        

    def print_info(self, utilidad_j1, utilidad_j2):
        ### TODO: Completar bien esta funcion
        print(f'Jugador 1: {utilidad_j1}')
        print(f'Jugador 2: {utilidad_j2}')

class Jugador:
    
    @staticmethod
    def correlacion_de_gustos(g1, g2):
        ### TODO: Completar bien esta funcion
        return 1.0

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

    def __init__(self, gustos):
        #self.gustos = Jugador.normalizar_gustos(gustos)
        self.gustos = gustos
        self.umbral_de_correlacion = 0.5
        self.porcentaje_bin = 1/10

    # Dada una porcion devuelve la utilidad de la misma para el jugador
    def utilidad(self, porcion):
        return sum([self.gustos[c] for c in porcion])

    def obtener_bins(self, torta):
        bin_1, bin_2, bin_3 = [0], [0], [0]
        bin_size = round(len(torta)*self.porcentaje_bin)
        i = 0
        for s in torta:
            i += 1
            if i > bin_size:
                i = 0
                bin_1.append(0)
                bin_2.append(0)
                bin_3.append(0)

            if s == "1":
                bin_1[-1] += 1
            elif s == "2":
                bin_2[-1] += 1
            elif s == "3":
                bin_3[-1] += 1

        return bin_1, bin_2, bin_3

    def degustar_bins(self, bin_1, bin_2, bin_3):
        bin = []
        g = self.gustos
        for b1, b2, b3 in zip(bin_1, bin_2, bin_3):
            bin.append(g["1"]*b1 + g["2"]*b2 + g["3"]*b3)

        return bin

    def obtener_indices_del_bin_maximo(self, torta, bin):
        maximo = max(bin)
        argmax = bin.index(maximo)

        bin_size = round(len(torta)*self.porcentaje_bin)
        return (bin_size*argmax, bin_size*(argmax+1))
        
    def encontrar_mejores_indices_en(self, torta, indices_maximo_bin):
        mejor_temp = (0, 1)
        mejor_utilidad = 0
        for i in range(indices_maximo_bin[0], indices_maximo_bin[1]):
            for j in range(i+1, indices_maximo_bin[1]):
                corte1, corte2 = self.cortar(torta, (i, j))
                utilidad1 = self.utilidad(corte1)
                utilidad2 = self.utilidad(corte2)
                if utilidad1 > mejor_utilidad:
                    mejor_temp = (i, j)
                    mejor_utilidad = utilidad1

                if utilidad2 > mejor_utilidad:
                    mejor_temp = (j, i)
                    mejor_utilidad = utilidad2
                

        return mejor_temp

    # Dada una torta y el rival devuelve un corte
    def cut(self, torta, rival):
        ### TODO: Completar bien esta funcion
        if Jugador.correlacion_de_gustos(self.gustos, rival.gustos) > self.umbral_de_correlacion:
            # Hago los bins y me fijo todos los posibles cortes en el mejor rango de bins
            bin_1, bin_2, bin_3 = self.obtener_bins(torta)
            bin = self.degustar_bins(bin_1, bin_2, bin_3)
            indices_maximo_bin = self.obtener_indices_del_bin_maximo(torta, bin)
            print(torta)
            print(bin)
            print(indices_maximo_bin)
            print(self.encontrar_mejores_indices_en(torta, indices_maximo_bin))
            return self.encontrar_mejores_indices_en(torta, indices_maximo_bin)

        else:
             
            return (0, 4)
        
        return (0, 1)

    # Dadas dos porciones devuelve la que mas utilidad le genera al jugador
    def choose(self, porcion1, porcion2):
        utilidad1 = self.utilidad(porcion1)
        utilidad2 = self.utilidad(porcion2)
        if utilidad1 >= utilidad2:
            return porcion1, porcion2
        else:
            return porcion2, porcion1
        
     
        
jugador1 = Jugador({'1': 1, '2': 1, '3': 1})
jugador2 = Jugador({'1': 1, '2': 2, '3': 0})
juego = Juego(30, 1, jugador1, jugador2)
juego.jugar()
