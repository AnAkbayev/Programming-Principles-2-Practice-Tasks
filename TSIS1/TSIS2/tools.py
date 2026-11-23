
"""Drawing helpers for the TSIS2 Paint application.

Only Pygame and the Python standard library are used.
"""

from collections import deque
import math
import pygame


def draw_shape(surface, tool, start, end, color, width):
    """Draw a shape using the active stroke width."""

    x1, y1 = map(int, start)
    x2, y2 = map(int, end)

    width = max(1, int(width))

    # Normalize rectangle coordinates.
    rect = pygame.Rect(
        min(x1, x2),
        min(y1, y2),
        abs(x2 - x1),
        abs(y2 - y1)
    )

    if tool == "line":
        pygame.draw.line(surface, color, (x1, y1), (x2, y2), width)

    elif tool == "rectangle":
        if rect.width > 0 and rect.height > 0:
            pygame.draw.rect(surface, color, rect, width)

    elif tool == "circle":
        # Draw an ellipse inside the selected rectangle.
        if rect.width > 0 and rect.height > 0:
            pygame.draw.ellipse(surface, color, rect, width)

    elif tool == "square":
        # Create a square based on the largest drag dimension.
        side = max(abs(x2 - x1), abs(y2 - y1))

        if side > 0:
            sx = side if x2 >= x1 else -side
            sy = side if y2 >= y1 else -side

            square = pygame.Rect(x1, y1, sx, sy)
            square.normalize()

            pygame.draw.rect(surface, color, square, width)

    elif tool == "right triangle":
        points = [
            (x1, y1),
            (x1, y2),
            (x2, y2)
        ]

        pygame.draw.polygon(surface, color, points, width)

    elif tool == "equilateral triangle":
        side = max(1, abs(x2 - x1))
        height = side * math.sqrt(3) / 2

        direction = 1 if y2 >= y1 else -1

        points = [
            (x1, y2),
            (x2, y2),
            (round((x1 + x2) / 2),
             round(y2 - direction * height))
        ]

        pygame.draw.polygon(surface, color, points, width)

    elif tool == "rhombus":
        cx = (x1 + x2) // 2
        cy = (y1 + y2) // 2

        points = [
            (cx, y1),
            (x2, cy),
            (cx, y2),
            (x1, cy)
        ]

        pygame.draw.polygon(surface, color, points, width)


def flood_fill(surface, start_pos, fill_color):
    """Replace a contiguous area of exactly matching color.

    Uses pygame.Surface.get_at() and pygame.Surface.set_at().
    Returns the number of changed pixels.
    """

    x, y = map(int, start_pos)

    surface_width, surface_height = surface.get_size()

    # Check canvas boundaries.
    if not (0 <= x < surface_width and
            0 <= y < surface_height):
        return 0

    target_color = surface.get_at((x, y))

    replacement_color = pygame.Color(
        fill_color[0],
        fill_color[1],
        fill_color[2],
        255
    )

    # Nothing to do if colors are identical.
    if target_color == replacement_color:
        return 0

    queue = deque([(x, y)])
    changed = 0

    while queue:
        px, py = queue.pop()

        if not (0 <= px < surface_width and
                0 <= py < surface_height):
            continue

        # Check whether this pixel matches the original color.
        if surface.get_at((px, py)) != target_color:
            continue

        # Replace the pixel.
        surface.set_at((px, py), replacement_color)
        changed += 1

        # Add neighboring pixels.
        if px > 0:
            queue.append((px - 1, py))

        if px < surface_width - 1:
            queue.append((px + 1, py))

        if py > 0:
            queue.append((px, py - 1))

        if py < surface_height - 1:
            queue.append((px, py + 1))

    return changed


def draw_freehand(surface, previous, current, color, width):
    """Draw a continuous freehand segment."""

    width = max(1, int(width))

    previous = tuple(map(int, previous))
    current = tuple(map(int, current))

    if previous == current:
        pygame.draw.circle(
            surface,
            color,
            current,
            max(1, width // 2)
        )
    else:
        pygame.draw.line(
            surface,
            color,
            previous,
            current,
            width
        )
