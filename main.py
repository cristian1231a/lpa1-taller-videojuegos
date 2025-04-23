# programa principal
import pygame
import sys
import random
from configuracion import WIDTH, HEIGHT, FPS
from jugador import Jugador
from enemigo import Enemigo
from escenario import Escenario
from plataforma import Plataforma
from corazones import Corazones
from nivel_xp import NivelXP
from nivel_escudo import BarraEscudo
from puntuacion import Puntuacion
from billetera import Billetera
from condicion_victoria import CondicionVictoria
from screen_inicio import mostrar_pantalla_inicio    
from trampa_explosiva import TrampaExplosiva
from tienda import Tienda
from tesoro import Tesoro

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie Vs Ninja")
clock = pygame.time.Clock()

TRAP_DROP_CHANCE = 0.25

# Cargar y reproducir música de fondo
pygame.mixer.music.load("assets/sounds/sonidoDeFondo.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# Configuración inicial
escenario = Escenario()
jugador = Jugador()
plataforma = Plataforma(0, 0, HEIGHT, WIDTH)  # Plataforma en la parte inferior
corazones = Corazones(jugador)  # Se pasa el jugador como referencia
barra_escudo = BarraEscudo(jugador)
grupo_particulas_xp = pygame.sprite.Group()
puntuacion = Puntuacion(jugador)
billetera = Billetera(jugador)
nivel = jugador.nivel_xp
cond_victoria = CondicionVictoria(jugador, exploracion_requerida=5, puntaje_requerido=400)
areas_exploradas = 0  # Lógica para incrementarlo cuando el jugador avance de área
tienda = Tienda(WIDTH, HEIGHT, jugador)
juego_pausado = False

# Carga de íconos
icon_atk = pygame.image.load("assets/img/scene/statistics/ninja_attack_icon.png").convert_alpha()
icon_def = pygame.image.load("assets/img/scene/statistics/ninja_defense_icon.png").convert_alpha()

# Escalado de íconos
icon_size = (27, 27)
icon_atk = pygame.transform.scale(icon_atk, icon_size)
icon_def = pygame.transform.scale(icon_def, icon_size)

# Grupos de sprites
objetos_sueltos = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
enemies_list = pygame.sprite.Group()

all_sprites.add(jugador, corazones)

# Crear enemigos con posiciones reales
for i in range(20):
    enemigo = Enemigo(
        x=100 + i * 200,
        y=HEIGHT - 150,
        color=(255, 255, 255),
        imagen=pygame.Surface((50, 50)),
        puntos_vida=50,
        ataque=8,
        defensa=2,
        tipo="Zombie"
    )
    enemigo.grupo_objetos = objetos_sueltos
    enemigo.grupo_todos = all_sprites
    all_sprites.add(enemigo)
    enemies_list.add(enemigo)

# Ahora que enemies_list ya existe, instanciamos el sistema de niveles
from sistema_niveles import SistemaNiveles
sistema_niveles = SistemaNiveles(jugador, enemies_list)

# Mostrar pantalla de inicio
mostrar_pantalla_inicio(screen)

# Bucle principal
running = True
while running:
    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_h:
                tienda.mostrar = not tienda.mostrar
                juego_pausado = tienda.mostrar
                print("Tienda activada:", tienda.mostrar)

    # Si estamos en tienda, no actualizamos el juego
    if juego_pausado:
        # Dibujar interfaz de tienda
        tienda.dibujar_boton(screen)
        tienda.dibujar_tienda(screen)
        pygame.display.flip()
        clock.tick(FPS)
        continue

    # 1) Verificar victoria antes que nada
    if cond_victoria.verificar_victoria(areas_exploradas):
        cond_victoria.dibujar(screen)
        pygame.display.flip()
        clock.tick(FPS)
        continue

    # Actualizar lógica de juego
    enemigos_vivos = [e for e in enemies_list if not e.is_dead]
    jugador.update(enemigos_vivos, escenario, plataforma)
    corazones.update()

    # Procesar muerte de enemigos y drops
    for enemy in list(enemies_list):
        if enemy.is_dead and enemy.death_frame_index >= len(enemy.dead_frames):
            # XP y posible subida de nivel
            xp = sistema_niveles.calcular_experiencia(enemy)
            if sistema_niveles.intentar_subir_nivel(xp):
                jugador.nivel_xp.agregar_experiencia(xp)
                print("¡Subiste de nivel!")
            # Puntuación y dinero
            jugador.puntuacion += 20
            monedas = random.randint(2, 8)
            jugador.dinero += monedas
            print(f"¡Obtuviste {monedas} monedas!")
            # Trampa explosiva
            if random.random() < TRAP_DROP_CHANCE:
                trap = TrampaExplosiva(enemy.rect.centerx, enemy.rect.centery)
                objetos_sueltos.add(trap)
                all_sprites.add(trap)
            # Tesoro
            if random.random() < Tesoro.PROBABILIDAD_APARICION:
                tesoro = Tesoro(enemy.rect.centerx, enemy.rect.centery)
                objetos_sueltos.add(tesoro)
                all_sprites.add(tesoro)
            # Escalado de enemigos vivos
            sistema_niveles.actualizar_enemigos()
            # Finalmente eliminar enemigo
            enemy.kill()
            enemies_list.remove(enemy)
        else:
            enemy.update(jugador if not jugador.is_dead else None)

    # Colisiones con objetos sueltos
    current_time = pygame.time.get_ticks()
    for obj in list(objetos_sueltos):
        if isinstance(obj, TrampaExplosiva):
            obj.update(current_time, jugador)
        elif jugador.rect.colliderect(obj.rect):
            jugador.agregar_al_inventario(obj)
            obj.kill()
            objetos_sueltos.remove(obj)
            all_sprites.remove(obj)

    # Dibujado
    screen.fill((0, 0, 0))
    escenario.draw(screen)
    plataforma.draw(screen)
    for spr in all_sprites:
        if hasattr(spr, 'pintar'):
            spr.pintar(screen)
        else:
            screen.blit(spr.image, spr.rect)
    # Sangre enemigos
    for e in enemies_list:
        if e.mostrar_sangre and e.sangre_index > 0:
            blood = e.sangre_frames[e.sangre_index-1]
            pos = blood.get_rect(center=e.sangre_pos)
            screen.blit(blood, pos)

    # Interfaces
    jugador.dibujar_inventario(screen)
    jugador.nivel_xp.mostrar_barra_xp(screen, 300)
    barra_escudo.mostrar_barra_escudo(screen)
    puntuacion.dibujar(screen)
    billetera.dibujar(screen)
    # Estadísticas ninja
    font = pygame.font.Font(None, 24)
    txt_atk = font.render(str(jugador.ataque), True, (255,90,30))
    txt_def = font.render(str(jugador.defensa), True, (100,200,255))
    # Calcular posiciones...
    spacing = 80
    block_w = icon_size[0] + 5 + max(txt_atk.get_width(), txt_def.get_width())
    total_w = block_w*2 + spacing
    x0 = (WIDTH - total_w)//2
    y0 = 50
    # Dibujar
    screen.blit(icon_atk, (x0, y0))
    screen.blit(txt_atk, (x0+icon_size[0]+5, y0+(icon_size[1]-txt_atk.get_height())//2))
    x1 = x0 + block_w + spacing
    screen.blit(icon_def, (x1, y0))
    screen.blit(txt_def, (x1+icon_size[0]+5, y0+(icon_size[1]-txt_def.get_height())//2))

    # Mostrar tienda si activada (botón + UI)
    tienda.dibujar_boton(screen)
    tienda.dibujar_tienda(screen)

    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
