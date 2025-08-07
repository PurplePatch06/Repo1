# cazador.py

import mapa
import heapq

class Cazador:
    def __init__(self, posicion_inicial):
        self.posicion = tuple(posicion_inicial)  # (fila, col)
        self.ruta = []
        self.objetivo = None

    def actualizar_objetivo(self, nueva_pos):
        if nueva_pos != self.objetivo:
            self.objetivo = tuple(nueva_pos)
            self.ruta = self.a_star(self.posicion, self.objetivo)

    def mover(self):
        if self.ruta:
            self.posicion = self.ruta.pop(0)

    def esta_cerca_jugador(self, jugador_pos):
        return self.posicion == tuple(jugador_pos)

    def a_star(self, inicio, objetivo):
        open_set = []
        heapq.heappush(open_set, (0, 0, inicio, []))
        visited = set()

        def heuristica(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        while open_set:
            f_score, g_score, actual, camino = heapq.heappop(open_set)

            if actual == objetivo:
                return camino + [objetivo]

            if actual in visited:
                continue
            visited.add(actual)

            for vecino in self.obtener_vecinos(actual):
                if vecino in visited:
                    continue
                nuevo_g = g_score + 1
                nuevo_f = nuevo_g + heuristica(vecino, objetivo)
                heapq.heappush(open_set, (nuevo_f, nuevo_g, vecino, camino + [actual]))

        return []

    def obtener_vecinos(self, nodo):
        fila, col = nodo
        posibles = [
            (fila - 1, col),
            (fila + 1, col),
            (fila, col - 1),
            (fila, col + 1),
        ]
        vecinos_validos = []
        for f, c in posibles:
            if mapa.es_caminable(f, c) or (f, c) == self.objetivo:
                vecinos_validos.append((f, c))
        return vecinos_validos
