#mapa.py

#15x15
# mapa.py
# mapa.py

# mapa.py
import random
from collections import deque

ANCHO = 15
ALTO = 15

CAMINO = 20
MURO = 800
META = 10
INICIO = (1, 1)
FINAL = (ALTO-2, ANCHO-2)

mapa = []  # Variable global del mapa actual

# --- Generador principal ---
def generar_mapa_aleatorio(ancho=ANCHO, alto=ALTO):
    while True:
        laberinto = [[MURO for _ in range(ancho)] for _ in range(alto)]

        # Punto inicial
        start_x, start_y = INICIO
        laberinto[start_y][start_x] = CAMINO

        direcciones = [(-2,0),(2,0),(0,-2),(0,2)]

        def backtrack(x, y):
            random.shuffle(direcciones)
            for dx, dy in direcciones:
                nx, ny = x + dx, y + dy
                if 1 <= nx < ancho-1 and 1 <= ny < alto-1 and laberinto[ny][nx] == MURO:
                    laberinto[y+dy//2][x+dx//2] = CAMINO
                    laberinto[ny][nx] = CAMINO
                    backtrack(nx, ny)

        # Generar laberinto base
        backtrack(start_x, start_y)

        # Añadir caminos alternativos
        laberinto = agregar_caminos_alternativos(laberinto, intentos=15)

        # Colocar meta
        laberinto[FINAL[0]][FINAL[1]] = META

        # Verificar que exista camino
        if camino_valido(laberinto):
            return laberinto

# --- Agregar loops para rutas alternativas ---
def agregar_caminos_alternativos(laberinto, intentos=10):
    alto = len(laberinto)
    ancho = len(laberinto[0])
    for _ in range(intentos):
        x = random.randint(1, ancho-2)
        y = random.randint(1, alto-2)
        if laberinto[y][x] == MURO:
            vecinos = 0
            for dx, dy in [(-1,0),(1,0),(0,-1),(0,1)]:
                nx, ny = x+dx, y+dy
                if 0<=nx<ancho and 0<=ny<alto and laberinto[ny][nx]==CAMINO:
                    vecinos +=1
            if vecinos >= 2:
                laberinto[y][x] = CAMINO
    return laberinto

# --- Verificar camino válido usando BFS ---
def camino_existe(lab, inicio, meta):
    alto = len(lab)
    ancho = len(lab[0])
    visitado = [[False]*ancho for _ in range(alto)]
    q = deque([inicio])
    visitado[inicio[0]][inicio[1]] = True

    while q:
        y,x = q.popleft()
        if (y,x) == meta:
            return True
        for dy, dx in [(-1,0),(1,0),(0,-1),(0,1)]:
            ny, nx = y+dy, x+dx
            if 0<=ny<alto and 0<=nx<ancho:
                if not visitado[ny][nx] and lab[ny][nx] in (CAMINO,META):
                    visitado[ny][nx] = True
                    q.append((ny,nx))
    return False

def camino_valido(laberinto):
    inicio = INICIO
    meta = FINAL
    return camino_existe(laberinto, inicio, meta)

# --- Área accesible desde una celda ---
def area_accesible(lab, inicio):
    alto = len(lab)
    ancho = len(lab[0])
    visitado = [[False]*ancho for _ in range(alto)]
    q = deque([inicio])
    visitado[inicio[0]][inicio[1]] = True
    area = 0
    while q:
        y,x = q.popleft()
        area += 1
        for dy, dx in [(-1,0),(1,0),(0,-1),(0,1)]:
            ny, nx = y+dy, x+dx
            if 0<=ny<alto and 0<=nx<ancho:
                if not visitado[ny][nx] and lab[ny][nx] in (CAMINO,META):
                    visitado[ny][nx] = True
                    q.append((ny,nx))
    return area

# --- Utilidades ---
def imprimir_mapa(mapa_actual):
    for fila in mapa_actual:
        print(fila)

def es_caminable(fila, col):
    if 0<=fila<len(mapa) and 0<=col<len(mapa[0]):
        return mapa[fila][col] in (CAMINO,META)
    return False

# Generar mapa al importar
mapa = generar_mapa_aleatorio()


# 800 = pared
# 20 = camino
# 10 Inicio y Meta

#mapa = [
#    [1]  [2]  [3]  [4]  [5]  [6]  [7]  [8]  [9]  [10] [11] [12] [13] [14] [15] 
 #   [800, 800, 800, 800, 800, 800, 800, 800, 800, 800, 800, 800, 800, 800, 800],
 #   [800,  20,  20, 800,  20,  20,  20, 800,  20,  20,  20, 800,  20,  20, 800],
 #   [800, 800,  20, 800,  20, 800,  20, 800,  20, 800,  20, 800,  20, 800, 800],
 #   [800,  20,  20,  20,  20, 800,  20,  20,  20, 800,  20,  20,  20,  20, 800],
 #   [800,  20, 800, 800,  20, 800, 800, 800,  20, 800, 800, 800, 800,  20, 800],
 #   [800,  20, 800,  20,  20,  20,  20,  20,  20,  20,  20,  20, 800,  20, 800],
 #   [800,  20, 800,  20, 800, 800, 800, 800, 800, 800,  20, 800, 800,  20, 800],
 #   [800,  20,  20,  20, 800,  20,  20,  20,  20, 800,  20,  20,  20,  20, 800],
 #   [800, 800, 800,  20, 800,  20, 800, 800,  20, 800, 800, 800, 800,  20, 800],
 #   [800,  20,  20,  20, 800,  20, 800,  20,  20,  20,  20,  20, 800,  20, 800],
 #   [800,  20, 800, 800, 800,  20, 800,  20, 800, 800, 800,  20, 800,  20, 800],
 #   [800,  20,  20,  20,  20,  20, 800,  20,  20,  20, 800,  20,  20,  20, 800],
 #   [800, 800, 800, 800, 800, 800, 800, 800, 800,  20, 800, 800, 800, 800, 800],
 #   [800,  20,  20,  20,  20,  20,  20,  20,  20,  20,  20,  20,  20,  10, 800],
 #   [800, 800, 800, 800, 800, 800, 800, 800, 800, 800, 800, 800, 800, 800, 800],
#]

#def es_caminable(fila, col):
#    if 0 <= fila < len(mapa) and 0 <= col < len(mapa[0]):
#        return mapa[fila][col] == 20
#    return False
