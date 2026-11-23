"""Red ball movement with fixed 20-pixel steps and boundary checks."""
import pygame

class Ball:
    RADIUS = 25
    STEP = 20
    COLOR = (220, 35, 45)

    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.x = screen_width // 2
        self.y = screen_height // 2

    def handle_key(self, key):
        dx, dy = 0, 0
        if key == pygame.K_LEFT:
            dx = -self.STEP
        elif key == pygame.K_RIGHT:
            dx = self.STEP
        elif key == pygame.K_UP:
            dy = -self.STEP
        elif key == pygame.K_DOWN:
            dy = self.STEP
        else:
            return

        new_x = self.x + dx
        new_y = self.y + dy

        # Ignore the move if any part of the ball would leave the window.
        if (self.RADIUS <= new_x <= self.screen_width - self.RADIUS and
                self.RADIUS <= new_y <= self.screen_height - self.RADIUS):
            self.x, self.y = new_x, new_y

    def draw(self, screen):
        pygame.draw.circle(screen, self.COLOR, (self.x, self.y), self.RADIUS)
