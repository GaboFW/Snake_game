import pygame
import random
import colores
import sqlite3
from serpiente import *
import pygame.font
from base_de_datos import *

pygame.init()
pygame.mixer.init()

# Dimension pantalla
ANCHO = 800
ALTO = 600

# Tamaño y velocidad
TAMANIO_CABEZA = 20
velocidad = 15

# Sonido
# Fondo
sonido_fondo = pygame.mixer.music.load("SNAKE\Musica de Fondo.mp3")
pygame.mixer.music.play()
# Dentro del juego
sonido_comer = pygame.mixer.Sound("SNAKE\Comer.mp3")
sonido_game_over = pygame.mixer.Sound("SNAKE\Game_Over.mp3")
pygame.mixer.music.set_volume(0.1)

# Pantalla
pantalla = pygame.display.set_mode((ANCHO, ALTO))
pygame.display.set_caption("Snake Game")

# Imagen fondo
fondo = pygame.image.load("SNAKE\Fondo.png")
fondo = pygame.transform.scale(fondo, (800, 600))

# Imagen inicio
pantalla_inicio = pygame.image.load("SNAKE\Pantalla de inicio.png")
pantalla_inicio = pygame.transform.scale(pantalla_inicio, (800, 600))

# Llamar a la clase
serpiente = Serpiente()

# Velocidad actualizacion
reloj = pygame.time.Clock()

# Puntos
def mostrar_puntaje(puntos):
    fuente = pygame.font.Font(None, 25)
    texto = fuente.render(f"Puntos: {puntos}", True, (colores.negro))
    pantalla.blit(texto, (10, 10))

# Dibujar la comida
def manzanita(comida):
    x, y = comida
    manzanita = pygame.image.load("SNAKE\Manzanita.png")
    manzanita = pygame.transform.scale(manzanita, (TAMANIO_CABEZA, TAMANIO_CABEZA))
    pantalla.blit(manzanita, (x, y))

# Generar la posicion de la comida
def generar_comida():
    celdas_x = ANCHO / 20
    celdas_y = ALTO / 20
    x = random.randint(0, celdas_x - 1) * 20
    y = random.randint(0, celdas_y - 1) * 20
    return (x, y)

# Mostrar el Ranking
def mostrar_ranking(conexion):
    cursor = conexion.execute("SELECT jugador, puntos FROM Ranking ORDER BY puntos DESC LIMIT 5")
    pos = 300
    for fila in cursor:
        nombre, puntos = fila
        fuente = pygame.font.Font(None, 35)
        datos = fuente.render(f"{nombre}: {puntos}", True, colores.negro)
        pantalla.blit(datos, (ANCHO / 2 - datos.get_width() / 2, pos))
        pos += 40

# El juego
def juego():
    movimiento = 1.0

    puntos = 0

    cronometro = 0

    comida = generar_comida()

    pantalla.blit(pantalla_inicio, (0, 0))
    pygame.display.flip()

    nombre = ""
    nombre_ingresado = False

    while not nombre_ingresado:
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if len(nombre) < 3:
                    letra = pygame.key.name(event.key)
                    nombre += letra
                    nombre_ranking = pygame.font.Font(None, 35)
                    texto = nombre_ranking.render("Escriba su nombre: " + "".join(nombre), True, colores.negro)
                    pantalla.blit(texto, (10, 500))
                else:
                    nombre_ingresado = True
        pygame.display.flip()

    game_over = False

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Cronometro
        if running:
            cronometro += 1

        # Movimiento de la serpiente
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] or keys[pygame.K_w]:
            serpiente.cambiar_direccion(0, -movimiento)
        if keys[pygame.K_DOWN] or keys[pygame.K_s]:
            serpiente.cambiar_direccion(0, movimiento)
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            serpiente.cambiar_direccion(movimiento, 0)
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            serpiente.cambiar_direccion(-movimiento, 0)

        serpiente.mover()

        # Come y suma 1 punto
        if serpiente.colision_comida(comida):
            sonido_comer.play()
            puntos += 1
            if puntos % 5 == 0:  # Aumentar velocidad cada 5 puntos
                movimiento += 0.2
            comida = generar_comida()

        # Choca con ella misma y con la pared ¡¡GAME OVER!!
        if serpiente.colision_pared() or serpiente.colision_cuerpo():
            sonido_game_over.play()
            game_over = True
            running = False

        # Mostrarlo
        pantalla.blit(fondo, (0, 0))
        mostrar_puntaje(puntos)
        serpiente.dibujar(pantalla)
        manzanita(comida)
        pygame.display.update()
        reloj.tick(velocidad)

    # Guardar puntaje en un SQL
    conexion = sqlite3.connect("Puntacion.db")
    conexion.execute("INSERT INTO Ranking(jugador, puntos) VALUES (?,?)", (nombre, puntos))
    conexion.commit()

    while game_over:
        pygame.mixer.music.stop()
        # Todo
        pantalla.blit(fondo, (0, 0))
        # Game Over
        mensaje = pygame.font.SysFont("Gintronic", 70)
        texto = mensaje.render("GAME OVER", True, colores.rojo)
        pantalla.blit(texto, (ANCHO / 4, ALTO / 4))
        # Puntos
        score = pygame.font.SysFont("Gintronic", 50)
        puntaje = score.render(f"Puntos: {puntos}", True, colores.negro)
        # Cerrar Juego
        botones = pygame.font.SysFont("Gintronic", 15)
        boton_q = botones.render("[Q] Cerrar Juego", True, colores.negro)
        # Mostrar
        pantalla.blit(puntaje, (10, 10))
        pantalla.blit(boton_q, (ANCHO / 8, ALTO / 8))
        # SQL
        mostrar_ranking(conexion)

        pygame.display.update()

        # Reiniciar o Cerrar
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = False
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    game_over = False
                    running = False

    conexion.close()

    pygame.quit()

juego()
