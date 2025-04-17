import pygame

BLACK = (0, 0, 0)

class Lives:
    def __init__(self):
        # Cargar imágenes desde lives1.png (0 vidas) hasta lives4.png (3 vidas)
        self.live_frames = [
            pygame.image.load(f"assets/img/lives/lives{i}.png").convert()
            for i in range(1, 5)  # Del 1 al 4
        ]

        for frame in self.live_frames:
            frame.set_colorkey(BLACK)

        self.lives = 3  # Comienza con 3 vidas (index 3 → lives4.png)
        self.x = 20
        self.y = 10

    def draw(self, screen):
        # El índice se alinea con el número de vidas: 3 → index 3 (lives4.png)
        screen.blit(self.live_frames[self.lives], (self.x, self.y))

    def lose_life(self):
        if self.lives > 0:
            self.lives -= 1

    def gain_life(self):
        if self.lives < 3:
            self.lives += 1