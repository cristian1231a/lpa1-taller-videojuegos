# programa principal
import pygame
import sys
import random
from configuracion import WIDTH, HEIGHT, FPS
from jugador import Jugador
from enemigo import Enemigo
from boss import Boss
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
from niveles import cargar_todos_los_niveles

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
SCROLL_MARGIN = 200   # debe coincidir con el de Jugador
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
niveles = cargar_todos_los_niveles() # Lista de niveles existentes
cond_victoria = CondicionVictoria(jugador, exploracion_requerida=3, puntaje_requerido=400)
areas_exploradas = 0  # Lógica para incrementarlo cuando el jugador avance de área
tienda = Tienda(WIDTH, HEIGHT, jugador)
juego_pausado = False

# Inicializamos la variable de fin del juego en False
juego_terminado = False

# Cargar niveles
BASE_FLOOR_HEIGHT = niveles[0].floor_height # Altura base en todos los niveles
nivel_actual = 0
nivel = niveles[nivel_actual]

# Establecemos que la condición de victoria por exploración se cumpla al terminar el tercer nivel
exploracion_requerida = len(niveles)  # Es decir, después de completar el tercer nivel

exploracion_requerida

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

all_sprites.add(jugador)

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


    # Crear JEFE FINAL
for i in range(1):
    enemigoBoss = Boss(
        x=100 + i * 200,
        y=HEIGHT - 150,
        color=(255, 255, 255),
        imagen=pygame.Surface((100, 100)),
        puntos_vida=50,
        ataque=8,
        defensa=2,
        tipo="Zombie Boss"
    )
    enemigoBoss.grupo_objetos = objetos_sueltos
    enemigoBoss.grupo_todos = all_sprites
    all_sprites.add(enemigoBoss)
    enemies_list.add(enemigoBoss)


# Ahora que enemies_list ya existe, instanciamos el sistema de niveles
from sistema_niveles import SistemaNiveles
sistema_niveles = SistemaNiveles(jugador, enemies_list)

# Mostrar pantalla de inicio
mostrar_pantalla_inicio(screen)

# Impresiones de condicion de victoria por consola:
mensaje_exploracion_impreso = False

