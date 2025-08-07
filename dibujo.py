#dibujo.py
import pygame
from mapa import mapa
from jugador import jugador_pos
from config import TAM_CELDA, COLOR_MURO, COLOR_CAMINO, COLOR_BOTON, COLOR_TEXTO, BOTON_RECT, COLOR_VICTORIA, ALTURA_TOOLBAR,COLOR_JUGADOR

def dibujar_tablero(pantalla, fuente, idioma_actual):
    # Dibujar toolbar
    pygame.draw.rect(pantalla, (30, 30, 30), (0, 0, pantalla.get_width(), ALTURA_TOOLBAR))

    # Texto idioma
    texto_idioma = fuente.render(f"Idioma: {idioma_actual}", True, COLOR_TEXTO)
    pantalla.blit(texto_idioma, (10, 10))

    # Botón salir
    boton_rect = pygame.Rect(BOTON_RECT)
    pygame.draw.rect(pantalla, COLOR_BOTON, boton_rect)
    texto_salir = fuente.render("Salir", True, COLOR_TEXTO)
    texto_rect = texto_salir.get_rect(center=boton_rect.center)
    pantalla.blit(texto_salir, texto_rect)

    # Dibujar el mapa
    y_offset = ALTURA_TOOLBAR
    for fila in range(len(mapa)):
        for col in range(len(mapa[fila])):
            valor = mapa[fila][col]
            if valor == 20:
                color = COLOR_CAMINO
            elif valor == 10:
                color = COLOR_VICTORIA
            else:
                color = COLOR_MURO
            pygame.draw.rect(
                pantalla,
                color,
                (col * TAM_CELDA, fila * TAM_CELDA + y_offset, TAM_CELDA, TAM_CELDA)
            )

    # Dibujar jugador
    pygame.draw.rect(
        pantalla,
        COLOR_JUGADOR,
        (jugador_pos[1] * TAM_CELDA, jugador_pos[0] * TAM_CELDA + y_offset, TAM_CELDA, TAM_CELDA)
    )

def obtener_area_boton_salir():
    return pygame.Rect(BOTON_RECT)

def obtener_area_selector_idioma():
    return pygame.Rect(10, 10, 150, 25)
