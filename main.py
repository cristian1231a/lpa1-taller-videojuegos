# programa principal
import pygame
import sys
from configuracion import WIDTH, HEIGHT, FPS
from jugador import Jugador
from enemigo import Enemigo
from escenario import Escenario
from plataforma import Plataforma
from corazones import Corazones
from nivel_xp import NivelXP
from nivel_escudo import BarraEscudo
from particula_xp import ParticulaXP

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie Vs Ninja")
clock = pygame.time.Clock()


# Configuración inicial
escenario = Escenario()
jugador = Jugador()
plataforma = Plataforma(0, 0, HEIGHT, WIDTH)  # Plataforma en la parte inferior
corazones = Corazones(jugador)  # Se pasa el jugador como referencia
barra_escudo = BarraEscudo(jugador)
grupo_particulas_xp = pygame.sprite.Group()



nivel = NivelXP()

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
        ataque=10,
        defensa=2,
        tipo="Zombie"
    )
    enemigo.grupo_objetos = objetos_sueltos  # Asignar grupo_objetos
    enemigo.grupo_todos = all_sprites  # Asignar grupo_todos
    all_sprites.add(enemigo)
    enemies_list.add(enemigo)


running = True
while running:
    # Manejo de eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Actualización del juego
    enemigos_vivos = [e for e in enemies_list if not e.is_dead]
    
    # Actualizar jugador
    jugador.update(enemigos_vivos, escenario, plataforma)
    
    # Actualizar corazones
    corazones.update()

    # Actualizar enemigos vivos y limpiar muertos
    for enemy in list(enemies_list):
        if enemy.is_dead and enemy.death_frame_index >= len(enemy.dead_frames):
            enemy.kill()
            enemies_list.remove(enemy)
        else:
            enemy.update(jugador if not jugador.is_dead else None)

            # Dibujar enemigos y sangre
    for enemigo in enemies_list:
        screen.blit(enemigo.image, enemigo.rect)

    # Recolectar objetos
    for objeto in objetos_sueltos:
        if jugador.rect.colliderect(objeto.rect):
            jugador.agregar_al_inventario(objeto)
            objeto.kill()  # Elimina el objeto de todos los grupos (incluyendo objetos_sueltos y all_sprites)
            break

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
    all_sprites.draw(screen)

    # ❤️ Dibujar sangre encima de los enemigos
    for enemigo in enemies_list:
        if enemigo.mostrar_sangre and enemigo.sangre_index > 0:
            blood_img = enemigo.sangre_frames[enemigo.sangre_index - 1]
            blood_rect = blood_img.get_rect(center=enemigo.sangre_pos)
            screen.blit(blood_img, blood_rect)
    
    
    # Interfaces
    jugador.dibujar_inventario(screen)
    nivel.mostrar_barra_xp(screen, 300)
    barra_escudo.mostrar_barra_escudo(screen)
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
