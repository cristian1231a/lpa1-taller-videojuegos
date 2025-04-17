# corazones.py
import pygame

class Corazones(pygame.sprite.Sprite):
    def __init__(self, jugador):
        super().__init__()
        self.jugador = jugador
        self.live_frames = [
            pygame.image.load(f"assets/img/lives/lives{i}.png").convert()
            for i in range(1, 5)
        ]
        for frame in self.live_frames:
            frame.set_colorkey((0, 0, 0))
        
        self.image = self.live_frames[3]  # vidas llenas inicialmente
        self.rect = self.image.get_rect(topleft=(20, 10))  # Posición en pantalla

    # corazones.py
    def update(self):
        # Calcular la vida por cada corazón (25% de la salud máxima)
        vida_por_corazon = self.jugador.puntos_vida_max // 4
    
        # Calcular corazones (0-3) basado en salud actual
        if self.jugador.puntos_vida <= 0:
            corazones_actuales = 0  # 0 corazones si está muerto
        else:
            # Ejemplo: salud=25 → 25 / 25 = 1 → 1 corazón (no 0)
            corazones_actuales = (self.jugador.puntos_vida - 1) // vida_por_corazon + 1
    
        # Asegurar que no exceda el rango [0, 3]
        corazones_actuales = max(0, min(corazones_actuales, 3))
        self.image = self.live_frames[corazones_actuales]