import pygame

from player import Player  # Assuming player.py is in the same directory
from Buildings.base import BaseBuilding  # Import BaseBuilding

class Game:
    def __init__(self, width, height):
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.player = Player(100, 100)  # Create a player instance
        # Create a simple ground platform
        self.platforms = [pygame.Rect(0, 550, self.width, 50)]
        pygame.display.set_caption("First 2025")
        self.clock = pygame.time.Clock()
        self.running = True

        # Add base buildings for both teams
        self.user_base = BaseBuilding(20, 350, 60, 200, health=100)  # Taller building
        self.enemy_base = BaseBuilding(self.width - 80, 350, 60, 200, health=100)  # Taller building
        self.attack_cooldown = 0  # Cooldown for attack animation
        self.attack_animation_time = 15  # Frames for attack animation
        self.attacking = False
        self.has_collided = False  # Track if collision is ongoing
        self.font = pygame.font.SysFont(None, 32)  # Font for hitpoints

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            self.screen.fill((0, 0, 0))  # Clear the screen with black
            # Draw platforms
            for plat in self.platforms:
                pygame.draw.rect(self.screen, (100, 100, 100), plat)
            # Draw bases
            self.user_base.draw(self.screen)
            self.enemy_base.draw(self.screen)
            # Draw hitpoints above each base
            user_hp_text = self.font.render(f"HP: {self.user_base.health}", True, (255, 255, 255))
            enemy_hp_text = self.font.render(f"HP: {self.enemy_base.health}", True, (255, 255, 255))
            self.screen.blit(user_hp_text, (self.user_base.rect.centerx - user_hp_text.get_width() // 2, self.user_base.rect.top - 30))
            self.screen.blit(enemy_hp_text, (self.enemy_base.rect.centerx - enemy_hp_text.get_width() // 2, self.enemy_base.rect.top - 30))
            # Update and draw player
            base_blocks = [self.enemy_base.rect]  # Only enemy base blocks the player
            self.player.update(self.platforms, base_blocks)
            self.player.draw(self.screen)

            # Player can go past own base, but not enemy base
            player_rect = self.player.rect
            # Check collision with enemy base
            if player_rect.colliderect(self.enemy_base.rect):
                # Prevent player from moving past enemy base
                if self.player.x < self.enemy_base.rect.left:
                    self.player.x = self.enemy_base.rect.left - self.player.rect.width
                # Attack logic: only one damage per collision
                if not self.has_collided:
                    self.attacking = True
                    self.attack_cooldown = self.attack_animation_time
                    self.enemy_base.take_damage(1)  # Inflict 1 damage per collision
                    self.has_collided = True
            else:
                self.attacking = False
                self.has_collided = False

            # Attack animation (simple flash effect)
            if self.attacking:
                pygame.draw.rect(self.screen, (255, 0, 0), self.enemy_base.rect, 5)
            if self.attack_cooldown > 0:
                self.attack_cooldown -= 1
                if self.attack_cooldown == 0:
                    self.attacking = False

            # Game over check
            if self.user_base.is_destroyed() or self.enemy_base.is_destroyed():
                font = pygame.font.SysFont(None, 72)
                if self.user_base.is_destroyed():
                    text = font.render("Game Over! You Lose!", True, (255, 0, 0))
                else:
                    text = font.render("Victory!", True, (0, 255, 0))
                self.screen.blit(text, (self.width // 2 - text.get_width() // 2, self.height // 2 - text.get_height() // 2))
                pygame.display.flip()
                pygame.time.wait(2000)
                self.running = False
                continue

            pygame.display.flip()  # Update the display
            self.clock.tick(60)  # Limit to 60 FPS

        pygame.quit()

if __name__ == "__main__":
    game = Game(800, 600)
    game.run()