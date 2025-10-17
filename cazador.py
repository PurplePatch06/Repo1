# cazador.py - Versión simplificada usando [x, y]

import mapa
import heapq

class Cazador:
    def _init_(self, posicion_inicial):
        self.posicion = list(posicion_inicial)  # [x, y]
        self.ruta = []
        self.objetivo = None

    def actualizar_objetivo(self, nueva_pos):
        if list(nueva_pos) != self.objetivo:
            self.objetivo = list(nueva_pos)
            self.ruta = self.a_star(self.posicion, self.objetivo)

    def mover(self):
        if self.ruta:
            self.posicion = self.ruta.pop(0)

    def esta_cerca_jugador(self, jugador_pos):
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
        x, y = nodo
        posibles = [
            [x, y - 1],  # Arriba
            [x, y + 1],  # Abajo
            [x - 1, y],  # Izquierda
            [x + 1, y],  # Derecha
        ]
        vecinos_validos = []
        for pos in posibles:
            # 🔹 mapa.es_caminable espera (fila, col) = (y, x)
            if mapa.es_caminable(pos[1], pos[0]) or pos == self.objetivo:
                vecinos_validos.append(pos)
        return vecinos_validos