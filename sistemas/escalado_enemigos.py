class EscaladoEnemigos:
    """
    Aumenta atributos de enemigos en función del nivel del jugador.
    """
    def __init__(self, nivel_jugador: int, porcentaje_aumento: float):
        self.nivel_jugador = nivel_jugador
        self.porcentaje_aumento = porcentaje_aumento  # e.g. 0.1 para 10% por nivel

    def calcular_escalado(self) -> float:
        """Devuelve factor de escalado: 1 + nivel * porcentaje."""
        return 1 + self.nivel_jugador * self.porcentaje_aumento