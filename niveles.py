import pygame
from plataforma import Plataforma
from configuracion import WIDTH, HEIGHT

class Nivel:
    def __init__(self, back_path, floor_path, floor_height, platforms, level_width=None):
        """
        back_path: ruta al PNG de fondo completo
        floor_path: ruta al PNG de suelo
        floor_height: alto del suelo en píxeles
        platforms: lista de (x, y, w, h) de plataformas
        level_width: ancho deseado del nivel (en píxeles). Si es None, usa todo el fondo.
        """
        # Carga fondo completo
        full_bg = pygame.image.load(back_path).convert()
        bg_h = full_bg.get_height()
        
        # Si level_width está dado, recortamos el fondo:
        if level_width is not None:
            # Nos aseguramos de no pasarnos del ancho real:
            level_width = min(level_width, full_bg.get_width())
            # Creamos un subsurface del ancho deseado:
            self.background = full_bg.subsurface((0, 0, level_width, bg_h)).copy()
        else:
            self.background = full_bg
        
        # Cargamos la imagen de suelo (podrías recortarla igual si fuera muy ancha)
        self.floor_img  = pygame.image.load(floor_path).convert_alpha()
        
        # Scroll de nivel
        self.scroll_x    = 0
        self.level_width = self.background.get_width()
        self.max_scroll  = max(0, self.level_width - WIDTH)
        
        # Altura del suelo en píxeles
        self.floor_height = floor_height
        
        # Grupo de plataformas (incluye suelo)
        self.plataformas = pygame.sprite.Group()
        # Plataforma sólida de suelo (extiende todo el ancho del nivel)
        self.plataformas.add(
            Plataforma(0, HEIGHT - floor_height, self.level_width, floor_height)
        )
        # Plataformas adicionales (x, y, ancho, alto)
        for x, y, w, h in platforms:
            # Si alguna plataforma cae fuera del level_width, la puedes ignorar o ajustarla:
            if x < self.level_width:
                w = min(w, self.level_width - x)
                self.plataformas.add(Plataforma(x, y, w, h))

    def update(self, dx):
        self.scroll_x = max(0, min(self.scroll_x + dx, self.max_scroll))
        for plat in self.plataformas:
            plat.scroll_x = self.scroll_x

    def draw(self, screen):
        # Dibuja fondo recortado o completo
        screen.blit(self.background, (-self.scroll_x, 0))
        # Dibuja suelo
        screen.blit(
            self.floor_img,
            (-self.scroll_x, HEIGHT - self.floor_img.get_height())
        )
        # Dibuja plataformas “visibles”
        for plat in self.plataformas:
            screen.blit(plat.image, (plat.rect.x - self.scroll_x, plat.rect.y))


# Función de conveniencia para crear tus tres niveles
def cargar_todos_los_niveles():
    niveles = []
    # Nivel 1
    niveles.append(
        Nivel(
            back_path = "assets/img/scene/scene1/back.png",
            floor_path = "assets/img/scene/scene1/front.png",
            floor_height = 10,
            platforms = [
                (300, 450, 200, 20),
                (600, 350, 200, 20),
                (900, 250, 200, 20),
            ],
            level_width = 2000
        )
    )
    # Nivel 2 (ajusta rutas y coords)
    niveles.append(
        Nivel(
            back_path = "assets/img/scene/scene1/fondo_nivel_2.png",
            floor_path = "assets/img/scene/scene1/front.png",
            floor_height = 10,
            platforms = [
                (200, 480, 150, 20),
                (500, 380, 150, 20),
                (800, 280, 150, 20),
            ],
            level_width = 2000
        )
    )
    # Nivel 3 (ajusta rutas y coords)
    niveles.append(
        Nivel(
            back_path = "assets/img/scene/scene1/fondo_nivel_3.png",
            floor_path = "assets/img/scene/scene1/front.png",
            floor_height = 10,
            platforms = [
                (250, 460, 180, 20),
                (550, 360, 180, 20),
                (850, 260, 180, 20),
            ],
            level_width = 2000
        )
    )
    return niveles
