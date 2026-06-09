import pygame
import random
import math
from settings import *
from bullet import Bullet

class Enemy(pygame.sprite.Sprite):
    def __init__(self, pos, enemy_type='basic'):
        super().__init__()
        self.enemy_type = enemy_type
        try:
            img_path = ENEMY_IMGS.get(enemy_type, ENEMY_IMGS['basic'])
            self.image = pygame.image.load(img_path).convert_alpha()
        except:
            self.image = pygame.Surface((40, 30), pygame.SRCALPHA)
            if enemy_type == 'basic':
                pygame.draw.rect(self.image, RED, (0, 0, 40, 30))
                pygame.draw.rect(self.image, WHITE, (5, 5, 30, 20))
            elif enemy_type == 'armored':
                pygame.draw.rect(self.image, ORANGE, (0, 0, 40, 30))
                pygame.draw.rect(self.image, WHITE, (5, 5, 30, 20), 2)
            elif enemy_type == 'fast':
                pygame.draw.rect(self.image, CYAN, (0, 0, 40, 30))
                pygame.draw.polygon(self.image, WHITE, [(20, 5), (5, 25), (35, 25)])
        self.rect = self.image.get_rect(topleft=pos)
        self.health = 2 if enemy_type == 'armored' else 1
        self.can_shoot = True
        self.shoot_prob = ENEMY_SHOOT_PROB
        if enemy_type == 'fast':
            self.shoot_prob *= 2

    def update(self, bullets_group, player_pos=None):
        if self.can_shoot and random.random() < self.shoot_prob:
            self.shoot(bullets_group, player_pos)

    def shoot(self, bullets_group, player_pos):
        if player_pos:
            dx = player_pos[0] - self.rect.centerx
            dy = player_pos[1] - self.rect.centery
            dist = math.hypot(dx, dy)
            if dist != 0:
                vx = dx / dist * ENEMY_BULLET_SPEED
                vy = dy / dist * ENEMY_BULLET_SPEED
            else:
                vx, vy = 0, ENEMY_BULLET_SPEED
        else:
            vx, vy = 0, ENEMY_BULLET_SPEED
        bullet = Bullet(self.rect.midbottom, 0, 'enemy', velocity=(vx, vy))
        bullets_group.add(bullet)


class ArmoredEnemy(Enemy):
    def __init__(self, pos):
        super().__init__(pos, 'armored')

class FastEnemy(Enemy):
    def __init__(self, pos):
        super().__init__(pos, 'fast')