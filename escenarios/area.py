from abc import ABC, abstractmethod
from typing import List
from entidades.entidad import Entidad

class Area(ABC):
    def __init__(self):
        self.elementos: List['Entidad'] = []  # Lista de entidades (enemigos, objetos, etc.)

    @abstractmethod
    def generar_elementos(self):
        """Método abstracto para generar elementos específicos del área."""
        pass

    def agregar_elemento(self, elemento: 'Entidad'):
        """Añade una entidad al área."""
        self.elementos.append(elemento)