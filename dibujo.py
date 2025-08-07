# dibujo.py

import pygame
from config import (
    TAM_CELDA,
    ALTURA_TOOLBAR,
    COLOR_MURO,
    COLOR_CAMINO,
    COLOR_JUGADOR,
    COLOR_CAZADOR,
    COLOR_BOTON,
    COLOR_TEXTO,
    COLOR_VICTORIA
)

def dibujar_tablero(pantalla, mapa):
    y_offset = ALTURA_TOOLBAR
    for fila in range(len(mapa)):
        for col in range(len(mapa[fila])):
            valor = mapa[fila][col]
            if valor == 20:
                color = COLOR_CAMINO
            elif valor == 10:  # Meta
                color = COLOR_VICTORIA
            else:
                color = COLOR_MURO

            pygame.draw.rect(
                pantalla,
                color,
                (col * TAM_CELDA, fila * TAM_CELDA + y_offset, TAM_CELDA, TAM_CELDA)
            )

def dibujar_toolbar(pantalla, fuente, idioma_actual):
    pygame.draw.rect(pantalla, (30, 30, 30), (0, 0, pantalla.get_width(), ALTURA_TOOLBAR))

    # Botón salir
    boton_rect = pygame.Rect((pantalla.get_width() - 80, 5, 70, 30))
    pygame.draw.rect(pantalla, COLOR_BOTON, boton_rect)
    texto_salir = fuente.render("Salir", True, COLOR_TEXTO)
    pantalla.blit(texto_salir, (boton_rect.x + 10, boton_rect.y + 5))

    # Selector idioma
    texto_idioma = fuente.render(f"Idioma: {idioma_actual}", True, COLOR_TEXTO)
    pantalla.blit(texto_idioma, (10, 10))

def dibujar_jugador(pantalla, posicion_jugador):
    y_offset = ALTURA_TOOLBAR
    fila, col = posicion_jugador
    pygame.draw.rect(
        pantalla,
        COLOR_JUGADOR,
        (col * TAM_CELDA, fila * TAM_CELDA + y_offset, TAM_CELDA, TAM_CELDA)
    )

def dibujar_cazador(pantalla, posicion_cazador):
    y_offset = ALTURA_TOOLBAR
    fila, col = posicion_cazador
    pygame.draw.rect(
        pantalla,
        COLOR_CAZADOR,
        (col * TAM_CELDA, fila * TAM_CELDA + y_offset, TAM_CELDA, TAM_CELDA)
    )
