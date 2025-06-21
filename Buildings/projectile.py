import pygame
import math

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, speed=7, damage=5, target_pos=None):
        super().__init__()
        self.image = pygame.Surface((12, 6))
        self.image.fill((255, 200, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.damage = damage
        if target_pos is not None:
            dx = target_pos[0] - x
            dy = target_pos[1] - y
            dist = math.hypot(dx, dy)
            if dist == 0:
                dist = 1
            self.vel_x = self.speed * dx / dist
            self.vel_y = self.speed * dy / dist
        else:
            self.vel_x = self.speed * direction
            self.vel_y = 0

    def update(self):
        self.rect.x += self.vel_x
        self.rect.y += self.vel_y
        # Remove projectile if it goes off screen
        if self.rect.right < 0 or self.rect.left > 800 or self.rect.bottom < 0 or self.rect.top > 600:
            self.kill()
