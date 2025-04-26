# pocion_vida.py
import pygame

# Clase concreta PocionDeVida
class PocionVida(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/img/scene/items/chickeLive.png").convert_alpha()  # Carga la imagen correctamente
        self.image = pygame.transform.scale(self.image, (20, 40))  # Ajusta el tamaño aquí
        self.rect = self.image.get_rect()  # Definir el rectángulo para colisiones
        self.rect.center = (0, 0)  # Coloca la poción en el origen o la posición inicial deseada
        self.nombre = "Poción de Vida"
        self.es_consumible = True  # Es un objeto consumible

    def usar(self, objetivo):
        cantidad_cura = 25  # Cantidad de vida a restaurar

        if objetivo.puntos_vida < objetivo.puntos_vida_max:
            objetivo.puntos_vida = min(objetivo.puntos_vida + cantidad_cura, objetivo.puntos_vida_max)
            print("¡Muslo de Pollo consumido! Vida restaurada.")
        else:
            print("La vida ya está completa. No se usó el Muslo de Pollo.")