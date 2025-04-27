# condicion_victoria.py

import pygame
import sys

class CondicionVictoria:
    def __init__(self, jugador, exploracion_requerida=5, puntaje_requerido=400):
        """
        jugador: instancia de tu clase Jugador
        exploracion_requerida: número de áreas exploradas para victoria por exploración
        puntaje_requerido: puntuación necesaria para victoria por puntaje
        """
        self.jugador = jugador
        self.exploracion_requerida = exploracion_requerida
        self.puntaje_requerido = puntaje_requerido

        # Flags internos  
        self.victoria_exploracion = False
        self.victoria_puntaje    = False
        self.derrota             = False

        # Fade-in
        self.alpha = 0  
        self.fade_speed = 3  

        # Carga de imágenes (coloca estos PNG en assets/img/scene/)
        self.img_victoria = pygame.image.load("assets/img/scene/victory_condition/victory_ninja.png").convert_alpha()
        self.img_derrota  = pygame.image.load("assets/img/scene/victory_condition/defeat_ninja.png").convert_alpha()

        # Ajusta tamaño
        screen_w, screen_h = pygame.display.get_surface().get_size()
        target_w = screen_w // 2
        self.img_victoria = pygame.transform.scale(self.img_victoria, (target_w, int(target_w * self.img_victoria.get_height()/self.img_victoria.get_width())))
        self.img_derrota  = pygame.transform.scale(self.img_derrota,  (target_w, int(target_w * self.img_derrota.get_height() /self.img_derrota.get_width())))

        # Prepara superficie con canal alpha
        self.surf_victoria = self.img_victoria.copy()
        self.surf_derrota  = self.img_derrota.copy()
        self.surf_victoria.set_alpha(self.alpha)
        self.surf_derrota.set_alpha(self.alpha)

    def verificar_victoria(self, exploracion_actual):
        """Llamar cada frame antes de dibujar; retorna True si el juego ha terminado."""
        # Victoria por exploración
        if exploracion_actual >= self.exploracion_requerida:
            self.victoria_exploracion = True
        # Victoria por puntaje
        if self.jugador.puntuacion >= self.puntaje_requerido:
            self.victoria_puntaje = True
        # Derrota
        if self.jugador.puntos_vida <= 0:
            self.derrota = True

        return self.victoria_exploracion or self.victoria_puntaje or self.derrota

    def dibujar(self, screen):
        """Dibuja la pantalla de victoria/derrota con fade-in."""
        if not (self.victoria_exploracion or self.victoria_puntaje or self.derrota):
            return

        # Incrementa alpha (máximo 255 para el fade)
        self.alpha = min(255, self.alpha + self.fade_speed)

        # Elige la superficie correspondiente
        if self.derrota:
            img_surf = self.surf_derrota
        else:
            img_surf = self.surf_victoria

        img_surf.set_alpha(self.alpha)

        # Centra en pantalla
        sw, sh = screen.get_size()
        iw, ih = img_surf.get_size()
        x = (sw - iw) // 2
        y = (sh - ih) // 2

        screen.blit(img_surf, (x, y))
