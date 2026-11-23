"""Moving red ball game."""
import pygame
from ball import Ball

WIDTH, HEIGHT = 640, 480

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Practice 09 - Moving Ball")
    clock = pygame.time.Clock()
    ball = Ball(WIDTH, HEIGHT)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                else:
                    ball.handle_key(event.key)

        screen.fill((255, 255, 255))
        ball.draw(screen)
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
