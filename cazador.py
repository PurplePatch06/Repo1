# cazador.py - Versión simplificada usando [x, y]

import mapa
import heapq

class Cazador:
    def __init__(self, posicion_inicial):
        self.posicion = list(posicion_inicial)  # [x, y]
        self.ruta = []
        self.objetivo = None

    def actualizar_objetivo(self, nueva_pos):
        nueva_pos_lista = list(nueva_pos)
        if nueva_pos_lista != self.objetivo:
            self.objetivo = nueva_pos_lista
            self.ruta = self.a_star(self.posicion, self.objetivo)

    def mover(self):
        if self.ruta:
            self.posicion = self.ruta.pop(0)

    def atrapo_jugador(self, jugador_pos):
        return self.posicion == list(jugador_pos)

    def a_star(self, inicio, objetivo):
        open_set = []
        heapq.heappush(open_set, (0, 0, tuple(inicio), []))
        visited = set()

        def heuristica(a, b):
            return abs(a[0] - b[0]) + abs(a[1] - b[1])

        while open_set:
            f_score, g_score, actual, camino = heapq.heappop(open_set)

            if list(actual) == objetivo:
                return camino + [list(objetivo)]

            if actual in visited:
                continue
            visited.add(actual)

            for vecino in self.obtener_vecinos(list(actual)):
                vecino_tupla = tuple(vecino)
                if vecino_tupla in visited:
                    continue
                nuevo_g = g_score + 1
                nuevo_f = nuevo_g + heuristica(vecino_tupla, tuple(objetivo))
                heapq.heappush(
                    open_set,
                    (nuevo_f, nuevo_g, vecino_tupla, camino + [list(actual)]),
                )

        return []

    def obtener_vecinos(self, nodo):
        fila, col = nodo
        posibles = [
            [fila - 1, col],  # Arriba
            [fila + 1, col],  # Abajo
            [fila, col - 1],  # Izquierda
            [fila, col + 1],  # Derecha
        ]
        vecinos_validos = []
        for pos in posibles:
            # mapa.es_caminable espera (fila, col)
            if mapa.es_caminable(pos[0], pos[1]) or pos == self.objetivo:
                vecinos_validos.append(pos)
        return vecinos_validos
