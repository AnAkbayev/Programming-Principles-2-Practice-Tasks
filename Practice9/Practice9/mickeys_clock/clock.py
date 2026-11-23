"""Clock face and animated Mickey-style glove hands.

The right glove indicates minutes; the left glove indicates seconds.
The clock reads the computer's local system time.
"""
from datetime import datetime
import math
from pathlib import Path
import pygame

SIZE = 720
CENTER = (SIZE // 2, SIZE // 2)
FACE_RADIUS = 275
BG = (250, 248, 240)
DARK = (35, 35, 42)
GOLD = (242, 207, 115)
RED = (210, 45, 55)

class MickeyClock:
    def __init__(self):
        self.font_big = pygame.font.SysFont("arial", 54, bold=True)
        self.font_num = pygame.font.SysFont("arial", 30, bold=True)
        self.font_small = pygame.font.SysFont("arial", 18)
        image_path = Path(__file__).parent / "images" / "mickey_hand.png"
        self.hand_image = pygame.image.load(str(image_path)).convert_alpha()
        self.hand_image = pygame.transform.smoothscale(self.hand_image, (170, 100))

    def _draw_face(self, screen):
        screen.fill(BG)
        pygame.draw.circle(screen, (185, 185, 190), CENTER, FACE_RADIUS + 18)
        pygame.draw.circle(screen, DARK, CENTER, FACE_RADIUS + 7)
        pygame.draw.circle(screen, (255, 248, 218), CENTER, FACE_RADIUS)
        pygame.draw.circle(screen, GOLD, CENTER, FACE_RADIUS, 5)

        # Mickey-inspired silhouette at the top of the clock.
        pygame.draw.circle(screen, DARK, (CENTER[0] - 67, CENTER[1] - 175), 43)
        pygame.draw.circle(screen, DARK, (CENTER[0] + 67, CENTER[1] - 175), 43)
        pygame.draw.circle(screen, (255, 255, 255), (CENTER[0], CENTER[1] - 125), 67)
        pygame.draw.ellipse(screen, DARK, (CENTER[0] - 12, CENTER[1] - 140, 24, 34))
        pygame.draw.ellipse(screen, DARK, (CENTER[0] - 10, CENTER[1] - 92, 20, 12))

        for i in range(60):
            angle = math.radians(i * 6 - 90)
            outer = FACE_RADIUS - 15
            inner = FACE_RADIUS - (37 if i % 5 == 0 else 24)
            p1 = (CENTER[0] + math.cos(angle) * inner, CENTER[1] + math.sin(angle) * inner)
            p2 = (CENTER[0] + math.cos(angle) * outer, CENTER[1] + math.sin(angle) * outer)
            color = RED if i % 5 == 0 else (85, 85, 90)
            pygame.draw.line(screen, color, p1, p2, 5 if i % 5 == 0 else 3)

        for number in range(1, 13):
            angle = math.radians(number * 30 - 90)
            radius = FACE_RADIUS - 75
            pos = (CENTER[0] + math.cos(angle) * radius,
                   CENTER[1] + math.sin(angle) * radius)
            label = self.font_num.render(str(number), True, DARK)
            screen.blit(label, label.get_rect(center=pos))

    def _draw_glove_hand(self, screen, angle_degrees, length=170):
        # Sprite points upward at zero degrees. Rotate clockwise by the time angle.
        rotated = pygame.transform.rotate(self.hand_image, -angle_degrees)
        rect = rotated.get_rect()
        rect.center = CENTER
        screen.blit(rotated, rect)

    def draw(self, screen):
        now = datetime.now()
        self._draw_face(screen)

        # Minute hand advances smoothly with seconds; second hand follows seconds.
        minute_angle = (now.minute + now.second / 60.0) * 6
        second_angle = now.second * 6

        self._draw_glove_hand(screen, minute_angle)
        self._draw_glove_hand(screen, second_angle)

        pygame.draw.circle(screen, DARK, CENTER, 15)
        pygame.draw.circle(screen, (245, 245, 245), CENTER, 6)

        digital = self.font_big.render(now.strftime("%M:%S"), True, DARK)
        screen.blit(digital, digital.get_rect(center=(CENTER[0], 610)))
        hint = self.font_small.render("Right glove: minutes   |   Left glove: seconds   |   ESC: quit", True, DARK)
        screen.blit(hint, hint.get_rect(center=(CENTER[0], 670)))
