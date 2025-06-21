import pygame

class BaseBuilding(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, health=100):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.image.fill((150, 150, 150))  # Default color for the building
        self.rect = self.image.get_rect(topleft=(x, y))
        self.health = health  # Add health points to the base

    def update(self):
        # Update logic for the building can be added here
        pass

    def draw(self, surface):
        surface.blit(self.image, self.rect)  # Draw the building on the given surface

    def take_damage(self, amount):
        self.health -= amount
        if self.health < 0:
            self.health = 0

    def is_destroyed(self):
        return self.health == 0