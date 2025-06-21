import pygame
from player import Player  # Assuming player.py is in the same directory
from Buildings.base import BaseBuilding  # Import BaseBuilding
from Troops.trooper import Trooper  # Import Trooper

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
        self.respawn_timer = 0  # Timer for respawn
        self.spawn_point = (self.user_base.rect.right + 10, self.user_base.rect.bottom - self.player.rect.height)  # Right side of user base

        # Trooper group and spawn timer
        self.trooper_group = pygame.sprite.Group()
        self.enemy_trooper_group = pygame.sprite.Group()
        self.trooper_spawn_timer = pygame.time.get_ticks()
        self.trooper_spawn_interval = 5000  # 5 seconds
        self.enemy_trooper_spawn_timer = pygame.time.get_ticks()
        self.enemy_trooper_spawn_interval = 5000

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
            self.player.draw(self.screen, font=self.font)

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

            # Enemy base fires at player if in range
            fire_range = 350
            player_center = self.player.rect.centerx
            enemy_center = self.enemy_base.rect.centerx
            if abs(player_center - enemy_center) < fire_range:
                player_pos = self.player.rect.center
                self.enemy_base.shoot(direction=-1, target_pos=player_pos)

            # Update base projectiles
            self.user_base.update()
            self.enemy_base.update()

            # Check collision between enemy projectiles and player
            for proj in self.enemy_base.projectiles:
                if self.player.rect.colliderect(proj.rect):
                    self.player.take_damage(proj.damage)
                    proj.kill()

            # Handle player death and respawn
            if self.player.is_dead():
                if not self.player.is_hidden():
                    self.player.hide()
                if self.respawn_timer == 0:
                    self.respawn_timer = pygame.time.get_ticks()
                # Draw 'You Died' message
                font = pygame.font.SysFont(None, 64)
                text = font.render("You Died!", True, (255, 0, 0))
                self.screen.blit(text, (self.width // 2 - text.get_width() // 2, self.height // 2 - text.get_height() // 2))
                pygame.display.flip()
                # Wait for 2 seconds before respawn
                if pygame.time.get_ticks() - self.respawn_timer > 2000:
                    self.player.respawn(*self.spawn_point)
                    self.respawn_timer = 0
                self.clock.tick(60)
                continue

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

            # Spawn troopers every 5 seconds if building exists
            if not self.user_base.is_destroyed():
                now = pygame.time.get_ticks()
                if now - self.trooper_spawn_timer > self.trooper_spawn_interval:
                    trooper = Trooper(self.user_base.rect.right + 10, self.user_base.rect.bottom - 20, direction=1)
                    self.trooper_group.add(trooper)
                    self.trooper_spawn_timer = now
            # Spawn enemy troopers every 5 seconds if building exists
            if not self.enemy_base.is_destroyed():
                now = pygame.time.get_ticks()
                if now - self.enemy_trooper_spawn_timer > self.enemy_trooper_spawn_interval:
                    enemy_trooper = Trooper(self.enemy_base.rect.left - 10, self.enemy_base.rect.bottom - 20, direction=-1)
                    self.enemy_trooper_group.add(enemy_trooper)
                    self.enemy_trooper_spawn_timer = now
            # Update and draw troopers
            for trooper in self.trooper_group:
                trooper.update([], list(self.enemy_trooper_group) + [self.enemy_base, self.player], ignore_player=True)
                trooper.draw(self.screen)
            for trooper in self.enemy_trooper_group:
                trooper.update([], list(self.trooper_group) + [self.user_base, self.player], ignore_player=False)
                trooper.draw(self.screen)

            # Player damages only enemy troopers on collision
            for trooper in self.enemy_trooper_group:
                if self.player.rect.colliderect(trooper.rect):
                    trooper.take_damage(10)  # Player inflicts 10 damage per collision

            pygame.display.flip()  # Update the display
            self.clock.tick(60)  # Limit to 60 FPS

        pygame.quit()

if __name__ == "__main__":
    game = Game(800, 600)
    game.run()