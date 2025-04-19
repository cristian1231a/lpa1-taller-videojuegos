# nivel_escudo.py

import pygame

class BarraEscudo:
    def __init__(self, jugador, ancho_pantalla=100):
        self.jugador = jugador
        self.ancho_pantalla = ancho_pantalla
        self.alto_barra = 20
        self.pos_x = 20  # Posición en X
        self.pos_y = 60  # Posición en Y
        self.fuente = pygame.font.Font(None, 24)  # Fuente para el texto

    def mostrar_barra_escudo(self, pantalla):
        escudo_actual = self.jugador.escudo
        escudo_max = self.jugador.escudo_max

        # Determinar el color de la barra dependiendo del escudo
        if escudo_max > 25:
            color_barra = (212, 175, 55)  # Dorado para escudo avanzado
        else:
            color_barra = (135, 206, 250)  # Azul claro para escudo básico

        # Calcular el largo proporcional de la barra
        ancho_barra = int((escudo_actual / escudo_max) * self.ancho_pantalla)

        # Fondo gris
        pygame.draw.rect(pantalla, (100, 100, 100), (self.pos_x, self.pos_y, self.ancho_pantalla, self.alto_barra))

        # Barra de escudo
        pygame.draw.rect(pantalla, color_barra, (self.pos_x, self.pos_y, ancho_barra, self.alto_barra))

        # Borde blanco
        pygame.draw.rect(pantalla, (255, 255, 255), (self.pos_x, self.pos_y, self.ancho_pantalla, self.alto_barra), 2)

        # Texto opcional con los valores del escudo
        texto_escudo = f"{escudo_actual}/{escudo_max}"
        render_escudo = self.fuente.render(texto_escudo, True, (255, 255, 255))
        pantalla.blit(render_escudo, (self.pos_x + self.ancho_pantalla + 10, self.pos_y))