# Bucle principal
running = True
while running:
    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        # ——— doble‐clic en inventario para vender —— sólo dentro de la tienda ——
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and tienda.mostrar:
            mx, my = event.pos
            # coordenadas fijas del inventario en pantalla
            slot_size = 40
            espacio   = 10
            x0, y0    = 30, 120
            for idx in range(4):
                rect = pygame.Rect(x0, y0 + idx*(slot_size+espacio), slot_size, slot_size)
                if rect.collidepoint(mx, my):
                    jugador.vender(idx)
                    break

        # ——— toggle tienda — sólo si el jugador sigue con vida ———
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_x:
            if jugador.puntos_vida > 0:                               # ← NUEVO
                tienda.mostrar = not tienda.mostrar
                juego_pausado  = tienda.mostrar

        # ——— Uso de inventario — sólo si el jugador sigue con vida ——
        elif event.type == pygame.KEYDOWN and jugador.puntos_vida > 0:  # ← NUEVO
            if event.key == pygame.K_1:
                jugador.usar_objeto(0)
            elif event.key == pygame.K_2:
                jugador.usar_objeto(1)
            elif event.key == pygame.K_3:
                jugador.usar_objeto(2)
            elif event.key == pygame.K_4:
                jugador.usar_objeto(3)

    if juego_pausado:
        # — 1) Fondo y escenario —
        screen.fill((0, 0, 0))
        nivel.draw(screen)
    
        # — 2) Sprites (jugador/enemigos) — opcional si quieres verlos detrás de la tienda
        for spr in all_sprites:
            draw_pos = (spr.rect.x - nivel.scroll_x, spr.rect.y)
            if hasattr(spr, 'pintar'):
                orig = spr.rect.copy()
                spr.rect.topleft = draw_pos
                spr.pintar(screen)
                spr.rect = orig
            else:
                screen.blit(spr.image, draw_pos)
    
        # — 3) Interfaz de juego (corazones, inventario, xp, escudo, puntuación, monedas, stats) —
        corazones.update()
        screen.blit(corazones.image, corazones.rect)
    
        jugador.dibujar_inventario(screen)
        jugador.nivel_xp.mostrar_barra_xp(screen, 300)
        barra_escudo.mostrar_barra_escudo(screen)
        puntuacion.dibujar(screen)
        billetera.dibujar(screen)
    
        # (si dibujas también shurikens y stats ninja, repite las mismas líneas que tienes al final del loop)
    
        # — 4) Finalmente la UI de la tienda —
        tienda.dibujar_boton(screen)
        tienda.dibujar_tienda(screen)
    
        # CREAR TEXTO para ataque y defensa (antes de dibujar)
        font = pygame.font.Font(None, 24)
        txt_atk = font.render(str(jugador.ataque), True, (255,90,30))
        txt_def = font.render(str(jugador.defensa), True, (100,200,255))

        # Calcular posiciones
        spacing = 80
        block_w = icon_size[0] + 5 + max(txt_atk.get_width(), txt_def.get_width())
        total_w = block_w*2 + spacing
        x0 = (WIDTH - total_w)//2
        y0 = 50
        x1 = x0 + block_w + spacing

        # Ahora sí dibujar
        screen.blit(icon_atk, (x0, y0))
        screen.blit(txt_atk, (x0+icon_size[0]+5, y0+(icon_size[1]-txt_atk.get_height())//2))
        screen.blit(icon_def, (x1, y0))
        screen.blit(txt_def, (x1+icon_size[0]+5, y0+(icon_size[1]-txt_def.get_height())//2))


        pygame.display.flip()
        clock.tick(FPS)
        continue

    if cond_victoria.verificar_victoria(areas_exploradas):
        # Dibujamos el overlay de victoria/derrota
        cond_victoria.dibujar(screen)
        # ——— Mensaje extra por victoria de puntuación ———
        if cond_victoria.victoria_puntaje:
            print("¡¡¡ Felicidades, has alcanzado la puntuación requerida para ganar !!!")
        pygame.display.flip()
        clock.tick(FPS)
        # ——— Pausa de victoria por puntuación ———
        if cond_victoria.victoria_puntaje:
            # Capturamos el último fotograma como fondo
            fondo_final = screen.copy()
            mostrando_victoria = True
            while mostrando_victoria:
                for evt in pygame.event.get():
                    if evt.type == pygame.QUIT:
                        mostrando_victoria = False
                        running = False
                    elif evt.type == pygame.KEYDOWN and evt.key == pygame.K_ESCAPE:
                        mostrando_victoria = False
                # Volvemos a dibujar fondo + overlay
                screen.blit(fondo_final, (0, 0))
                cond_victoria.dibujar(screen)
                pygame.display.flip()
                clock.tick(FPS)
            # Saltamos el resto del frame para no seguir actualizando el juego
            continue
        

    # Actualizar lógica de juego (colisiones, animaciones…)
    enemigos_vivos = [e for e in enemies_list if not e.is_dead]
    # Pasamos el objeto nivel como 'escenario' y como 'plataforma'
    jugador.update(enemigos_vivos, nivel, nivel)
    
    corazones.update()

    # ——— Cámara siempre centrada en el jugador (dentro de los límites) ———
    # Calculamos una cámara que intente dejar al jugador en el centro de la pantalla:
    offset = jugador.rect.centerx - WIDTH // 2
    # La limitamos para que no se salga del nivel:
    offset = max(0, min(offset, nivel.max_scroll))
    nivel.scroll_x = offset
    

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
            # ——— Victoria por eliminar al Boss ———
            if isinstance(enemy, Boss):
                # Activamos la victoria por matar al Boss
                cond_victoria.victoria_puntaje = True
                # ——— Mensaje extra por victoria al jefe ———
                print("¡¡¡ Felicidades, has derrotado al Jefe Final !!!")
                # Capturamos el estado final para mantenerlo de fondo
                fondo_final = screen.copy()
                # Entramos en bucle de “pausa de victoria” hasta que el jugador cierre o pulse Esc
                mostrando_victoria = True
                while mostrando_victoria:
                    for evt in pygame.event.get():
                        if evt.type == pygame.QUIT:
                            mostrando_victoria = False
                            running = False
                        elif evt.type == pygame.KEYDOWN and evt.key == pygame.K_ESCAPE:
                            mostrando_victoria = False
                    # Redibujamos el último frame y la pantalla de victoria
                    screen.blit(fondo_final, (0, 0))
                    cond_victoria.dibujar(screen)
                    pygame.display.flip()
                    clock.tick(FPS)
                # Al salir de este bucle volvemos al main loop
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

    screen.fill((0, 0, 0))
    nivel.draw(screen)
    # ——— Dibujar sprites compensando el scroll ———
    for spr in all_sprites:
        # calculamos la posición en pantalla restando scroll_x
        draw_pos = (spr.rect.x - nivel.scroll_x, spr.rect.y)
        if hasattr(spr, 'pintar'):
            # temporalmente movemos su rect, pintamos, y lo restauramos
            orig_rect = spr.rect.copy()
            spr.rect.topleft = draw_pos
            spr.pintar(screen)
            spr.rect = orig_rect
        else:
            screen.blit(spr.image, draw_pos)
    # ❤️ Dibujar sangre encima de los enemigos
    for e in enemies_list:
        if e.mostrar_sangre and e.sangre_index > 0:
            blood = e.sangre_frames[e.sangre_index-1]
            # e.sangre_pos está en coordenadas del mundo, así que le aplicamos scroll:
            screen_x, screen_y = e.sangre_pos
            screen_x -= nivel.scroll_x
            # recreamos el rect centrado en la posición en pantalla
            pos = blood.get_rect(center=(screen_x, screen_y))
            screen.blit(blood, pos)
    

    # Interfaces
    corazones.update()         
    screen.blit(corazones.image, corazones.rect)
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

    # ——— Cambio de nivel al llegar al final del mundo ———
    world_width = nivel.background.get_width()
    
    if nivel_actual == 2 and jugador.rect.x >= world_width - jugador.rect.width - 100:
        # Marcamos la victoria por exploración
        cond_victoria.victoria_exploracion = True
        if cond_victoria.victoria_exploracion and not mensaje_exploracion_impreso:
            print("¡¡¡ Felicidades, has escapado de la horda de Zombies !!!")
            mensaje_exploracion_impreso = True
        
    if jugador.rect.x >= world_width - jugador.rect.width:
        nivel_actual += 1
        if nivel_actual < len(niveles):
            # Asigna el nuevo nivel
            nivel = niveles[nivel_actual]
            # Reset scroll y posición del jugador
            nivel.scroll_x = 0
            jugador.rect.x = 0
            jugador.rect.bottom = HEIGHT - BASE_FLOOR_HEIGHT
            jugador.speed_y = 0
        else:
            
            # Fin del último nivel: mostrar pantalla de victoria por exploración o puntaje
            exploracion_actual = nivel_actual + 1  # o la variable que estés usando
            mostrar_victoria = True
            fin_timer = 0
            while mostrar_victoria:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        mostrar_victoria = False

                screen.fill((0, 0, 0))
                cond_victoria.dibujar(screen)
                pygame.display.flip()
                clock.tick(60)
                
                fin_timer += 1
                if fin_timer > 5:  # Segundos a 60 FPS antes de cerrar el juego
                    mostrar_victoria = False

            running = False


    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()