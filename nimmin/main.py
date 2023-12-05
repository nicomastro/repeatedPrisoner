# Sean los enteros positivos n1, n2, n3, r1, r2, r3, con n1 <= n2 <= n3 y r1 <= r2 <= r3. 
# Juego por turnos de información perfecta no partizano para los jugadores L y R. 
# Hay 3 pilas, de n1, n2 y n3 objetos, respectivamente. 
# Cada jugador a su turno debe quitar r1, r2 o r3 objetos de una misma pila. 
# Comienza el jugador L. Pierde quien juega último.


# Calcular los conjuntos de P-posiciones y N-posiciones,

# Dar una función que dada una posición para el jugador L devuelva la resultante de hacer una jugada óptima. 

# Si la posición original no fuese ganadora para L, se deberá "dificultar" la decisión al jugador R en su siguiente turno si fuera posible.



# para dificultar la decisión se puede considerar el valor de cada nodo que sería, por ejemplo, el tamaño del arbol
# para las hojas, esto es 1 

import numpy as np

class Game:

	def __init__(self, ns, rs):
		self.ns = ns
		self.rs = rs
		self.moves = [] # sequence of games (left, player 0, goes first)
		self.score = 0

	def isLeaf(self):
		return (self.rs[0] > self.ns[0] and self.rs[0] > self.ns[1] 
				and self.rs[0] > self.ns[2])

	def valor(self):

		if self.isLeaf():
			self._value = 1
			return self._value
		elif jugadas_previas.get(self.id()) is not None:
			self._value, self.moves = jugadas_previas[self.id()]
		else:
			children = self.children()
			self._value = int(np.sum([h.valor() for h in children]) != len(children))
			self.score += np.sum([ch.score for ch in children])		

			if self._value == 1:
				option = [h for h in children if h.valor() == 0][0] # any p move
			else:
				option = children[np.argmax([ch.score for ch in children])]
		
			l = option.moves
			self.moves = [option] + l
			jugadas_previas[self.id()] = (self._value, self.moves)
		return self._value

	def children(self):
		children = []
		for r in self.rs:
			for i, n in enumerate(self.ns):
				if r <= n:
					new_ns = self.ns.copy()
					new_ns[i] -= r	
					children.append(Game(new_ns,self.rs))

		return children	

	def id(self):
		return tuple(sorted(self.ns))

	def __repr__(self):
		return ('|' + '*'*self.ns[0] +'|' + '*'*self.ns[1] + '|' + '*'*self.ns[2] + '|')

# n3 < 200 deberia ser razonable

ns = [200,100,100]
rs = [1,2,3]
assert(ns[0] <= ns[1] <= ns[2])
assert(0 < rs[0] <= rs[1] <= rs[2])
d = {0: 'P', 1:'N'}
jugadas_previas = {}
j = Game(ns, rs)
v = j.valor()

print(d[v])
print(j)
for j in j.moves:
	print(j)