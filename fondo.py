import pygame, random
WIDTH = 800
HEIGHT = 600

class Fondo:
    def __init__(self):
        self.image = pygame.image.load("assets/img/scene/scene1/back.png").convert()
        self.scroll_x = 0  # Desplazamiento inicial

    def draw(self, screen):
        screen.blit(self.image, (0, 0))  # Dibujar fondo en la pantalla

    def update(self, speed_x):
        self.scroll_x -= speed_x  # Mover el fondo en dirección opuesta al jugador

