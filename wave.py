import pygame
import random
from settings import *
from enemy import Enemy, ArmoredEnemy, FastEnemy
from boss import Boss

class WaveManager:
    def __init__(self):
        self.enemies = pygame.sprite.Group()
        self.boss = None
        self.wave_number = 0
        self.move_direction = 1
        self.move_speed = ENEMY_BASE_SPEED

    def start_new_wave(self):
        self.wave_number += 1
        self.enemies.empty()
        self.boss = None
        self.move_direction = 1
        self.move_speed = ENEMY_BASE_SPEED + (self.wave_number - 1) * WAVE_SPEED_MULTIPLIER

        rows = ENEMY_ROWS + self.wave_number // 3
        cols = ENEMY_COLS + (self.wave_number - 1) // 2
        max_cols = (SCREEN_WIDTH - 100) // 50
        cols = min(cols, max_cols)
        rows = min(rows, 8) 

        for row in range(rows):
            for col in range(cols):
                x = 80 + col * 50
                y = 50 + row * 50
                # Распределение типов врагов
                if self.wave_number <= 2:
                    enemy = Enemy((x, y), 'basic')
                elif row == 0 and self.wave_number % 2 == 0:
                    enemy = ArmoredEnemy((x, y))
                elif row == rows - 1 and self.wave_number > 3:
                    enemy = FastEnemy((x, y))
                else:
                    if random.random() < 0.2 * self.wave_number / 10:
                        enemy = ArmoredEnemy((x, y))
                    elif random.random() < 0.1 * self.wave_number / 10:
                        enemy = FastEnemy((x, y))
                    else:
                        enemy = Enemy((x, y), 'basic')
                self.enemies.add(enemy)

        if self.wave_number % BOSS_EVERY_WAVE == 0:
            self.boss = Boss(self.wave_number)

    def update(self, bullets_group, player_pos):
        move_down = False
        for enemy in self.enemies:
            enemy.rect.x += self.move_direction * self.move_speed
            if enemy.rect.right >= SCREEN_WIDTH or enemy.rect.left <= 0:
                move_down = True

        if move_down:
            self.move_direction *= -1
            for enemy in self.enemies:
                enemy.rect.y += ENEMY_DROP_DISTANCE
                if enemy.rect.bottom >= SCREEN_HEIGHT - 80:
                    return 'game_over'


        for enemy in self.enemies:
            enemy.update(bullets_group, player_pos)

        if self.boss:
            self.boss.update(bullets_group, player_pos)

        return 'ok'