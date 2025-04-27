# personaje.py
import pygame
from abc import ABC, abstractmethod
from entidades.entidad import Entidad

class Personaje(Entidad, ABC):  # Añadir ABC como clase padre
    def __init__(self, x: int, y: int, color: tuple, imagen: pygame.Surface, 
                 puntos_vida: int, ataque: int, defensa: int):
        super().__init__(x, y, color, imagen)
        self.puntos_vida = puntos_vida
        self.ataque = ataque
        self.defensa = defensa

    @abstractmethod
    def recibir_daño(self, dano: int) -> None:  # Método abstracto corregido
        pass