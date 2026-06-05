import pygame
from settings import *

class Bullet(pygame.sprite.Sprite):
    def __init__(self, pos, speed_y, owner_type, velocity=None):
        super().__init__()
        self.owner = owner_type
        # Цветная заливка
        color = GREEN if owner_type == 'player' else RED
        self.image = pygame.Surface((4, 12))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=pos)
        if velocity:
            self.vel_x, self.vel_y = velocity
        else:
            self.vel_x = 0
            self.vel_y = speed_y

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        # Удаление за экраном
        if (self.rect.bottom < 0 or self.rect.top > SCREEN_HEIGHT or
            self.rect.right < 0 or self.rect.left > SCREEN_WIDTH):
            self.kill()