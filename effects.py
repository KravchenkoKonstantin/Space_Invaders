import pygame
import random

class Particle(pygame.sprite.Sprite):
    def __init__(self, pos, color, velocity, lifetime):
        super().__init__()
        self.image = pygame.Surface((4, 4))
        self.image.fill(color)
        self.rect = self.image.get_rect(center=pos)
        self.vel = velocity
        self.lifetime = lifetime
        self.start_time = pygame.time.get_ticks()

    def update(self):
        self.rect.x += self.vel[0]
        self.rect.y += self.vel[1]
        if pygame.time.get_ticks() - self.start_time > self.lifetime:
            self.kill()

def spawn_particles(group, pos, color, count=10, max_speed=3, lifetime=300):
    for _ in range(count):
        vx = random.uniform(-max_speed, max_speed)
        vy = random.uniform(-max_speed, max_speed)
        p = Particle(pos, color, (vx, vy), lifetime)
        group.add(p)