import pygame, random

WIDTH = 800
HEIGHT = 600
BLACK = (0,0,0)
WHITE = (255,255,255)

enemie_width = 60  #Ancho del enemigo
enemie_heigth = 80 #Altura del enemigo


class Enemies(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Cargar todas las imágenes de la animación
        self.walk_frames = [
            pygame.transform.flip(
                pygame.transform.scale(
                    pygame.image.load(f"assets/img/enemies/zombie/male/walk/Walk ({i}).png").convert(),
                    (enemie_width, enemie_heigth)  # ⬅️ Tamaño nuevo (ancho, alto)
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


        # ANIMACION PARA CUANDO EL ENEMIGO COMIENCE ATACAR
        self.attack_frames = [
            pygame.transform.flip(
                pygame.transform.scale(
                    pygame.image.load(f"assets/img/enemies/zombie/male/attack/Attack ({i}).png").convert(),
                    (enemie_width, enemie_heigth)  # ⬅️ Tamaño nuevo (ancho, alto)
                ),
                True, False  # ⬅️ Flip horizontal, no vertical
            )
            for i in range(1, 8)
        ]

         

        for frame in self.attack_frames:
            frame.set_colorkey(BLACK)

            self.attacking = False
            self.attack_index = 0
            self.attack_speed = 10  # Ajustá esto si querés que ataque más lento/rápido
            self.attack_count = 0

    def update(self, player):
        if self.attacking:
            # Animación de ataque
            self.attack_count += 1
            if self.attack_count >= self.attack_speed:
                self.attack_count = 0
                self.attack_index = (self.attack_index + 1) % len(self.attack_frames)
                self.image = self.attack_frames[self.attack_index]
        else:
            # Movimiento hacia el jugador
            if player.rect.centerx < self.rect.centerx:
                self.rect.x -= 1  # Ajustá la velocidad si querés
            elif player.rect.centerx > self.rect.centerx:
                self.rect.x += 1

            # Animación de caminar
            self.frame_count += 1
            if self.frame_count >= self.animation_speed:
                self.frame_count = 0
                self.image_index = (self.image_index + 1) % len(self.walk_frames)
                self.image = self.walk_frames[self.image_index]