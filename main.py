# programa principal
import pygame
import sys
from configuracion import WIDTH, HEIGHT, FPS
from jugador import Jugador
from enemigo import Enemigo
from fondo import Fondo
from plataforma import Plataforma
from corazones import Corazones
from nivel_xp import NivelXP
from nivel_escudo import BarraEscudo

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Zombie Vs Ninja")
clock = pygame.time.Clock()

# Configuración inicial
fondo = Fondo()
jugador = Jugador()
plataforma = Plataforma(0, 0, HEIGHT, WIDTH)  # Plataforma en la parte inferior
corazones = Corazones(jugador)  # Se pasa el jugador como referencia
barra_escudo = BarraEscudo(jugador)



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
    jugador.update(enemigos_vivos)
    
    # Actualizar corazones
    corazones.update()

    # Actualizar enemigos vivos y limpiar muertos
    for enemy in list(enemies_list):
        if enemy.is_dead and enemy.death_frame_index >= len(enemy.dead_frames):
            enemy.kill()
            enemies_list.remove(enemy)
        else:
            enemy.update(jugador if not jugador.is_dead else None)

    # Recolectar objetos
    for objeto in objetos_sueltos:
        if jugador.rect.colliderect(objeto.rect):
            jugador.agregar_al_inventario(objeto)
            objeto.kill()  # Elimina el objeto de todos los grupos (incluyendo objetos_sueltos y all_sprites)
            break

    # Dibujado
    screen.fill((0, 0, 0))
    fondo.draw(screen)
    screen.blit(plataforma.image, plataforma.rect)
    nivel.mostrar_barra_xp(screen, 300)
    barra_escudo.mostrar_barra_escudo(screen)
    all_sprites.draw(screen)
    jugador.dibujar_inventario(screen)
    
    pygame.display.flip()
    clock.tick(FPS)

pygame.quit()
sys.exit()
