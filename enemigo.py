import pygame, random
from configuracion import WIDTH, HEIGHT, BLACK, WHITE
from personaje import Personaje
from sistema_combate import SistemaCombate
from pocion_vida import PocionVida  # Ajusta la ruta si es diferente

enemy_width = 60
enemy_height = 80

class Enemigo(Personaje):
    def __init__(self, x, y, color, imagen, puntos_vida, ataque, defensa, tipo):
        raw_walk_frames = [
            pygame.transform.scale(
                pygame.image.load(f"assets/img/enemies/zombie/male/walk/Walk ({i}).png").convert(),
                (enemy_width, enemy_height)
            )
            for i in range(1, 5)
        ]
        for frame in raw_walk_frames:
            frame.set_colorkey(BLACK)

        self.walk_frames_left = [pygame.transform.flip(frame, True, False) for frame in raw_walk_frames]
        self.walk_frames_right = raw_walk_frames[:]
        self.walk_frames = self.walk_frames_left

        self.image_index = 0
        image_initial = self.walk_frames[self.image_index]

        self.rect = image_initial.get_rect()
        self.rect.x = WIDTH + random.randint(0, 300)
        self.rect.bottom = HEIGHT - 10

        x = self.rect.x
        y = self.rect.y
        color = WHITE
        puntos_vida = 2
        ataque = 6
        defensa = 11
        tipo = "Zombie"
        super().__init__(x, y, color, image_initial, puntos_vida, ataque, defensa)
        self.tipo = tipo

        self.image = image_initial

        self.facing_right = False
        self.speed_x = 1
        self.animation_speed = 5
        self.frame_count = 0

        raw_attack_frames = [
            pygame.transform.scale(
                pygame.image.load(f"assets/img/enemies/zombie/male/attack/Attack ({i}).png").convert(),
                (enemy_width, enemy_height)
            )
            for i in range(1, 8)
        ]
        for frame in raw_attack_frames:
            frame.set_colorkey(BLACK)
        self.attack_frames_left = [pygame.transform.flip(frame, True, False) for frame in raw_attack_frames]
        self.attack_frames_right = raw_attack_frames[:]
        self.attack_frames = self.attack_frames_left

        self.attacking = False
        self.attack_index = 0
        self.attack_speed = 9
        self.attack_count = 0
        self.attack_timer = 0
        self.attack_delay = 60  # Tiempo en frames entre ataques

        self.dead_frames = [
            pygame.transform.scale(
                pygame.image.load(f"assets/img/enemies/zombie/male/dead/Dead ({i}).png").convert(),
                (enemy_width, enemy_height)
            )
            for i in range(1, 12)
        ]
        for frame in self.dead_frames:
            frame.set_colorkey(BLACK)
        self.death_frame_index = 0
        self.death_frame_timer = 0
        self.death_frame_delay = 10

        self.hit_count = 0
        self.is_dead = False

    def update(self, player):
        if self.is_dead:
            self.death_frame_timer += 1
            if self.death_frame_timer >= self.death_frame_delay:
                self.death_frame_timer = 0
                if self.death_frame_index < len(self.dead_frames):
                    self.image = self.dead_frames[self.death_frame_index]
                    self.death_frame_index += 1
                else:
                    if not hasattr(self, 'death_hold_count'):
                        self.death_hold_count = 0
                    self.death_hold_count += 1
                    if self.death_hold_count >= 20:
                        self.kill()
            return

        # ⚠️ Añadir validación para evitar acceso a 'player' si es None
        if player is None or player.is_dead:
            return  # No hacer nada si el jugador está muerto
        
        rango_ataque = 50
        distancia_horizontal = abs(self.rect.centerx - player.rect.centerx)

        if distancia_horizontal <= rango_ataque:
            self.attacking = True
            self.attack_frames = self.attack_frames_right if self.facing_right else self.attack_frames_left
            self.attack_count += 1
            if self.attack_count >= self.attack_speed:
                self.attack_count = 0
                self.attack_index = (self.attack_index + 1) % len(self.attack_frames)
                self.image = self.attack_frames[self.attack_index]

            self.attack_timer += 1
            if self.attack_timer >= self.attack_delay:
                self.attack_timer = 0
                self.realizar_ataque(player)
        else:
            self.attacking = False
            self.attack_count = 0
            self.attack_index = 0
            self.attack_timer = 0

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

    def realizar_ataque(self, jugador):
        if jugador.is_dead:
            return

        # Solo aplicamos daño UNA VEZ
        SistemaCombate.calcular_daño(self, jugador)

    def take_hit(self):
        if not self.is_dead:
            self.hit_count += 1
            if self.hit_count >= 2:
                self.die()

    def die(self):
        self.is_dead = True
        self.death_frame_index = 0

        # Probabilidad de soltar una poción (ej. 40%)
        # Probabilidad de soltar poción
        if random.random() < 0.4:  # 30% de probabilidad
            pocion = PocionVida()  # Crear una nueva poción
            pocion.rect.center = self.rect.center  # Colocar la poción en la posición del enemigo

            # Agregar la poción a los grupos
            self.grupo_objetos.add(pocion)
            self.grupo_todos.add(pocion)


    def pintar(self, screen: pygame.Surface) -> None:
        screen.blit(self.image, self.rect)

    def colision(self, otra) -> bool:
        return self.rect.colliderect(otra.rect)

    def actualizar(self) -> None:
        pass

    def recibir_daño(self, dano: int) -> None:
        """
        Aplica el daño final calculado al enemigo directamente.
        """
        if self.is_dead:
            return
        # Como 'dano' ya está reducido por defensa en SistemaCombate, lo aplicamos directamente
        self.puntos_vida = max(0, self.puntos_vida - dano)
        print(f"{self.tipo} recibió {dano} daño. Salud: {self.puntos_vida}")
        if self.puntos_vida == 0:
            self.die()
