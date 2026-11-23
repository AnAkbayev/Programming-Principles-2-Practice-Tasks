"""Entry point for Mickey's Clock."""
import pygame
from clock import MickeyClock

def main():
    pygame.init()
    screen = pygame.display.set_mode((720, 720))
    pygame.display.set_caption("Mickey's Clock")
    clock = pygame.time.Clock()
    app = MickeyClock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                running = False

        app.draw(screen)
        pygame.display.flip()
        clock.tick(30)

    pygame.quit()

if __name__ == "__main__":
    main()
