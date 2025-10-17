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
    pygame.display.set_caption("Juego de Voz y Cazador")
    reloj = pygame.time.Clock()
    fuente = pygame.font.SysFont("Arial", 20)

    efectos.inicializar()
    voz.iniciar()

    idiomas = ["Español", "Ingles"]
    indice_idioma = 0
    idioma_actual = idiomas[indice_idioma]
    voz.set_idioma(idioma_actual)

    # 🔹 Generar laberinto inicial
    #mapa.mapa = mapa.generar_mapa_aleatorio(15, 15)

    # Inicializar cazador
    cazador_instancia = cazador.Cazador(POS_INICIAL_CAZADOR)
    tiempo_ultima_actualizacion = time.time()

    # Flag para mostrar mensaje de victoria
    ganador = False
    tiempo_ganador = 0

    # --- Bucle principal ---
    while True:
        pantalla.fill((0, 0, 0))

        # --- Dibujar ---
        dibujo.dibujar_toolbar(pantalla, fuente, idioma_actual)
        dibujo.dibujar_tablero(pantalla, mapa.mapa)
        dibujo.dibujar_jugador(pantalla, jugador.jugador_pos)
        dibujo.dibujar_cazador(pantalla, cazador_instancia.posicion)
        
        # Mostrar mensaje de victoria si corresponde
        if ganador and pygame.time.get_ticks() - tiempo_ganador < 1000:
            texto = fuente.render("¡Has ganado!", True, (255, 255, 0))
            pantalla.blit(texto, (ANCHO//2 - 60, ALTO//2))
        elif ganador:
            ganador = False  # Desactivar mensaje

        # --- Movimiento por voz ---
        comando = voz.get_comando()
        if comando:
            victoria = jugador.mover_jugador_direccion(comando)
            if victoria:
                ganador = True
                tiempo_ganador = pygame.time.get_ticks()

                # Generar nuevo laberinto válido
                nuevo_mapa = mapa.generar_mapa_aleatorio(15, 15)

                # Sobrescribir in-place el mapa existente
                for y in range(len(mapa.mapa)):
                    for x in range(len(mapa.mapa[0])):
                        mapa.mapa[y][x] = nuevo_mapa[y][x]

                # Reiniciar posiciones
                jugador.jugador_pos = [1, 1]
                cazador_instancia.posicion = POS_INICIAL_CAZADOR
                cazador_instancia.ruta = []

        # --- Movimiento por teclado ---
        # Mover cazador constantemente
        cazador_instancia.actualizar_objetivo(jugador.jugador_pos)
        cazador_instancia.mover()

        for evento in pygame.event.get():
            if evento.type == pygame.KEYDOWN:
                teclas = {
                    pygame.K_UP: "up",
                    pygame.K_DOWN: "down",
                    pygame.K_LEFT: "left",
                    pygame.K_RIGHT: "right"
                }
                if evento.key in teclas:
                    direccion = teclas[evento.key]
                    victoria = jugador.mover_jugador_direccion(direccion)

                    if victoria:
                        ganador = True
                        tiempo_ganador = pygame.time.get_ticks()

                        # Generar nuevo laberinto válido
                        nuevo_mapa = mapa.generar_mapa_aleatorio(15, 15)

                        # Sobrescribir in-place
                        for y in range(len(mapa.mapa)):
                            for x in range(len(mapa.mapa[0])):
                                mapa.mapa[y][x] = nuevo_mapa[y][x]

                        # Reiniciar posiciones
                        jugador.jugador_pos = [1, 1]
                        cazador_instancia.posicion = POS_INICIAL_CAZADOR
                        cazador_instancia.ruta = []



        pygame.display.flip()
        reloj.tick(FPS)


if __name__ == "__main__":
    main()
