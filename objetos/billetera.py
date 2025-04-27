import pygame

class Billetera:
    def __init__(self, jugador):
        self.jugador = jugador
        self.font = pygame.font.SysFont("consolas", 24, bold=True)
        self.shuriken_img = pygame.image.load("assets/img/scene/money/shuriken_money.png").convert_alpha()
        self.shuriken_img = pygame.transform.scale(self.shuriken_img, (32, 32))  # Tamaño ajustado
    
    def dibujar(self, screen):
        dinero = self.jugador.dinero  # Asegúrate que el jugador tenga un atributo "dinero"
        texto = self.font.render(f"{dinero}", True, (255, 255, 255))
        x = screen.get_width() - 110
        y = 80
        screen.blit(self.shuriken_img, (x, y))
        screen.blit(texto, (x + 40, y + 4))  # Ajusta el texto al lado del ícono
