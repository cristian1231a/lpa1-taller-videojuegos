import pygame
import math

class ParticulaXP(pygame.sprite.Sprite):
    def __init__(self, x, y, destino, cantidad_xp, jugador):
        super().__init__()
        self.image = pygame.Surface((10, 10))  # Tamaño de la partícula
        self.image.fill((255, 255, 0))  # Color amarillo para la partícula
        self.rect = self.image.get_rect(center=(x, y))
        self.destino = destino  # La posición de la barra de experiencia
        self.cantidad_xp = cantidad_xp  # Cuántos puntos de experiencia da esta partícula
        self.velocidad = 3  # Velocidad a la que se mueve la partícula
        self.jugador = jugador  # El jugador, para agregar experiencia al llegar

    def update(self):
        # Movimiento de la partícula hacia el destino
        dx = self.destino[0] - self.rect.centerx
        dy = self.destino[1] - self.rect.centery
        distancia = (dx ** 2 + dy ** 2) ** 0.5  # Distancia a la barra de experiencia

        if distancia > self.velocidad:
            # Mover la partícula hacia el destino
            self.rect.x += self.velocidad * (dx / distancia)
            self.rect.y += self.velocidad * (dy / distancia)
        else:
            # Si la partícula llega al destino, se elimina y suma la experiencia
            self.kill()  # Eliminar la partícula
            self.sumar_experiencia()  # Sumar experiencia al jugador

    def sumar_experiencia(self):
        # Sumar la experiencia directamente al jugador
        if self.jugador:
            self.jugador.nivel_xp.agregar_experiencia(self.cantidad_xp)