# main.py

import pygame
import sys
import time

import mapa
import jugador
import efectos
import voz
import dibujo
import cazador

from config import (
    ANCHO,
    ALTO,
    ALTURA_TOOLBAR,
    FPS,
    POS_INICIAL_CAZADOR,
    POS_INICIAL_JUGADOR,
)

def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO + ALTURA_TOOLBAR))
    pygame.display.set_caption("Juego con Voz y Cazador")
    reloj = pygame.time.Clock()
    fuente = pygame.font.SysFont("Arial", 20)

    efectos.inicializar()
    voz.iniciar()

    idiomas = ["Español", "Ingles"]
    indice_idioma = 0
    idioma_actual = idiomas[indice_idioma]
    voz.set_idioma(idioma_actual)

    # Inicializar cazador
    cazador_instancia = cazador.Cazador(POS_INICIAL_CAZADOR)
    tiempo_ultima_actualizacion = time.time()

    while True:
        pantalla.fill((0, 0, 0))

        dibujo.dibujar_toolbar(pantalla, fuente, idioma_actual)
        dibujo.dibujar_tablero(pantalla, mapa.mapa)
        dibujo.dibujar_jugador(pantalla, jugador.jugador_pos)
        dibujo.dibujar_cazador(pantalla, cazador_instancia.posicion)

        # Movimiento por voz
        comando = voz.get_comando()
        if comando:
            victoria = jugador.mover_jugador_direccion(comando)
            if victoria:
                cazador_instancia.posicion = POS_INICIAL_CAZADOR
                cazador_instancia.ruta = []

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                voz.detener()
                pygame.quit()
                sys.exit()

            elif evento.type == pygame.KEYDOWN and not comando:
                teclas = {
                    pygame.K_UP: "up",
                    pygame.K_DOWN: "down",
                    pygame.K_LEFT: "left",
                    pygame.K_RIGHT: "right"
                }
                if evento.key in teclas:
                    victoria = jugador.mover_jugador_direccion(teclas[evento.key])
                    if victoria:
                        cazador_instancia.posicion = POS_INICIAL_CAZADOR
                        cazador_instancia.ruta = []

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if evento.pos[0] >= ANCHO - 80:  # Botón salir
                    voz.detener()
                    pygame.quit()
                    sys.exit()
                elif 10 <= evento.pos[0] <= 160:  # Cambiar idioma
                    indice_idioma = (indice_idioma + 1) % len(idiomas)
                    idioma_actual = idiomas[indice_idioma]
                    voz.set_idioma(idioma_actual)

        # Actualizar objetivo del cazador cada 3 segundos
        if time.time() - tiempo_ultima_actualizacion > 3:
            cazador_instancia.actualizar_objetivo(jugador.jugador_pos)
            tiempo_ultima_actualizacion = time.time()

        # Mover cazador 1 paso por frame
        cazador_instancia.mover()

        # Si el cazador atrapa al jugador
        if cazador_instancia.esta_cerca_jugador(jugador.jugador_pos):
            print("[CAZADOR] El jugador fue atrapado. Reiniciando posición...")
            jugador.jugador_pos = list(POS_INICIAL_JUGADOR)
            cazador_instancia.posicion = POS_INICIAL_CAZADOR
            cazador_instancia.ruta = []

        pygame.display.flip()
        reloj.tick(FPS)

if __name__ == "__main__":
    main()
