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

    def update(self):
        # Relacionar vida con corazones (0 a 3 corazones)
        vida_por_corazon = self.jugador.puntos_vida_max / 4
        corazones_actuales = int(self.jugador.puntos_vida / vida_por_corazon)

        # Evitar índices fuera de rango
        corazones_actuales = max(0, min(corazones_actuales, 3))
        self.image = self.live_frames[corazones_actuales]
