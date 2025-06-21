import pygame

class Projectile(pygame.sprite.Sprite):
    def __init__(self, x, y, direction, speed=7, damage=5):
        super().__init__()
        self.image = pygame.Surface((12, 6))
        self.image.fill((255, 200, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.direction = direction  # 1 for right, -1 for left
        self.speed = speed
        self.damage = damage

    def update(self):
        self.rect.x += self.speed * self.direction
        # Remove projectile if it goes off screen
        if self.rect.right < 0 or self.rect.left > 800:
            self.kill()
