import pygame, random

WIDTH = 800
HEIGHT = 600
BLACK = (0,0,0)
WHITE = (255,255,255)

enemie_width = 60  # Ancho del enemigo
enemie_heigth = 80  # Altura del enemigo

class Enemies(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # Cargar imágenes raw de la animación de caminar sin flip
        raw_walk_frames = [
            pygame.transform.scale(
                pygame.image.load(f"assets/img/enemies/zombie/male/walk/Walk ({i}).png").convert(),
                (enemie_width, enemie_heigth)
            )
            for i in range(1, 5)
        ]
        for frame in raw_walk_frames:
            frame.set_colorkey(BLACK)

        # Crear conjuntos de animación para ambas direcciones
        self.walk_frames_left = [pygame.transform.flip(frame, True, False) for frame in raw_walk_frames]
        self.walk_frames_right = raw_walk_frames[:]

        self.hit_count = 0  # Contador de golpes recibidos
        self.is_dead = False  # Estado del enemigo

        # Estado inicial: el enemigo mira a la izquierda
        self.facing_right = False
        self.walk_frames = self.walk_frames_left

        self.image_index = 0
        self.image = self.walk_frames[self.image_index]
        self.rect = self.image.get_rect()

        # Posición inicial fuera del borde derecho
        self.rect.x = WIDTH + random.randint(0, 300)
        self.rect.bottom = HEIGHT - 10

        # Velocidad de movimiento y control de animación
        self.speed_x = 1
        self.animation_speed = 5
        self.frame_count = 0

        # Vida
        self.hit_points = 2
        self.is_dying = False

        # Cargar imágenes de la animación de ataque
        raw_attack_frames = [
            pygame.transform.scale(
                pygame.image.load(f"assets/img/enemies/zombie/male/attack/Attack ({i}).png").convert(),
                (enemie_width, enemie_heigth)
            )
            for i in range(1, 8)
        ]

        for frame in raw_attack_frames:
            frame.set_colorkey(BLACK)

        # Cargar animación de muerte
        self.dead_frames = [
            pygame.transform.scale(
                pygame.image.load(f"assets/img/enemies/zombie/male/dead/Dead ({i}).png").convert(),
                (enemie_width, enemie_heigth)
            )
            for i in range(1, 12)
        ]

        for frame in self.dead_frames:
            frame.set_colorkey(BLACK)

        self.attack_frames_left = [pygame.transform.flip(frame, True, False) for frame in raw_attack_frames]
        self.attack_frames_right = raw_attack_frames[:]
        self.attack_frames = self.attack_frames_left

        # Índices y temporizadores de animaciones
        self.death_frame_index = 0
        self.death_frame_timer = 0
        self.death_frame_delay = 10  # Velocidad de animación de muerte

        # Variables de ataque
        self.attacking = False
        self.attack_index = 0
        self.attack_speed = 10
        self.attack_count = 0

    def update(self, player):

        if self.is_dead:
            self.death_frame_timer += 1
            if self.death_frame_timer >= self.death_frame_delay:
                self.death_frame_timer = 0

                if self.death_frame_index < len(self.dead_frames):
                    self.image = self.dead_frames[self.death_frame_index]
                    self.death_frame_index += 1
                else:
                    # Esperar un poco más antes de desaparecer
                    if not hasattr(self, 'death_hold_count'):
                        self.death_hold_count = 0
                    self.death_hold_count += 1
                    if self.death_hold_count >= 20:  # puedes ajustar el tiempo de espera
                        self.kill()
            return  # Importante: no seguir ejecutando nada más si está muerto
        

        if self.attacking:
            self.attack_frames = self.attack_frames_right if self.facing_right else self.attack_frames_left
            self.attack_count += 1
            if self.attack_count >= self.attack_speed:
                self.attack_count = 0
                self.attack_index = (self.attack_index + 1) % len(self.attack_frames)
                self.image = self.attack_frames[self.attack_index]
        else:
            if player.rect.centerx < self.rect.centerx:
                self.rect.x -= self.speed_x
                if self.facing_right:
                    self.facing_right = False
                    self.image_index = 0
            elif player.rect.centerx > self.rect.centerx:
                self.rect.x += self.speed_x
                if not self.facing_right:
                    self.facing_right = True
                    self.image_index = 0

            self.rect.bottom = HEIGHT - 10
            self.walk_frames = self.walk_frames_right if self.facing_right else self.walk_frames_left

            self.frame_count += 1
            if self.frame_count >= self.animation_speed:
                self.frame_count = 0
                self.image_index = (self.image_index + 1) % len(self.walk_frames)
                self.image = self.walk_frames[self.image_index]

    def take_hit(self):
        if not self.is_dead:
            self.hit_count += 1
            if self.hit_count >= 2:
                self.die()

    def die(self):
        self.is_dead = True
        self.death_frame_index = 0