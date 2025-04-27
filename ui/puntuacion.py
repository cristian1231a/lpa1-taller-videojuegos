import pygame

class Puntuacion:
    def __init__(self, jugador):
        self.jugador = jugador
        self.font = pygame.font.SysFont("consolas", 24, bold=True)
        self.icono = pygame.image.load("assets/img/scene/punctuation/shuriken_puntuacion.png").convert_alpha()  # icono opcional
        self.icono = pygame.transform.scale(self.icono, (32, 32))
    
    def dibujar(self, screen):
        puntos = self.jugador.puntuacion
        texto = self.font.render(f"{puntos}", True, (255, 255, 0))
        x = screen.get_width() - 110
        y = 20
        screen.blit(self.icono, (x, y))
        screen.blit(texto, (x + 40, y + 4))
