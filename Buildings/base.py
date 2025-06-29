import pygame
from Buildings.projectile import Projectile

class BaseBuilding(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, health=100):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((150, 150, 150))  # Default color for the building
        self.rect = self.image.get_rect(topleft=(x, y))
        self.health = health  # Add health points to the base
        self.projectiles = pygame.sprite.Group()  # Group to hold projectiles
        self.shoot_cooldown = 0  # Cooldown for shooting
        self.shoot_interval = 60  # Frames between shots

    def update(self):
        # Update logic for the building can be added here
        self.projectiles.update()
        if self.shoot_cooldown > 0:
            self.shoot_cooldown -= 1

    def draw(self, surface):
        surface.blit(self.image, self.rect)  # Draw the building on the given surface
        self.projectiles.draw(surface)

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def is_destroyed(self):
        return self.health == 0

    def shoot(self, direction, target_pos=None):
        if self.shoot_cooldown == 0:
            # Fire from the edge of the building, not the center
            if direction == 1:
                x = self.rect.right + 6  # 6 is half projectile width
            else:
                x = self.rect.left - 6
            y = self.rect.centery
            proj = Projectile(x, y, direction, target_pos=target_pos)
            self.projectiles.add(proj)
            self.shoot_cooldown = self.shoot_interval