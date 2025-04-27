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