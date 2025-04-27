# niveles.py
import pygame, random
from plataforma import Plataforma
from configuracion import WIDTH, HEIGHT
from enemigo import Enemigo
from boss import Boss
from trampa_explosiva import TrampaExplosiva

class Nivel:
    def __init__(
        self,
        back_path,
        floor_path,
        floor_height,
        platforms,
        level_width=None,
        enemy_count: int = 0,
        spawn_bombs: bool = False,
        has_boss: bool = False
    ):
        """
        back_path: ruta al PNG de fondo completo
        floor_path: ruta al PNG de suelo
        floor_height: alto del suelo en píxeles
        platforms: lista de (x, y, w, h) de plataformas
        level_width: ancho deseado del nivel (en píxeles). Si es None, usa todo el fondo.
        enemy_count: cuántos enemigos generar al inicio
        spawn_bombs: si debe ir generando bombas periódicamente
        has_boss: si este nivel es un jefe único en lugar de zombis
        """
        # Carga fondo completo y recorte opcional
        full_bg = pygame.image.load(back_path).convert()
        bg_h = full_bg.get_height()
        if level_width is not None:
            level_width = min(level_width, full_bg.get_width())
            self.background = full_bg.subsurface((0, 0, level_width, bg_h)).copy()
        else:
            self.background = full_bg

        # Suelo
        self.floor_img = pygame.image.load(floor_path).convert_alpha()
        self.scroll_x = 0
        self.level_width = self.background.get_width()
        self.max_scroll = max(0, self.level_width - WIDTH)
        self.floor_height = floor_height

        # Plataformas
        self.plataformas = pygame.sprite.Group()
        # Suelo extiende todo el ancho
        self.plataformas.add(
            Plataforma(0, HEIGHT - floor_height, self.level_width, floor_height)
        )
        for x, y, w, h in platforms:
            if x < self.level_width:
                w = min(w, self.level_width - x)
                self.plataformas.add(Plataforma(x, y, w, h))

        # Lógica de spawn
        self.enemy_count = enemy_count
        self.spawn_bombs = spawn_bombs
        self.has_boss = has_boss
        self._bomb_timer = 0
        self._bomb_period = 2000  # ms entre bombas
        self.jugador = None  # se asignará en setup_entities

    def setup_entities(self, jugador, enemies_list, all_sprites, objetos_sueltos):
        """Si es jefe, genera un Boss; si no, spawnea `enemy_count` zombis."""
        # Guardamos referencia al jugador para las bombas
        self.jugador = jugador

        if self.has_boss:
            b = Boss(
                x=self.level_width // 2,
                y=HEIGHT - self.floor_height - 100,
                color=(255, 255, 255),
                imagen=pygame.Surface((100, 100)),
                puntos_vida=200,
                ataque=20,
                defensa=5,
                tipo="Zombie Boss"
            )
            b.grupo_objetos = objetos_sueltos
            b.grupo_todos = all_sprites
            all_sprites.add(b)
            enemies_list.add(b)
        else:
            for _ in range(self.enemy_count):
                x = random.randint(50, self.level_width - 50)
                e = Enemigo(
                    x=x,
                    y=HEIGHT - self.floor_height - 50,
                    color=(255, 255, 255),
                    imagen=pygame.Surface((50, 50)),
                    puntos_vida=50,
                    ataque=8,
                    defensa=2,
                    tipo="Zombie"
                )
                e.grupo_objetos = objetos_sueltos
                e.grupo_todos = all_sprites
                all_sprites.add(e)
                enemies_list.add(e)

    def update_logic(self, dt, objetos_sueltos, all_sprites):
        """Si `spawn_bombs`, genera una trampa explosiva cada `_bomb_period` ms en la altura del jugador."""
        if not self.spawn_bombs or self.jugador is None:
            return
        self._bomb_timer += dt
        if self._bomb_timer >= self._bomb_period:
            self._bomb_timer = 0
            # Elegimos una x dentro de la vista actual
            x_world = random.randint(self.scroll_x, self.scroll_x + WIDTH)
            # Generar bomba a la altura del jugador
            y_world = 550
            bomb = TrampaExplosiva(x_world, y_world)
            objetos_sueltos.add(bomb)
            all_sprites.add(bomb)

    def update(self, dx):
        self.scroll_x = max(0, min(self.scroll_x + dx, self.max_scroll))
        for plat in self.plataformas:
            plat.scroll_x = self.scroll_x

    def draw(self, screen):
        screen.blit(self.background, (-self.scroll_x, 0))
        screen.blit(
            self.floor_img,
            (-self.scroll_x, HEIGHT - self.floor_img.get_height())
        )
        for plat in self.plataformas:
            screen.blit(plat.image, (plat.rect.x - self.scroll_x, plat.rect.y))


def cargar_todos_los_niveles():
    niveles = []
    # Nivel 1: 10 zombies, sin bombas
    niveles.append(Nivel(
        back_path="assets/img/scene/scene1/back.png",
        floor_path="assets/img/scene/scene1/front.png",
        floor_height=10,
        platforms=[(300,450,200,20),(600,350,200,20),(900,250,200,20)],
        level_width=2000,
        enemy_count=10,
        spawn_bombs=False,
        has_boss=False
    ))
    # Nivel 2: 25 zombies + bombas constantes
    niveles.append(Nivel(
        back_path="assets/img/scene/scene1/fondo_nivel_2.png",
        floor_path="assets/img/scene/scene1/front.png",
        floor_height=10,
        platforms=[(200,480,150,20),(500,380,150,20),(800,280,150,20)],
        level_width=2000,
        enemy_count=25,
        spawn_bombs=True,
        has_boss=False
    ))
    # Nivel 3: jefe + bombas
    niveles.append(Nivel(
        back_path="assets/img/scene/scene1/fondo_nivel_3.png",
        floor_path="assets/img/scene/scene1/front.png",
        floor_height=10,
        platforms=[(250,460,180,20),(550,360,180,20),(850,260,180,20)],
        level_width=2000,
        enemy_count=0,
        spawn_bombs=True,
        has_boss=True
    ))
    return niveles