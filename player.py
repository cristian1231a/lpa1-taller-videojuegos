import pygame, random

WIDTH = 800
HEIGHT = 600
BLACK = (0,0,0)
WHITE = (255,255,255)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()


         # Cargar todas las imágenes de la animación para caminar
        self.walk_frames = [
            pygame.image.load(f"assets/img/player/walk/Walk{i}.png").convert()
            for i in range(1, 9)  # Ajusta el rango según la cantidad de imágenes que tengas
        ]

        for frame in self.walk_frames:
            frame.set_colorkey(BLACK)


            # Cargar todas las imágenes de la animación para saltar
        self.jump_frames = [
            pygame.image.load(f"assets/img/player/jump/Jump{i}.png").convert()
            for i in range(1, 9)  # Ajusta el rango según la cantidad de imágenes que tengas
        ]

      
        
        for frame in self.jump_frames:
            frame.set_colorkey(BLACK)


        self.image_index = 0  # Índice del fotograma actual
        self.image = self.walk_frames[self.image_index]  # Imagen actual walk
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed_x = 0
        self.speed_y = 0 #Para saltar
        self.gravity = 1 # la fuera de la gravedad
        self.jump_power = -15
        self.on_ground = True


        self.walk_animation_speed = 10 #VELOCIDAD DE LA ANIMACION DE CAMINAR
        self.jump_animation_speed = 7 #VELOCIDAD DE LA ANIMACION DE SALTAR
        self.frame_count = 0  # Contador para cambiar de imagen
        self.is_jumping = False
   
    def update(self):
        self.speed_x = 0

        #CUANDO PRESIONES LA TECLAS DERECHA O IZQQUIERDA EL PLAYER SE MUEVA O CAMINE
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speed_x = -2 #VELOCIDAD DE MOVIMIENTO
        if keystate[pygame.K_RIGHT]:
            self.speed_x = 2#VELOCIDAD DE MOVIMIENTO

         # CUANDO PRESIONE LA TECLA ESPACIO HACER QUE EL PLAYER SALTE
        if keystate[pygame.K_UP] and self.on_ground:
            self.speed_y = self.jump_power
            self.on_ground = False
            self.is_jumping = True


        # APLICAR MOVIMIENTOS
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y


        # GRAVEDAD
        if not self.on_ground:
            self.speed_y += self.gravity

             # Piso (simplificado)
        if self.rect.bottom >= HEIGHT - 10:
            self.rect.bottom = HEIGHT - 10
            self.speed_y = 0
            self.on_ground = True
            self.is_jumping = False


        #PARA QUE EL JUGADOR (PLAYTER) NO SE SALGA DE LA VENTANA CUANDO LO ESTE MOVIENDO
        if self.rect.right > WIDTH: 
            self.rect.right = WIDTH
        if self.rect.left < 0: 
            self.rect.left = 0

            # Actualizar animación si el jugador se está moviendo
        self.frame_count += 1
        if self.is_jumping:
        # Mostrar animación de salto con velocidad separada
            if self.frame_count >= self.jump_animation_speed:
                self.frame_count = 0
                self.image_index = (self.image_index + 1) % len(self.jump_frames)
                self.image = self.jump_frames[self.image_index]

        elif self.speed_x != 0:
            # Animación de caminar con velocidad separada
            if self.frame_count >= self.walk_animation_speed:
                self.frame_count = 0
                self.image_index = (self.image_index + 1) % len(self.walk_frames)
                self.image = self.walk_frames[self.image_index]

        else:
            # Si está quieto, reseteamos animación
            self.image = self.walk_frames[0]
            self.frame_count = 0
            self.image_index = 0

