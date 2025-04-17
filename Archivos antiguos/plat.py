import pygame

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.image = pygame.image.load("assets/img/scene/scene1/front.png").convert_alpha()
       
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)  # Posición en la pantalla