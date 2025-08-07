#main.py

import pygame
import sys
import efectos
import voz
import jugador
import dibujo
from config import ALTURA_TOOLBAR, FPS, ANCHO, ALTO

IDIOMAS = ["Español", "Ingles"]
indice_idioma = 0

def main():
    global indice_idioma

    pygame.init()
    efectos.inicializar()
    voz.iniciar()
    voz.set_idioma(IDIOMAS[indice_idioma])

    pantalla = pygame.display.set_mode((ANCHO, ALTO + ALTURA_TOOLBAR))
    pygame.display.set_caption("Juego con Voz y Modularidad")
    reloj = pygame.time.Clock()
    fuente = pygame.font.SysFont("Arial", 20)

    while True:
        pantalla.fill((0, 0, 0))

        dibujo.dibujar_tablero(pantalla, fuente, IDIOMAS[indice_idioma])

        # Movimiento por voz
        comando = voz.get_comando()
        if comando:
            jugador.mover_jugador_direccion(comando)

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                voz.detener()
                pygame.quit()
                sys.exit()

            elif evento.type == pygame.KEYDOWN:
                if not comando:
                    teclas = {
                        pygame.K_UP: "up",
                        pygame.K_DOWN: "down",
                        pygame.K_LEFT: "left",
                        pygame.K_RIGHT: "right"
                    }
                    if evento.key in teclas:
                        jugador.mover_jugador_direccion(teclas[evento.key])

            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if dibujo.obtener_area_boton_salir().collidepoint(evento.pos):
                    voz.detener()
                    pygame.quit()
                    sys.exit()
                elif dibujo.obtener_area_selector_idioma().collidepoint(evento.pos):
                    indice_idioma = (indice_idioma + 1) % len(IDIOMAS)
                    voz.set_idioma(IDIOMAS[indice_idioma])
                    print(f"[INFO] Idioma cambiado a {IDIOMAS[indice_idioma]}")

        pygame.display.flip()
        reloj.tick(FPS)

if __name__ == "__main__":
    main()
