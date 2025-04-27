# plataforma.py
import pygame
from config.configuracion import WIDTH, HEIGHT

class Plataforma(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.original_image = pygame.image.load("assets/img/scene/scene1/front.png").convert_alpha()
        self.image = self.original_image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.base_x = x  # Guardamos la posición original
        self.scroll_x = 0
        self.max_scroll = self.image.get_width() - WIDTH

    def draw(self, screen):
        screen.blit(self.image, (-self.scroll_x, 0))  # Mover LA PLATAFORMA horizontalmente


    def update(self, speed_x):
        self.scroll_x += speed_x  # Ajusta el desplazamiento
        self.scroll_x = max(0, min(self.scroll_x, self.max_scroll))  # Limitar scroll