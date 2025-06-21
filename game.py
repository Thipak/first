import pygame

from player import Player  # Assuming player.py is in the same directory

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

    def run(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            
            self.screen.fill((0, 0, 0))  # Clear the screen with black
            # Draw platforms
            for plat in self.platforms:
                pygame.draw.rect(self.screen, (100, 100, 100), plat)
            self.player.update(self.platforms)  # Update the player with platforms
            self.player.draw(self.screen)  # Draw the player
            pygame.display.flip()  # Update the display
            self.clock.tick(60)  # Limit to 60 FPS

        pygame.quit()

if __name__ == "__main__":
    game = Game(800, 600)
    game.run()