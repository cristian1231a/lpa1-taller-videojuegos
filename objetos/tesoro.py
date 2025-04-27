# tesoro.py
import pygame
import random
from objetos.objeto import Objeto

class Tesoro(pygame.sprite.Sprite, Objeto):
    # Probabilidad de que al morir un enemigo suelte un tesoro
    PROBABILIDAD_APARICION = 0.2

    # marca que éste objeto es consumible
    es_consumible = True

    def __init__(self, x: int, y: int):
        # Inicializamos el nombre en la parte de Objeto
        Objeto.__init__(self, "Tesoro")
        # Inicializamos el sprite
        pygame.sprite.Sprite.__init__(self)

        # Rango del valor del tesoro
        self.valor = random.randint(20, 500)

        # Cargamos la imagen y ajustamos el rect
        self.image = pygame.image.load("assets/img/scene/items/tesoro.png").convert_alpha()
        self.rect = self.image.get_rect(center=(x, y))

        # Marcar si ya se recogió
        self._recogido = False

    def usar(self, objetivo):
        """
        Cuando el jugador 'usa' el tesoro,
        le suma su valor al dinero y lo elimina.
        """
        if not self._recogido:
            objetivo.dinero += self.valor
            print(f"¡Recogiste un tesoro de {self.valor} monedas!")
            self._recogido = True
            self.kill()