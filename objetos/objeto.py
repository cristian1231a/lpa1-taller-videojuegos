# objeto.py
import pygame
from abc import ABC, abstractmethod

# Clase abstracta Objeto
class Objeto(ABC):
    def __init__(self, nombre: str):
        self.nombre = nombre

    @abstractmethod
    def usar(self, objetivo):
        """Método abstracto para usar el objeto sobre un objetivo"""
        pass