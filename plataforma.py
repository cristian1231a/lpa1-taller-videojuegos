# plataforma.py
import pygame

class Plataforma(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.Surface((width, height))  # ✅ Atributo "image"
        self.image = pygame.image.load("assets/img/scene/scene1/front.png").convert_alpha()
        self.rect = self.image.get_rect(topleft=(x, y))