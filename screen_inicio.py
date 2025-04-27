import pygame
from configuracion import WIDTH, HEIGHT


#Antes de iniciar el juego se mostrara una pantalla de inicio
def mostrar_pantalla_inicio(screen):
        # Cargar imagen de fondo
        fondo = pygame.image.load("assets/img/scene/screen_inicio/screen_inicio.png").convert()
        fondo = pygame.transform.scale(fondo, (WIDTH, HEIGHT))  # Asegúrate que se escale a la pantalla si es necesario

        fuente = pygame.font.SysFont("arial", 32)
        texto = fuente.render("Presiona ESPACIO para comenzar", True, (255, 255, 255))
        texto_rect = texto.get_rect(center=(WIDTH // 2, HEIGHT - 60))

        reloj = pygame.time.Clock()
        esperando = True
        mostrar_texto = True
        parpadeo_timer = 0

        while esperando:
            screen.blit(fondo, (0, 0))

            # Lógica de parpadeo
            parpadeo_timer += reloj.get_time()
            if parpadeo_timer >= 500:  # Cambia cada 500 ms (0.5 segundos)
                mostrar_texto = not mostrar_texto
                parpadeo_timer = 0

            if mostrar_texto:
                screen.blit(texto, texto_rect)

            pygame.display.flip()
            reloj.tick(60)

            # Manejo de eventos: no cerramos pygame aquí
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    # Reenviamos QUIT al bucle principal y salimos
                    pygame.event.post(event)
                    esperando = False
                elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                    esperando = False
    
        # Al salir, volvemos al bucle principal sin cerrar display
        return