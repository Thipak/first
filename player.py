import pygame
import os

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)
        # Load the sprite sheet
        sprite_path = os.path.join('assets', 'player_sprite.png')
        self.sprite_sheet = pygame.image.load(sprite_path).convert_alpha()
        sheet_width, sheet_height = self.sprite_sheet.get_size()
        self.rows = 4
        self.cols = 8
        self.frame_width = sheet_width // self.cols
        self.frame_height = sheet_height // self.rows
        # Extract frames: frames[row][col]
        self.frames = [
            [self.sprite_sheet.subsurface(pygame.Rect(col * self.frame_width, row * self.frame_height, self.frame_width, self.frame_height))
             for col in range(self.cols)]
            for row in range(self.rows)
        ]
        self.direction = 3  # 2: left, 3: right
        self.frame_index = 0
        self.animation_timer = 0
        self.animation_speed = 0.2
        self.image = self.frames[self.direction][0]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 3
        self.run_speed = 9
        self.vel_y = 0
        self.gravity = 0.6
        self.on_ground = False
        self.moving = False
        self.jump_pressed = False  # Track jump key state

    @property
    def x(self):
        return self.rect.x

    @x.setter
    def x(self, value):
        self.rect.x = value

    @property
    def y(self):
        return self.rect.y

    @y.setter
    def y(self, value):
        self.rect.y = value

    def update(self, platforms=None, base_blocks=None):
        keys = pygame.key.get_pressed()
        dx = 0
        # Run if shift is held
        speed = self.run_speed if keys[pygame.K_LSHIFT] or keys[pygame.K_RSHIFT] else self.speed
        if keys[pygame.K_a]:
            dx = -speed
            self.direction = 2
            self.moving = True
        elif keys[pygame.K_d]:
            dx = speed
            self.direction = 3
            self.moving = True
        else:
            self.moving = False
        # Jump (prevent holding for double jump)
        if keys[pygame.K_w]:
            if self.on_ground and not self.jump_pressed:
                self.vel_y = -12
                self.on_ground = False
                self.jump_pressed = True
        else:
            self.jump_pressed = False
        # Apply gravity
        self.vel_y += self.gravity
        if self.vel_y > 12:
            self.vel_y = 12
        dy = self.vel_y
        # Move and check collisions
        self.rect.x += dx
        if platforms:
            self.check_collision(dx, 0, platforms)
        if base_blocks:
            self.check_collision(dx, 0, base_blocks)
        self.rect.y += dy
        if platforms:
            self.check_collision(0, dy, platforms)
        if base_blocks:
            self.check_collision(0, dy, base_blocks)
        # Animation
        if self.moving and self.on_ground:
            self.animation_timer += self.animation_speed
            if self.animation_timer >= 1:
                self.animation_timer = 0
                self.frame_index = (self.frame_index + 1) % (self.cols - 1)
            self.image = self.frames[self.direction][self.frame_index + 1]
        else:
            self.frame_index = 0
            self.image = self.frames[self.direction][0]
        # Prevent going out of screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > 800:
            self.rect.right = 800
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > 600:
            self.rect.bottom = 600

    def check_collision(self, dx, dy, platforms):
        for platform in platforms:
            if self.rect.colliderect(platform):
                if dy > 0:  # Falling
                    self.rect.bottom = platform.top
                    self.vel_y = 0
                    self.on_ground = True
                elif dy < 0:  # Jumping
                    self.rect.top = platform.bottom
                    self.vel_y = 0
                if dx > 0:  # Moving right
                    self.rect.right = platform.left
                elif dx < 0:  # Moving left
                    self.rect.left = platform.right

    def draw(self, surface):
        surface.blit(self.image, self.rect)


