import pygame, random

WIDTH = 800
HEIGHT = 600
BLACK = (0,0,0)
WHITE = (255,255,255)



class Enemies(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Cargar todas las imágenes de la animación
        self.walk_frames = [
            pygame.transform.flip(
                pygame.transform.scale(
                    pygame.image.load(f"assets/img/enemies/zombie/male/walk/Walk ({i}).png").convert(),
                    (60, 80)  # ⬅️ Tamaño nuevo (ancho, alto)
                ),
                True, False  # ⬅️ Flip horizontal, no vertical
            )
            for i in range(1, 5)
        ]

        for frame in self.walk_frames:
            frame.set_colorkey(BLACK)

        self.image_index = 0
        self.image = self.walk_frames[self.image_index]
        self.rect = self.image.get_rect()

        # Posición inicial fuera del borde derecho
        self.rect.x = WIDTH + random.randint(0, 300)
        self.rect.bottom = HEIGHT - 10

        self.speed_x = -0.55  # Velocidad del movimiento hacia la izquiedad del enemigo
        self.animation_speed = 5 # Velocidad con la que cambia cada frame
        self.frame_count = 0

    def update(self):
        self.rect.x += self.speed_x  # Mover enemigo

        # Si el enemigo sale de la pantalla, reaparece a la derecha
        if self.rect.right < 0:
            self.rect.x = WIDTH + random.randint(0, 300)

        # Actualizar animación
        self.frame_count += 1
        if self.frame_count >= self.animation_speed:
            self.frame_count = 0
            self.image_index = (self.image_index + 1) % len(self.walk_frames)
            self.image = self.walk_frames[self.image_index]