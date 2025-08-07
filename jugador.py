# jugador.py

import efectos
import pygame
from mapa import mapa
from config import POS_INICIAL_JUGADOR

# Posición inicial del jugador (fila, columna)
jugador_pos = list(POS_INICIAL_JUGADOR)  # Convertimos a lista para mutabilidad


def mover_jugador_direccion(direccion):
    dx, dy = 0, 0
    if direccion == "up":
        dx, dy = -1, 0
    elif direccion == "down":
        dx, dy = 1, 0
    elif direccion == "left":
        dx, dy = 0, -1
    elif direccion == "right":
        dx, dy = 0, 1

    nueva_x = jugador_pos[0] + dx
    nueva_y = jugador_pos[1] + dy

    if 0 <= nueva_x < len(mapa) and 0 <= nueva_y < len(mapa[0]):
        celda_valor = mapa[nueva_x][nueva_y]

        if celda_valor == 20:  # Camino
            jugador_pos[0] = nueva_x
            jugador_pos[1] = nueva_y

        elif celda_valor == 10:  # Meta (victoria)
            jugador_pos[0] = nueva_x
            jugador_pos[1] = nueva_y
            efectos.victoria()
            pygame.time.delay(1000)  # Espera 1 segundo para que se escuche el sonido

            # Reiniciar jugador
            jugador_pos[0] = POS_INICIAL_JUGADOR[0]
            jugador_pos[1] = POS_INICIAL_JUGADOR[1]

            return True  # Señal de victoria

        else:  # Muro u obstáculo
            efectos.bonk()
    else:
        efectos.bonk()

    return False  # No hubo victoria
