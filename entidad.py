# entidad.py
import pygame
from abc import ABC, abstractmethod

class Entidad(ABC, pygame.sprite.Sprite):
    """
    Clase abstracta que representa una entidad en el juego.
    Versión corregida con implementación correcta de ABC.
    """
    
    def __init__(self, x: int, y: int, color: tuple, imagen: pygame.Surface):
        super().__init__()
        self.x = x
        self.y = y
        self.color = color
        self.image  = imagen
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    @abstractmethod
    def pintar(self, screen: pygame.Surface) -> None:
        """Dibuja la entidad en la pantalla"""
        pass

    @abstractmethod
    def colision(self, otra: "Entidad") -> bool:
        """Detecta colisiones con otra entidad"""
        pass

    @abstractmethod
    def actualizar(self) -> None:
        """Actualiza el estado de la entidad"""
        pass

# Clase abstracta Objeto
class Objeto(ABC):
    def __init__(self, nombre: str):
        self.nombre = nombre

    @abstractmethod
    def usar(self, objetivo):
        """Método abstracto para usar el objeto sobre un objetivo"""
        pass

# Clase concreta TrampaExplosiva
class TrampaExplosiva(Objeto):
    def __init__(self):
        super().__init__("Trampa Explosiva")

    def usar(self, objetivo):
        print(f"{self.nombre} activada sobre {objetivo} ¡Boom!")
        # Aquí podrías hacer daño, etc.

# Clase concreta PocionDeVida
class PocionDeVida(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/img/scene/items/chickeLive.png").convert_alpha()  # Carga la imagen correctamente
        self.image = pygame.transform.scale(self.image, (20, 40))  # Ajusta el tamaño aquí
        self.rect = self.image.get_rect()  # Definir el rectángulo para colisiones
        self.rect.center = (0, 0)  # Coloca la poción en el origen o la posición inicial deseada

    def usar(self, objetivo):
        print(f"{self.nombre} usada en {objetivo}. Vida restaurada.")