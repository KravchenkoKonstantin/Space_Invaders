import pygame
import random
import math
from settings import *
from bullet import Bullet

class Boss(pygame.sprite.Sprite):
    def __init__(self, wave_number):
        super().__init__()
        # Загрузка графики босса
        try:
            self.image = pygame.image.load(BOSS_IMG).convert_alpha()
        except:
            self.image = pygame.Surface((100, 60), pygame.SRCALPHA)
            pygame.draw.rect(self.image, RED, (0, 0, 100, 60))
            pygame.draw.circle(self.image, WHITE, (50, 30), 20)
        self.rect = self.image.get_rect(center=(SCREEN_WIDTH//2, 100))
        self.max_health = 10 + wave_number * 2
        self.health = self.max_health
        self.shoot_timer = 0
        self.move_speed = 2
        self.direction = 1

    def update(self, bullets_group, player_pos):
        # Горизонтальное движение
        self.rect.x += self.direction * self.move_speed
        if self.rect.right >= SCREEN_WIDTH or self.rect.left <= 0:
            self.direction *= -1

        # Веерная стрельба
        now = pygame.time.get_ticks()
        if now - self.shoot_timer > 800:
            self.shoot_timer = now
            num_bullets = 5
            base_angle = math.atan2(player_pos[1] - self.rect.centery,
                                    player_pos[0] - self.rect.centerx)
            for i in range(num_bullets):
                angle = base_angle + (i - num_bullets//2) * 0.2
                vx = math.cos(angle) * ENEMY_BULLET_SPEED
                vy = math.sin(angle) * ENEMY_BULLET_SPEED
                bullet = Bullet(self.rect.midbottom, 0, 'enemy', velocity=(vx, vy))
                bullets_group.add(bullet)

    def hit(self):
        self.health -= 1
        if self.health <= 0:
            self.kill()
            return True
        return False 
