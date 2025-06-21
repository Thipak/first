import pygame

class Trooper(pygame.sprite.Sprite):
    def __init__(self, x, y, speed=2, damage=5, direction=1, health=10):
        super().__init__()
        self.image = pygame.Surface((30, 30))  # Smaller than player
        self.image.fill((255, 0, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed
        self.damage = damage
        self.direction = direction  # 1 for right, -1 for left
        self.max_health = health
        self.health = health
        self.alive = True

    def update(self, obstacles, enemy_sprites, ignore_player=False):
        if not self.alive:
            return
        # Move towards the enemy building
        self.rect.x += self.speed * self.direction
        # Check collision with enemy troops, player, or obstacles
        for sprite in enemy_sprites:
            if ignore_player and hasattr(sprite, 'is_player') and sprite.is_player:
                continue
            if self.rect.colliderect(sprite.rect):
                # Both parties take damage immediately
                if hasattr(sprite, 'take_damage'):
                    sprite.take_damage(self.damage)
                self.take_damage(getattr(sprite, 'damage', self.health))  # Use sprite.damage if available, else die
                return
        for obs in obstacles:
            if self.rect.colliderect(obs):
                self.take_damage(self.health)
                return

    def take_damage(self, amount):
        self.health -= amount
        if self.health <= 0:
            self.alive = False
            self.kill()

    def draw(self, surface, font=None):
        surface.blit(self.image, self.rect)
        # Draw HP bar
        bar_width = self.rect.width
        bar_height = 5
        hp_ratio = max(self.health / self.max_health, 0)
        hp_bar_rect = pygame.Rect(self.rect.left, self.rect.top - 10, int(bar_width * hp_ratio), bar_height)
        bg_bar_rect = pygame.Rect(self.rect.left, self.rect.top - 10, bar_width, bar_height)
        pygame.draw.rect(surface, (60, 60, 60), bg_bar_rect)
        pygame.draw.rect(surface, (0, 255, 0), hp_bar_rect)