import pygame

WIDTH = 800
HEIGHT = 600
BLACK = (0, 0, 0)

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        # === Animaciones ===
        self.walk_frames = [
            pygame.image.load(f"assets/img/player/walk/Walk{i}.png").convert()
            for i in range(1, 9)
        ]
        self.jump_frames = [
            pygame.image.load(f"assets/img/player/jump/Jump{i}.png").convert()
            for i in range(1, 9)
        ]
        self.attack_frames = [
            pygame.image.load(f"assets/img/player/attack1/Attack{i}.png").convert()
            for i in range(1, 5)
        ]

        # Eliminar fondo negro
        for frame in self.walk_frames + self.jump_frames + self.attack_frames:
            frame.set_colorkey(BLACK)

        # === Estado inicial ===
        self.image_index = 0
        self.image = self.walk_frames[self.image_index]
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10

        # Movimiento
        self.speed_x = 0
        self.speed_y = 0
        self.gravity = 1
        self.jump_power = -15
        self.on_ground = True

        # Animación
        self.frame_count = 0
        self.walk_animation_speed = 10
        self.jump_animation_speed = 7
        self.attack_animation_speed = 6

        self.is_jumping = False
        self.is_attacking = False

        self.facing_right = True  # Nueva bandera para dirección

    def update(self, enemies_list):
        keystate = pygame.key.get_pressed()

        # Movimiento horizontal
        self.speed_x = 0
        if keystate[pygame.K_LEFT]:
            self.speed_x = -2
            self.facing_right = False  # Cambia dirección
        if keystate[pygame.K_RIGHT]:
            self.speed_x = 2
            self.facing_right = True  # Cambia dirección

        # Saltar
        if keystate[pygame.K_UP] and self.on_ground and not self.is_jumping:
            self.speed_y = self.jump_power
            self.on_ground = False
            self.is_jumping = True

        # Ataque
        if keystate[pygame.K_SPACE] and not self.is_attacking:
            self.is_attacking = True
            self.frame_count = 0
            self.image_index = 0

        # Movimiento horizontal
        self.rect.x += self.speed_x
        for enemy in enemies_list:
            if self.rect.colliderect(enemy.rect):
                if self.speed_x > 0:
                    self.rect.right = enemy.rect.left
                elif self.speed_x < 0:
                    self.rect.left = enemy.rect.right

        # Movimiento vertical
        self.rect.y += self.speed_y
        if not self.on_ground:
            self.speed_y += self.gravity

        if self.rect.bottom >= HEIGHT - 10:
            self.rect.bottom = HEIGHT - 10
            self.speed_y = 0
            self.on_ground = True
            self.is_jumping = False

        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

        # === Animaciones ===
        self.frame_count += 1
        frame = None

        if self.is_attacking:
            if self.frame_count >= self.attack_animation_speed:
                self.frame_count = 0
                self.image_index += 1
                if self.image_index < len(self.attack_frames):
                    frame = self.attack_frames[self.image_index]
                else:
                    self.is_attacking = False
                    self.image_index = 0
        elif self.is_jumping:
            if self.frame_count >= self.jump_animation_speed:
                self.frame_count = 0
                self.image_index = (self.image_index + 1) % len(self.jump_frames)
            frame = self.jump_frames[self.image_index]
        elif self.speed_x != 0:
            if self.frame_count >= self.walk_animation_speed:
                self.frame_count = 0
                self.image_index = (self.image_index + 1) % len(self.walk_frames)
            frame = self.walk_frames[self.image_index]
        else:
            frame = self.walk_frames[0]
            self.frame_count = 0
            self.image_index = 0

        # Aplicar FLIP según dirección
        if frame:
            if not self.facing_right:
                self.image = pygame.transform.flip(frame, True, False)
            else:
                self.image = frame


        if self.is_attacking:
            for enemy in enemies_list:
                if self.rect.colliderect(enemy.rect):
                    enemy.take_hit()