# programa principal
import pygame
from player import Player
from enemies import Enemies
from background import Background
from plat import Platform

pygame.init()


WIDTH = 800
HEIGHT = 600
BLACK = (0,0,0)
WHITE = (255,255,255)


pygame.mixer.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

pygame.display.set_caption("Zombie Vs Ninja")
clock = pygame.time.Clock()

background = Background()
player = Player()
platform = Platform(0, 0, WIDTH, HEIGHT)  # (x, y, ancho, alto) / PARA CREAR LA PLATAFORMA EN LA POSICION ESPECIFICA



all_sprites = pygame.sprite.Group()
enemies_list = pygame.sprite.Group()

all_sprites.add(player)

for i in range(2):
    enemies = Enemies()
    all_sprites.add(enemies)
    enemies_list.add(enemies)





running = True
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    all_sprites.update()

    # fill the screen with a color to wipe away anything from last frame
    screen.fill((0, 0, 0))  # Opcional, limpia la pantalla antes de dibujar
    background.draw(screen)  # Llamamos al método draw() en vez de usar screen.blit directamente
    screen.blit(platform.image, platform.rect) #dibujar la base o la plataforma

    # RENDER YOUR GAME HERE
    all_sprites.draw(screen)

    # flip() the display to put your work on screen
    pygame.display.flip()


    clock.tick(60)  # limits FPS to 60

pygame.quit()