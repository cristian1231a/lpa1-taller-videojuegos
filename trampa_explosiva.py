# trampa_explosiva.py
from objeto import Objeto

# Clase concreta TrampaExplosiva
class TrampaExplosiva(Objeto):
    def __init__(self):
        super().__init__("Trampa Explosiva")

    def usar(self, objetivo):
        print(f"{self.nombre} activada sobre {objetivo} ¡Boom!")
        # Aquí podrías hacer daño, etc.