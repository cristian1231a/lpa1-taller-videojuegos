import pygame, random
from configuracion import WIDTH, HEIGHT

class Escenario:
    def __init__(self):
        self.image = pygame.image.load("assets/img/scene/scene1/back.png").convert()
        self.scroll_x = 0
        self.max_scroll = self.image.get_width() - WIDTH

    def draw(self, screen):
        screen.blit(self.image, (-self.scroll_x, 0))  # Mover el fondo horizontalmente

    def update(self, speed_x):
        self.scroll_x += speed_x  # Ajusta el desplazamiento
        self.scroll_x = max(0, min(self.scroll_x, self.max_scroll))  # Limitar scroll