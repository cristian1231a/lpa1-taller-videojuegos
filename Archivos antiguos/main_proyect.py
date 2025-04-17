# programa principal
import pygame
from player import Player
from enemies import Enemies
from background import Background
from plat import Platform
from lives import Lives
from settings import WIDTH , HEIGHT, FPS



pygame.init()


pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Zombie Vs Ninja")
clock = pygame.time.Clock()

background = Background()
player = Player()
platform = Platform(0, 0, WIDTH, HEIGHT)  # (x, y, ancho, alto) / PARA CREAR LA PLATAFORMA EN LA POSICION ESPECIFICA
lives = Lives()



all_sprites = pygame.sprite.Group()
enemies_list = pygame.sprite.Group()

all_sprites.add(player)

for i in range(2):
    enemies = Enemies()
    all_sprites.add(enemies)
    enemies_list.add(enemies)





running = True
while running:
    # --- 1. Manejo de eventos ---
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # --- 2. Actualizaciones de lógica del juego ---

    # Actualizar jugador
    player.update(enemies_list)

    # Actualizar enemigos (y verificar colisión individual)
    for enemy in enemies_list:
        enemy.attacking = pygame.sprite.collide_rect(player, enemy)
        enemy.update(player)

    # Otras colisiones globales (si necesitás acciones adicionales)
    hits = pygame.sprite.spritecollide(player, enemies_list, False)
    if hits:
        print("¡Colisión detectada!")

    # Actualizar otras entidades si tenés más (proyectiles, power-ups, etc.)

    # --- 3. Dibujar todo en pantalla ---
    screen.fill((0, 0, 0))  # Limpia la pantalla (negro de fondo)
    background.draw(screen)  # Dibuja el fondo
    screen.blit(platform.image, platform.rect)  # Dibuja la plataforma/base
    lives.draw(screen)  # Dibuja vidas
    all_sprites.draw(screen)  # Dibuja todos los sprites (jugador + enemigos)

    # --- 4. Actualizar pantalla ---
    pygame.display.flip()

    # --- 5. Controlar la velocidad del juego (FPS) ---
    clock.tick(FPS)  # Limita a 60 FPS

pygame.quit()