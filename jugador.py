import pygame
from entidad import Entidad
from personaje import Personaje
from sistema_combate import SistemaCombate

class Jugador(Personaje):
    def __init__(self):
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

        sheet = pygame.image.load("assets/img/player/Dead.png").convert()
        sheet.set_colorkey((0, 0, 0))
        sw, sh = sheet.get_size()
        num_frames = sw // sh
        self.death_frames = []
        for i in range(num_frames):
            frame = sheet.subsurface(pygame.Rect(i * sh, 0, sh, sh)).copy()
            self.death_frames.append(frame)

        for frame in self.walk_frames + self.jump_frames + self.attack_frames + self.death_frames:
            frame.set_colorkey((0, 0, 0))

        imagen_inicial = self.walk_frames[0]
        x_inicial = 800 // 2
        y_inicial = 600 - 10
        color_dummy = (255, 255, 255)
        puntos_vida_inicial = 100
        ataque_inicial = 10
        defensa_inicial = 2

        super().__init__(x_inicial, y_inicial, color_dummy, imagen_inicial,
                         puntos_vida_inicial, ataque_inicial, defensa_inicial)

        self.rect.centerx = x_inicial
        self.rect.bottom = y_inicial

        self.speed_x = 0
        self.speed_y = 0
        self.gravity = 0.8
        self.jump_power = -17
        self.on_ground = True

        self.frame_count = 0
        self.walk_animation_speed = 12
        self.jump_animation_speed = 7
        self.attack_animation_speed = 6
        self.death_animation_speed = 10
        self.image_index = 0
        self.is_jumping = False
        self.is_attacking = False
        self.facing_right = True

        self.tipo = "Jugador"
        self.daño_aplicado = False  # ← Nuevo: controlar un solo ataque por animación
        self.is_dead = False
        self.death_frame_index = 0
        self.death_frame_timer = 0
        self.death_frame_delay = self.death_animation_speed

        self.nivel = 1
        self.experiencia = 0
        self.inventario = []
        self.dinero = 100
        self.capas_defensa = 0
        self.puntos_vida_max = puntos_vida_inicial

    def obtener_hitbox_ataque(self):
        extension = 20
        if self.facing_right:
            return pygame.Rect(self.rect.right, self.rect.top, extension, self.rect.height)
        else:
            return pygame.Rect(self.rect.left - extension, self.rect.top, extension, self.rect.height)

    def update(self, enemies_list):
        if self.is_dead:
            self.death_frame_timer += 1
            if self.death_frame_timer >= self.death_frame_delay:
                self.death_frame_timer = 0
                if self.death_frame_index < len(self.death_frames):
                    old_centerx = self.rect.centerx
                    old_bottom = self.rect.bottom
                    self.image = self.death_frames[self.death_frame_index]
                    self.rect = self.image.get_rect()
                    self.rect.centerx = old_centerx
                    self.rect.bottom = old_bottom
                    self.death_frame_index += 1
                else:
                    if len(self.death_frames) > 0:
                        self.image = self.death_frames[-1]
            return

        keystate = pygame.key.get_pressed()
        self.speed_x = 0
        if keystate[pygame.K_LEFT]:
            self.speed_x = -2
            self.facing_right = False
        if keystate[pygame.K_RIGHT]:
            self.speed_x = 2
            self.facing_right = True
        # Invocara al metodo esquivar en el salto
        if keystate[pygame.K_UP] and self.on_ground:
            self.esquivar()
        if keystate[pygame.K_SPACE] and not self.is_attacking:
            self.atacar()

        self.rect.x += self.speed_x
        for enemy in enemies_list:
            if self.rect.colliderect(enemy.rect):
                dif = enemy.rect.centerx - self.rect.centerx
                if self.speed_x > 0 and dif > 0:
                    self.rect.right = enemy.rect.left
                elif self.speed_x < 0 and dif < 0:
                    self.rect.left = enemy.rect.right

        self.rect.y += self.speed_y
        if not self.on_ground:
            self.speed_y += self.gravity
        if self.rect.bottom >= 600 - 10:
            self.rect.bottom = 600 - 10
            self.speed_y = 0
            self.on_ground = True
            self.is_jumping = False

        if self.rect.right > 800:
            self.rect.right = 800
        if self.rect.left < 0:
            self.rect.left = 0

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

        if frame:
            self.image = pygame.transform.flip(frame, True, False) if not self.facing_right else frame

        if self.is_attacking:
            hitbox = self.obtener_hitbox_ataque()
            for enemy in enemies_list:
                if hitbox.colliderect(enemy.rect) and not self.daño_aplicado:
                    SistemaCombate.calcular_daño(self, enemy)
                    self.daño_aplicado = True  # ← se aplica daño solo una vez

    def atacar(self):
        self.is_attacking = True
        self.frame_count = 0
        self.image_index = 0
        self.daño_aplicado = False  # ← permite ataque nuevo
        print("Jugador ataca.")
        
    def esquivar(self):
        if self.on_ground and not self.is_jumping:
            self.speed_y = self.jump_power
            self.on_ground = False
            self.is_jumping = True
            print("¡Jugador obtiene inmunidad al estar en el aire!")

    def recibir_daño(self, dano: int):
        # Inmune si ya está muerto o está saltando
        if self.is_dead or self.is_jumping:
            return
        self.puntos_vida = max(0, self.puntos_vida - dano)
        print(f"[DAÑO] Salud: {self.puntos_vida}/{self.puntos_vida_max}")
        if self.puntos_vida == 0:
            self.morir()

    def morir(self):
        if not self.is_dead:
            self.is_dead = True
            self.death_frame_index = 0
            self.death_frame_timer = 0
            self.death_position = self.rect.copy()
        print("El jugador ha sido derrotado.")

    def pintar(self, screen: pygame.Surface) -> None:
        screen.blit(self.image, self.rect)

    def colision(self, otra: Entidad) -> bool:
        return self.rect.colliderect(otra.rect)

    def actualizar(self) -> None:
        self.update([])
