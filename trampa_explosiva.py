import pygame
from objeto import Objeto

class TrampaExplosiva(pygame.sprite.Sprite, Objeto):
    def __init__(self, x: int, y: int):
        # Inicializar las clases base
        pygame.sprite.Sprite.__init__(self)
        Objeto.__init__(self, "Trampa Explosiva")

        # Cargar y escalar la imagen estática de la trampa
        self.trap_image = pygame.image.load("assets/img/scene/items/tnt.png").convert_alpha()
        self.trap_image = pygame.transform.scale(self.trap_image, (48, 48))
        self.image = self.trap_image
        self.rect = self.image.get_rect(center=(x, y))

        # Cargar animación de explosión
        self.explosion_frames = []
        for i in range(1, 22):  # boom1.png a boom21.png
            frame = pygame.image.load(f"assets/img/sprites/boom/boom{i}.png").convert_alpha()
            # Escalar cada frame a un tamaño razonable
            frame = pygame.transform.scale(frame, (48, 48))
            self.explosion_frames.append(frame)
        
        # Cargar sonido de explosión
        self.explosion_sound = pygame.mixer.Sound("assets/sounds/boom-explosion.mp3")

        # Temporizador inicial
        self.spawn_time = pygame.time.get_ticks()
        self.delay = 2000  # ms hasta explosión

        # Estado de animación
        self.exploding = False
        self.current_frame = 0
        self.frame_delay = 5  # ticks entre frames
        self.frame_timer = 0

        # Parámetros de daño
        self.explosion_radius = 60
        self.damage = 45
        self.damage_applied = False  # Para aplicar daño una sola vez

    def usar(self, jugador):
        """
        Reinicia el temporizador y estado de la trampa.
        """
        self.spawn_time = pygame.time.get_ticks()
        self.exploding = False
        self.current_frame = 0
        self.frame_timer = 0
        self.image = self.trap_image
        print(f"{self.nombre} reactivada. Explotará en {self.delay/1000:.1f}s.")

    def update(self, current_time: int, target):
        """
        Llamar desde el bucle principal con tiempo y jugador.
        Tras el retraso, inicia animación y aplica daño.
        """
        # Iniciar explosión después del delay
        if not self.exploding and current_time - self.spawn_time >= self.delay:
            self.exploding = True
            self.current_frame = 0
            self.frame_timer = 0
            self.damage_applied = False
            # Reproducir sonido al iniciarse la animación
            self.explosion_sound.play()

        # Animación de explosión
        if self.exploding:
            self.frame_timer += 1
            if self.frame_timer >= self.frame_delay:
                self.frame_timer = 0
                if self.current_frame < len(self.explosion_frames):
                    center = self.rect.center
                    self.image = self.explosion_frames[self.current_frame]
                    self.rect = self.image.get_rect(center=center)
                    # Aplicar daño justo en el fotograma medio
                    mid_frame = len(self.explosion_frames) // 2
                    if self.current_frame == mid_frame and not self.damage_applied:
                        dx = abs(self.rect.centerx - target.rect.centerx)
                        dy = abs(self.rect.centery - target.rect.centery)
                        if dx <= self.explosion_radius and dy <= self.explosion_radius:
                            target.recibir_daño(self.damage)

                            # Ralentizar por 1 segundo
                            target.velocidad_actual = 0  # o cualquier velocidad lenta
                            target.tiempo_ralentizado = pygame.time.get_ticks() + 2000  # 1000 ms = 1 segundo
                            
                            print(f"{self.nombre} explotó y causó {self.damage} de daño")
                            print(f"El area de la {self.nombre} te ha aturdido momentáneamente")
                        else:
                            print(f"{self.nombre} explotó sin afectar al jugador")
                        self.damage_applied = True
                    self.current_frame += 1
                else:
                    # Al finalizar animación, aplicar daño
                    dx = abs(self.rect.centerx - target.rect.centerx)
                    dy = abs(self.rect.centery - target.rect.centery)
                    if dx <= self.explosion_radius and dy <= self.explosion_radius:
                        target.recibir_daño(self.damage)

                        # Ralentizar por 1 segundo
                        target.velocidad_actual = 2  # o cualquier velocidad lenta
                        target.tiempo_ralentizado = pygame.time.get_ticks() + 5000  # 1000 ms = 1 segundo

                        print(f"{self.nombre} explotó y causó {self.damage} de daño")
                    else:
                        print(f"{self.nombre} explotó sin afectar al jugador")
                    self.kill()
