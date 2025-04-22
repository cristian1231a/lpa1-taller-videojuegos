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

# Escalado (24×24px)
icon_size = (27, 27)
icon_atk = pygame.transform.scale(icon_atk, icon_size)
icon_def = pygame.transform.scale(icon_def, icon_size)

# Grupos de sprites
objetos_sueltos = pygame.sprite.Group()
all_sprites = pygame.sprite.Group()
enemies_list = pygame.sprite.Group()

all_sprites.add(jugador, corazones)





# Crear enemigos con posiciones reales
for i in range(2):
    enemigo = Enemigo(
        x=100 + i * 200,
        y=HEIGHT - 150,  # Posición sobre la plataforma
        color=(255, 255, 255),
        imagen=pygame.Surface((50, 50)),
        puntos_vida=50,
        ataque=8,
        defensa=2,
        tipo="Zombie"
    )
    enemigo.grupo_objetos = objetos_sueltos  # Asignar grupo_objetos
    enemigo.grupo_todos = all_sprites  # Asignar grupo_todos
    all_sprites.add(enemigo)
    enemies_list.add(enemigo)
    
# 2) Ahora que enemies_list ya existe, instanciamos el sistema de niveles
from sistema_niveles import SistemaNiveles
sistema_niveles = SistemaNiveles(jugador, enemies_list)

game_over = False

mostrar_pantalla_inicio(screen)


#/// COMIENZO DE BUCLE PRINCIPAL///
running = True
while running:
    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        #evento para poder abrir el inventario con la tecla H   
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_h:
                tienda.mostrar = not tienda.mostrar 
                juego_pausado = tienda.mostrar  # Pausar si la tienda se muestra
                print("Tienda activada:", tienda.mostrar)
    
                

    if not juego_pausado:
        # Actualización del juego
        enemigos_vivos = [e for e in enemies_list if not e.is_dead]
        
        # Actualizar jugador
        jugador.update(enemigos_vivos, escenario, plataforma)
        
        # Actualizar corazones
        corazones.update()



        # Actualizar enemigos vivos y limpiar muertos
        for enemy in list(enemies_list):
            if enemy.is_dead and enemy.death_frame_index >= len(enemy.dead_frames):
                # ── Calculamos XP y subimos de nivel si toca ──
                xp_ganada = sistema_niveles.calcular_experiencia(enemy)
                if sistema_niveles.intentar_subir_nivel(xp_ganada):
                    jugador.nivel_xp.agregar_experiencia(xp_ganada)
                    print("¡Subiste de nivel!")
                # ── Aumentar puntuación ──
                jugador.puntuacion += 20
                # ── Aumentar dinero entre 2 y 8 monedas ──
                monedas = random.randint(2, 8)
                jugador.dinero += monedas
                print(f"¡Obtuviste {monedas} monedas!")
                # Una vez subimos, reajustamos atributos de los enemigos vivos
                # Posibilidad de soltar una trampa explosiva
                if random.random() < TRAP_DROP_CHANCE:
                    # Crear trampa en la posición del enemigo muerto
                    trap = TrampaExplosiva(enemy.rect.centerx, enemy.rect.centery)
                    objetos_sueltos.add(trap)
                    all_sprites.add(trap)
                    print("¡Cayó una trampa explosiva!")
                sistema_niveles.actualizar_enemigos()

                # ── Ahora sí, eliminamos al enemigo muerto ──  
                enemy.kill()
                enemies_list.remove(enemy)
            else:
                enemy.update(jugador if not jugador.is_dead else None)

                # Dibujar enemigos y sangre
        for enemigo in enemies_list:
            screen.blit(enemigo.image, enemigo.rect)

        # ——— Actualizar trampas explosivas y recolectar otros objetos ———
        current_time = pygame.time.get_ticks()
        for objeto in list(objetos_sueltos):
            if isinstance(objeto, TrampaExplosiva):
                # No eliminarla, solo actualizar su animación y daño
                objeto.update(current_time, jugador)
            else:
                # Sí es un objeto “normal”, lo recolectamos
                if jugador.rect.colliderect(objeto.rect):
                    jugador.agregar_al_inventario(objeto)
                    objeto.kill()

        # Actualizar partículas XP (mueven y suman XP al llegar)
        for particula in grupo_particulas_xp:
            particula.update(NivelXP)

        # Dibujar partículas XP
        grupo_particulas_xp.draw(screen)


        escenario.update(jugador.scroll_x)
        plataforma.update(jugador.scroll_x)

        # Dibujado
        screen.fill((0, 0, 0))
        escenario.draw(screen)
        plataforma.draw(screen)
       

        #  Dibujar todos los sprites generales
            # escribe esto:
        for sprite in all_sprites:
            if hasattr(sprite, 'pintar'):
                sprite.pintar(screen)
            else:
                screen.blit(sprite.image, sprite.rect)

        # ❤️ Dibujar sangre encima de los enemigos
        for enemigo in enemies_list:
            if enemigo.mostrar_sangre and enemigo.sangre_index > 0:
                blood_img = enemigo.sangre_frames[enemigo.sangre_index - 1]
                blood_rect = blood_img.get_rect(center=enemigo.sangre_pos)
                screen.blit(blood_img, blood_rect)
        
        
        # Interfaces
        jugador.dibujar_inventario(screen)
        jugador.nivel_xp.mostrar_barra_xp(screen, 300)
        barra_escudo.mostrar_barra_escudo(screen)
        puntuacion.dibujar(screen)
        billetera.dibujar(screen)
        
        
        # En tu bucle de dibujado, reemplaza la sección de texto así:
        fuente    = pygame.font.Font(None, 24)
        texto_atk = fuente.render(str(jugador.ataque),  True, (255, 90, 30))
        texto_def = fuente.render(str(jugador.defensa), True, (100, 200, 255))

        # Espacio entre bloques
        spacing = 80 

        # Ancho de un bloque = icono + separación interna + texto
        block_width = icon_size[0] + 5 + max(texto_atk.get_width(), texto_def.get_width())

        # Ancho total de los dos bloques + spacing
        total_width = block_width * 2 + spacing

        # Coordenada X inicial para centrar
        x_base = (WIDTH - total_width) // 2
        y_base = 50 # altura fija

        # Dibujar ataque
        screen.blit(icon_atk,  (x_base,y_base))
        screen.blit(texto_atk, (x_base + icon_size[0] + 5, y_base + (icon_size[1] - texto_atk.get_height()) // 2))

        # Dibujar defensa, desplazado a la derecha
        x_def_block = x_base + block_width + spacing
        screen.blit(icon_def,  (x_def_block,                         y_base))
        screen.blit(texto_def, (x_def_block + icon_size[0] + 5,      y_base + (icon_size[1] - texto_def.get_height()) // 2))
        
        # ——— COMPROBAR VICTORIA/DERROTA ———
        if cond_victoria.verificar_victoria(areas_exploradas):
            cond_victoria.dibujar(screen)
            pygame.display.flip()
            continue   # salto a siguiente iteración, no redibujar nada más


    tienda.dibujar_boton(screen)
    tienda.dibujar_tienda(screen)    
    

    pygame.display.flip()
    clock.tick(FPS)
        
    if cond_victoria.verificar_victoria(areas_exploradas):
        cond_victoria.dibujar(screen)

pygame.quit()
sys.exit() 