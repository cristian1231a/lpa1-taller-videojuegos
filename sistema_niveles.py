from escalado_enemigos import EscaladoEnemigos
from typing import List


class SistemaNiveles:
    """
    Gestiona experiencia, subida de nivel y escalado de enemigos.
    """
    def __init__(self, jugador, grupo_enemigos: List):
        self.jugador = jugador
        self.grupo_enemigos = grupo_enemigos
        self.experiencia_para_siguiente = 30  # XP inicial requerida
        self.escalador = EscaladoEnemigos(jugador.nivel_xp.nivel, 0.27) 

    def calcular_experiencia(self, enemigo) -> int:
        """Calcula XP otorgada por derrotar a un enemigo."""
        # Ejemplo: XP base más bonus por nivel enemigo
        xp_base = 95
        return int(xp_base + enemigo.puntos_vida + enemigo.ataque)

    def mejorar_atributos(self):
        # Aumenta vida máxima, ataque y defensa
        self.jugador.puntos_vida_max += 10
        self.jugador.ataque += 9
        self.jugador.defensa += 13
        # Curar al máximo
        self.curar_puntos_vida()
        # Actualizar escalador con nuevo nivel
        self.escalador.nivel_jugador = self.jugador.nivel
        # Incrementar XP requerida (ejponencial)
        self.experiencia_para_siguiente = int(self.experiencia_para_siguiente * 1.5)

    def curar_puntos_vida(self):
        """Rellena la salud del jugador al máximo."""
        self.jugador.puntos_vida = self.jugador.puntos_vida_max

    def actualizar_enemigos(self):
        """Aplica escalado a todos los enemigos según nivel del jugador."""
        factor = self.escalador.calcular_escalado()
        for enemigo in self.grupo_enemigos:
            enemigo.puntos_vida = int(enemigo.puntos_vida * factor)
            enemigo.ataque     = int(enemigo.ataque     * factor)
            enemigo.defensa    = int(enemigo.defensa    * factor)

    def intentar_subir_nivel(self, xp_ganada: int):
        nivel_antes = self.jugador.nivel_xp.nivel
        self.jugador.nivel_xp.agregar_experiencia(xp_ganada)
        nivel_despues = self.jugador.nivel_xp.nivel

        if nivel_despues > nivel_antes:
            self.mejorar_atributos()
            return True
        return False
