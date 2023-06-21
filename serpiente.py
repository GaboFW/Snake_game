import pygame

class Serpiente:
    def __init__(self):
        self.cabeza_imagen = pygame.image.load("SNAKE\Cabeza.png")
        self.cabeza_imagen = pygame.transform.scale(self.cabeza_imagen, (TAMANIO_CABEZA, TAMANIO_CABEZA))

        self.cuerpo_imagen = pygame.image.load("SNAKE\Cuerpo.png")
        self.cuerpo_imagen = pygame.transform.scale(self.cuerpo_imagen, (TAMANIO_CABEZA, TAMANIO_CABEZA))

        self.segmentos = [(ANCHO / 2, ALTO / 2)]
        self.cambio_x = 0.0
        self.cambio_y = 0.0

    def dibujar(self, pantalla):
        for i, (x, y) in enumerate(self.segmentos):
            if i == 0:
                pantalla.blit(self.cabeza_imagen, (x, y))
            else:
                pantalla.blit(self.cuerpo_imagen, (x, y))

    def mover(self):
        x, y = self.segmentos[0]
        nueva_cabeza = (x + self.cambio_x * TAMANIO_CABEZA, y + self.cambio_y * TAMANIO_CABEZA)
        self.segmentos.insert(0, nueva_cabeza)
        self.segmentos.pop()

    def colision_comida(self, comida):
        cabeza_x, cabeza_y = self.segmentos[0]
        if abs(cabeza_x - comida[0]) < TAMANIO_CABEZA and abs(cabeza_y - comida[1]) < TAMANIO_CABEZA:
            self.segmentos.append((0, 0))
            return True
        return False

    def colision_pared(self):
        cabeza_x, cabeza_y = self.segmentos[0]
        return cabeza_x < 0 or cabeza_x >= ANCHO or cabeza_y < 0 or cabeza_y >= ALTO

    def colision_cuerpo(self):
        return self.segmentos[0] in self.segmentos[1:-1]

    def cambiar_direccion(self, cambio_x, cambio_y):
        if (cambio_x == 0 and self.cambio_y == 0) or (cambio_y == 0 and self.cambio_x == 0):
            self.cambio_x = cambio_x
            self.cambio_y = cambio_y

ANCHO = 800
ALTO = 600
TAMANIO_CABEZA = 20








