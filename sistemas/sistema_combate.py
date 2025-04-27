# sistema_combate.py

class SistemaCombate:
    def __init__(self):
        pass  # Estadísticas globales del combate, si hiciera falta

    @staticmethod
    def calcular_daño(atacante, defensor):
        """
        Calcula y aplica el daño que el atacante causa al defensor.
        Devuelve la cantidad de daño infligido.
        """
        # 1) Si el defensor ya está muerto, no hacemos nada
        if getattr(defensor, "is_dead", False):
            return 0

        daño_bruto = atacante.ataque
        # Asegurar al menos 1 de daño
        daño_final = max(1, daño_bruto - defensor.defensa)

        # Aplicar el daño; el propio objeto se encargará de imprimir su estado
        defensor.recibir_daño(daño_final)

        return daño_final
