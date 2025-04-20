import pygame
from entidad import Entidad
from personaje import Personaje
from sistema_combate import SistemaCombate
from configuracion import WIDTH, HEIGHT

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
        # Carga animación de protección
        self.protect_frames = [
            pygame.image.load(f"assets/img/player/protection/protection{i}.png").convert()
            for i in range(1, 3)   # asumo 2 frames: protection1.png y protection2.png
        ]
        for f in self.protect_frames:
            f.set_colorkey((0, 0, 0))

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
        self.scroll_x = 0
        

        self.escudo = 25  # Escudo básico, o cualquier valor inicial
        self.escudo_max = 25  # Escudo máximo, para escudo básico

        # O si el jugador puede tener un escudo avanzado:
        def activar_escudo_avanzado(self):
            self.escudo = 50  # Cambiar a escudo avanzado
            self.escudo_max = 50

        super().__init__(x_inicial, y_inicial, color_dummy, imagen_inicial,
                         puntos_vida_inicial, ataque_inicial, defensa_inicial)

        self.rect.centerx = x_inicial
        self.rect.bottom = y_inicial

        self.scroll_x = 0  # reset en cada frame

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
        
        # Estado de defensa
        self.is_defending = False
        self.defend_frame_index = 0
        self.defend_frame_timer = 0
        self.defend_frame_delay = 8  # controla velocidad de la animación de bloqueo
        # NUEVO: para detectar solo el flanco de bajada/subida de Z
        self._z_was_pressed = False
        
        self.puntuacion = 0
        self.puntuacion += 0

        self.nivel = 1
        self.experiencia = 0
        self.inventario = []  # Lista de inventario
        self.dinero = 100
        self.capas_defensa = 0
        self.puntos_vida_max = puntos_vida_inicial

    def obtener_hitbox_ataque(self):
        extension = 20
        if self.facing_right:
            return pygame.Rect(self.rect.right, self.rect.top, extension, self.rect.height)
        else:
            return pygame.Rect(self.rect.left - extension, self.rect.top, extension, self.rect.height)

    def update(self, enemies_list, escenario, plataforma):
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
        self.scroll_x = 0
        SCROLL_MARGIN = 200  # Límite a partir del cual se hace scroll

        if keystate[pygame.K_LEFT]:
            self.speed_x = -1
            self.facing_right = False
            if self.rect.centerx > SCROLL_MARGIN or escenario.scroll_x <= 0:
                self.rect.x += self.speed_x  # Mover jugador
            else:
                escenario.update(self.speed_x)  # Scroll escenario
                plataforma.rect.x -= self.speed_x  # Scroll plataforma (en sentido contrario)
                self.scroll_x = min(3160 - WIDTH, self.scroll_x + self.speed_x)


        if keystate[pygame.K_RIGHT]:
            self.speed_x = 1
            self.facing_right = True
            if self.rect.centerx < WIDTH - SCROLL_MARGIN or escenario.scroll_x >= escenario.max_scroll:
             self.rect.x += self.speed_x  # Mover jugador
            else:
                escenario.update(self.speed_x)  # Scroll escenario
                plataforma.rect.x -= self.speed_x  # Scroll plataforma (en sentido contrario)
                self.scroll_x = min(3160 - WIDTH, self.scroll_x + self.speed_x)
                


        # Invocara al metodo esquivar en el salto
        if keystate[pygame.K_UP] and self.on_ground:
            self.esquivar()
        if keystate[pygame.K_SPACE] and not self.is_attacking:
            self.atacar()
        # ---- DEFENSA con Z: solo en transición NO pulsado → pulsado ----
        z_pressed = keystate[pygame.K_z]
        # Si Z está presionado y condiciones permiten defensa
        if z_pressed:
            if not self.is_defending and self.on_ground and not self.is_attacking and not self.is_jumping:
                self.is_defending = True
                self.defend_frame_index = 0
                self.defend_frame_timer = 0
                print("¡Jugador se defiende!")
        else:
            if self.is_defending:
                self.is_defending = False
                self.defend_frame_index = 0
                self.defend_frame_timer = 0
                print("Jugador deja de defenderse.")

        # Guardar el estado actual de Z para la siguiente iteración
        self._z_was_pressed = z_pressed

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
        
        if self.is_defending:
            # Reproducir frames de protección
            self.defend_frame_timer += 1
            if self.defend_frame_timer >= self.defend_frame_delay:
                self.defend_frame_timer = 0
                self.defend_frame_index += 1
                if self.defend_frame_index < len(self.protect_frames):
                    frame = self.protect_frames[self.defend_frame_index]
                else:
                    # reiniciar animación si sigue defendiendo
                    self.defend_frame_index = 0
                    frame = self.protect_frames[self.defend_frame_index]
        elif self.is_attacking:
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



        # En tu ciclo principal del juego, dentro del bucle de eventos:
        # Captura la entrada del teclado para usar objetos
        keys = pygame.key.get_pressed()
        
        if keys[pygame.K_1]:  # Si presionas '1'
            self.usar_objeto(0)  # Usar el objeto en la ranura 1
        elif keys[pygame.K_2]:  # Si presionas '2'
            self.usar_objeto(1)  # Usar el objeto en la ranura 2
        elif keys[pygame.K_3]:  # Si presionas '3'
            self.usar_objeto(2)  # Usar el objeto en la ranura 3
        elif keys[pygame.K_4]:  # Si presionas '4'
            self.usar_objeto(3)  # Usar el objeto en la ranura 4

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
            
    def defender(self):
        # Solo desde el suelo, sin estar atacando ni saltando
        if self.on_ground and not self.is_attacking and not self.is_jumping:
            self.is_defending = True
            self.defend_frame_index = 0
            self.defend_frame_timer = 0
            print("¡Jugador se defiende!")


    def recibir_daño(self, dano: int):
        # inmune si salta o está muerto
        if self.is_dead or self.is_jumping:
            return

        # Si tiene escudo, reduce el daño del escudo primero
        if self.escudo > 0:
            if dano < self.escudo:
                self.escudo -= dano  # Reducir el escudo por el daño recibido
                print(f"[ESCUDO] Escudo: {self.escudo}/{self.escudo_max}")
                dano = 0  # No hay daño restante, ya se absorbió todo el daño con el escudo
            else:
                # Si el daño es mayor que el escudo, se reduce el escudo a 0 y el resto va a la vida
                dano -= self.escudo
                self.escudo = 0
                print(f"[ESCUDO] Escudo agotado. Escudo: {self.escudo}/{self.escudo_max}")

        # Si no queda escudo, reducir los puntos de vida
        if dano > 0:
            self.puntos_vida = max(0, self.puntos_vida - dano)
            print(f"[DAÑO] Salud: {self.puntos_vida}/{self.puntos_vida_max}")

        # Si se quedó sin vida, el jugador muere
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

    # Método para actualizar el jugador
    def actualizar(self) -> None:
        # Llamamos al método update de la clase base (para movimiento, colisiones, etc.)
        self.update([])  # Actualiza el jugador con las acciones necesarias (puedes añadir más parámetros si es necesario)

        # Llamamos al método para usar objetos
        self.usar_objeto()

    

    # METODO PARA mostrar el inventario de pantalla
    def dibujar_inventario(self, screen: pygame.Surface):
        slot_size = 40
        espacio = 10
        x_inicial = 30
        y_inicial = 120

        font = pygame.font.SysFont(None, 20)

        for i in range(4):
            y = y_inicial + i * (slot_size + espacio)
            rect = pygame.Rect(x_inicial, y, slot_size, slot_size)
            pygame.draw.rect(screen, (200, 200, 200), rect, 2)  # Borde gris

            # Evitar IndexError si el slot aún no está ocupado
            item = self.inventario[i] if i < len(self.inventario) else None

            if item and hasattr(item, "image"):
                imagen_escalada = pygame.transform.scale(item.image, (slot_size - 4, slot_size - 4))
                screen.blit(imagen_escalada, (x_inicial + 2, y + 2))
            elif item:
                texto = font.render(str(item), True, (255, 255, 255))
                screen.blit(texto, (x_inicial + 5, y + 10))

            # Mostrar número del slot (1 a 4) en la esquina inferior derecha
            numero = font.render(str(i + 1), True, (180, 180, 180))  # color gris claro
            numero_rect = numero.get_rect(bottomright=(x_inicial + slot_size - 2, y + slot_size - 2))
            screen.blit(numero, numero_rect)

    # METODO PARA AGREGAR AL INVENTARIO EL OBJETO
    def agregar_al_inventario(self, item):
        print(f"[DEBUG] Inventario actual: {len(self.inventario)} items")
        if len(self.inventario) < 4:
            self.inventario.append(item)
            print("Objeto agregado al inventario.")
        else:
            print("Inventario lleno. No se pudo agregar el objeto.")



    # MÉTODO PARA USAR EL OBJETO (iterando de atrás hacia adelante)
       
    def usar_objeto(self, index):
        if index < len(self.inventario):
            item = self.inventario[index]  # Obtener el item según el índice

            print(f"Usando objeto en slot {index + 1}: {item}")  # Mensaje de depuración

            # Llamar al método usar del objeto (si existe)
            if hasattr(item, 'usar'):
                item.usar(self)  # El jugador es el objetivo aquí
                print(f"Usando {item} en {self}.")  # Mensaje de depuración

            # Si el objeto es consumible, lo eliminamos del inventario
            if hasattr(item, 'es_consumible') and item.es_consumible:
                # Eliminar el objeto después de usarlo
                self.inventario.pop(index)
                print(f"Objeto {item} eliminado del inventario")  # Mensaje de depuración
        else:
            print("Índice fuera de rango, no hay objeto en ese slot.")