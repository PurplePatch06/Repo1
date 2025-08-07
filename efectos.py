#efectos.py

import pygame
import platform

if platform.system() == "Windows":
    import winsound

def inicializar():
    pygame.mixer.init()
    global sonido_bonk, sonido_victoria
    sonido_bonk = cargar_sonido("colision.mp3")
    sonido_victoria = cargar_sonido("victory.mp3")

def cargar_sonido(ruta):
    try:
        return pygame.mixer.Sound(ruta)
    except:
        print(f"[EFECTOS] No se pudo cargar {ruta}, se usará beep del sistema.")
        return None

def bonk():
    if sonido_bonk:
        sonido_bonk.play()
    else:
        beep()

def victoria():
    if sonido_victoria:
        sonido_victoria.play()
    else:
        beep(frecuencia=1000, duracion=300)

def beep(frecuencia=750, duracion=200):
    if platform.system() == "Windows":
        winsound.Beep(frecuencia, duracion)
    else:
        print("[EFECTOS] Beep no compatible en este sistema (solo Windows)")
