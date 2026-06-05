import pygame
from settings import *
from bullet import Bullet

class Player(pygame.sprite.Sprite):
    def __init__(self, pos):
        super().__init__()
        # Загрузка изображения игрока
        try:
            self.original_image = pygame.image.load(PLAYER_IMG).convert_alpha()
        except:
            self.original_image = pygame.Surface((40, 30), pygame.SRCALPHA)
            pygame.draw.polygon(self.original_image, GREEN, [(20, 0), (0, 30), (40, 30)])
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect(center=pos)
        self.speed = PLAYER_SPEED
        self.lives = PLAYER_LIVES
        self.invincible_until = 0
        self.last_shot_time = 0

    def update(self, keys, bullets_group):
        # Движение
        if keys[pygame.K_LEFT] and self.rect.left > 0:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT] and self.rect.right < SCREEN_WIDTH:
            self.rect.x += self.speed

        # Стрельба с кулдауном
        if keys[pygame.K_SPACE]:
            now = pygame.time.get_ticks()
            if now - self.last_shot_time > PLAYER_SHOOT_COOLDOWN:
                self.shoot(bullets_group)
                self.last_shot_time = now

        # Мерцание при неуязвимости
        if pygame.time.get_ticks() < self.invincible_until:
            if (pygame.time.get_ticks() // 100) % 2 == 0:
                self.image.set_alpha(128)
            else:
                self.image.set_alpha(255)
        else:
            self.image.set_alpha(255)

    def shoot(self, bullets_group):
        bullet = Bullet(self.rect.midtop, PLAYER_BULLET_SPEED, 'player')
        bullets_group.add(bullet)

    def hit(self):
        now = pygame.time.get_ticks()
        if now > self.invincible_until:
            self.lives -= 1
            self.invincible_until = now + INVINCIBILITY_DURATION
            return True
        return False

    def reset(self, pos):
        self.rect.center = pos
        self.lives = PLAYER_LIVES
        self.invincible_until = 0
        self.image = self.original_image.copy()