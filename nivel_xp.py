import pygame

class NivelXP:
    def __init__(self):
        self.nivel = 1
        self.experiencia_actual = 0
        self.experiencia_maxima = 100

    def agregar_experiencia(self, cantidad):
        self.experiencia_actual += cantidad
        while self.experiencia_actual >= self.experiencia_maxima:
            self.subir_nivel()

    def subir_nivel(self):
        self.experiencia_actual -= self.experiencia_maxima
        self.nivel += 1
        self.experiencia_maxima = int(self.experiencia_maxima * 1.5)

    def mostrar_barra_xp(self, pantalla, ancho_pantalla):
        alto_barra = 20
        x = 250  # Ubicación de la barra
        y = 20   # Ubicación de la barra

        porcentaje_xp = self.experiencia_actual / self.experiencia_maxima
        ancho_barra = int(porcentaje_xp * ancho_pantalla)

        # Fondo gris
        pygame.draw.rect(pantalla, (100, 100, 100), (x, y, ancho_pantalla, alto_barra))

        # Barra verde
        pygame.draw.rect(pantalla, (0, 255, 0), (x, y, ancho_barra, alto_barra))

        # Borde blanco
        pygame.draw.rect(pantalla, (255, 255, 255), (x, y, ancho_pantalla, alto_barra), 2)

        # Fuente para el texto
        fuente = pygame.font.Font(None, 24)

        # Texto de experiencia: "20 / 100"
        texto_xp = f"{self.experiencia_actual} / {self.experiencia_maxima}"
        render_xp = fuente.render(texto_xp, True, (255, 255, 255))
        pantalla.blit(render_xp, (x - render_xp.get_width() - 10, y))

        # Texto de nivel: "Lv.1"
        texto_nivel = f"Lv.{self.nivel}"
        render_nivel = fuente.render(texto_nivel, True, (255, 255, 255))
        pantalla.blit(render_nivel, (x + ancho_pantalla + 10, y))