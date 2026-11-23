"""TSIS 2 - Paint Application: Extended Drawing Tools.

Controls:
  P pencil | L line | R rectangle | C circle | E eraser | I color picker
  Q square | T right triangle | Y equilateral triangle | H rhombus
  F flood fill | X text | 1/2/3 brush size | Ctrl+S save | Esc cancel text
"""
import os
from datetime import datetime

import pygame
from tools import draw_shape, flood_fill, draw_freehand


pygame.init()
pygame.font.init()

WIDTH, HEIGHT = 1100, 720
TOOLBAR_H = 104
CANVAS_MARGIN = 14
CANVAS_W = WIDTH - 2 * CANVAS_MARGIN
CANVAS_H = HEIGHT - TOOLBAR_H - CANVAS_MARGIN

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("TSIS 2 - Paint Application")
clock = pygame.time.Clock()

FONT = pygame.font.SysFont("arial", 16)
SMALL_FONT = pygame.font.SysFont("arial", 13)
TEXT_FONT = pygame.font.SysFont("arial", 24)

WHITE = (255, 255, 255)
BLACK = (20, 20, 20)
BG = (235, 238, 242)
PANEL = (248, 249, 251)
BORDER = (190, 196, 204)
ACCENT = (55, 112, 190)
PALETTE = [
    (0, 0, 0), (255, 255, 255), (220, 40, 40), (30, 150, 70),
    (40, 95, 210), (245, 205, 40), (150, 70, 190), (240, 125, 30),
    (90, 90, 90), (120, 190, 200), (245, 150, 180), (125, 85, 50),
]
TOOLS = [
    ("Pencil", "pencil", "P"), ("Line", "line", "L"),
    ("Rect", "rectangle", "R"), ("Circle", "circle", "C"),
    ("Eraser", "eraser", "E"), ("Picker", "picker", "I"),
    ("Square", "square", "Q"), ("Right tri", "right triangle", "T"),
    ("Equi tri", "equilateral triangle", "Y"), ("Rhombus", "rhombus", "H"),
    ("Fill", "fill", "F"), ("Text", "text", "X"),
]
SIZES = [2, 5, 10]

canvas_rect = pygame.Rect(CANVAS_MARGIN, TOOLBAR_H, CANVAS_W, CANVAS_H)
canvas = pygame.Surface((CANVAS_W, CANVAS_H))
canvas.fill(WHITE)
current_color = BLACK
brush_index = 1
active_tool = "pencil"
drawing = False
shape_start = None
last_pos = None
preview_end = None
text_active = False
text_pos = None
text_buffer = ""
status_message = "Ready"
status_until = 0

def set_status(message, duration=2200):
    global status_message, status_until
    status_message = message
    status_until = pygame.time.get_ticks() + duration

def canvas_pos(pos):
    return (pos[0] - canvas_rect.x, pos[1] - canvas_rect.y)

def inside_canvas(pos):
    return canvas_rect.collidepoint(pos)

def save_canvas():
    os.makedirs("saves", exist_ok=True)
    stamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    filename = os.path.join("saves", f"paint_{stamp}.png")
    pygame.image.save(canvas, filename)
    set_status(f"Saved: {filename}")

def commit_text():
    global text_active, text_buffer, text_pos
    if text_buffer.strip():
        rendered = TEXT_FONT.render(text_buffer, True, current_color)
        canvas.blit(rendered, text_pos)
    text_active = False
    text_buffer = ""
    text_pos = None

def cancel_text():
    global text_active, text_buffer, text_pos
    text_active = False
    text_buffer = ""
    text_pos = None

def activate_tool(tool):
    global active_tool, drawing, shape_start, preview_end
    if text_active:
        cancel_text()
    active_tool = tool
    drawing = False
    shape_start = None
    preview_end = None

def button_rects():
    rects = {}
    x0, y0 = 12, 9
    bw, bh, gap = 78, 31, 5
    for i, (label, tool, key) in enumerate(TOOLS):
        row, col = divmod(i, 6)
        rects[tool] = pygame.Rect(x0 + col * (bw + gap), y0 + row * (bh + 5), bw, bh)
    return rects

TOOL_RECTS = button_rects()
palette_rects = [pygame.Rect(520 + i * 25, 81, 19, 15) for i in range(len(PALETTE))]
size_rects = [pygame.Rect(850 + i * 62, 17, 55, 29) for i in range(3)]
save_rect = pygame.Rect(850, 57, 180, 31)

def draw_toolbar():
    pygame.draw.rect(screen, PANEL, (0, 0, WIDTH, TOOLBAR_H))
    pygame.draw.line(screen, BORDER, (0, TOOLBAR_H - 1), (WIDTH, TOOLBAR_H - 1), 1)

    for label, tool, key in TOOLS:
        rect = TOOL_RECTS[tool]
        selected = active_tool == tool
        pygame.draw.rect(screen, (220, 233, 250) if selected else (238, 240, 244), rect, border_radius=5)
        pygame.draw.rect(screen, ACCENT if selected else BORDER, rect, 2 if selected else 1, border_radius=5)
        txt = SMALL_FONT.render(f"{label} [{key}]", True, BLACK)
        screen.blit(txt, txt.get_rect(center=rect.center))

    screen.blit(FONT.render("Color:", True, BLACK), (465, 79))
    for i, rect in enumerate(palette_rects):
        pygame.draw.rect(screen, PALETTE[i], rect)
        pygame.draw.rect(screen, ACCENT if current_color == PALETTE[i] else BORDER, rect, 2 if current_color == PALETTE[i] else 1)

    screen.blit(FONT.render("Brush size:", True, BLACK), (850, 4))
    for i, rect in enumerate(size_rects):
        selected = brush_index == i
        pygame.draw.rect(screen, (220, 233, 250) if selected else (238, 240, 244), rect, border_radius=4)
        pygame.draw.rect(screen, ACCENT if selected else BORDER, rect, 2 if selected else 1, border_radius=4)
        label = ["1  Small", "2  Medium", "3  Large"][i]
        screen.blit(SMALL_FONT.render(label, True, BLACK), (rect.x + 4, rect.y + 8))

    pygame.draw.rect(screen, (225, 239, 228), save_rect, border_radius=5)
    pygame.draw.rect(screen, (90, 150, 100), save_rect, 1, border_radius=5)
    screen.blit(FONT.render("Save PNG  (Ctrl+S)", True, BLACK), (save_rect.x + 28, save_rect.y + 7))
    screen.blit(SMALL_FONT.render(f"Active: {active_tool}  |  Stroke: {SIZES[brush_index]} px", True, BLACK), (465, 45))
    help_text = "Shortcuts: P pencil, L line, F fill, X text, 1-3 size"
    screen.blit(SMALL_FONT.render(help_text, True, (85, 90, 98)), (465, 61))

def draw_canvas():
    screen.blit(canvas, canvas_rect.topleft)
    pygame.draw.rect(screen, BORDER, canvas_rect, 1)
    if drawing and shape_start is not None and preview_end is not None:
        preview = canvas.copy()
        color = WHITE if active_tool == "eraser" else current_color
        tool = "rectangle" if active_tool == "eraser" else active_tool
        draw_shape(preview, tool, shape_start, preview_end, color, SIZES[brush_index])
        screen.blit(preview, canvas_rect.topleft)
    if text_active and text_pos is not None:
        preview = TEXT_FONT.render(text_buffer, True, current_color)
        screen.blit(preview, (canvas_rect.x + text_pos[0], canvas_rect.y + text_pos[1]))
        cursor_x = text_pos[0] + preview.get_width() + 1
        cursor_y = text_pos[1]
        pygame.draw.line(screen, current_color,
                         (canvas_rect.x + cursor_x, canvas_rect.y + cursor_y),
                         (canvas_rect.x + cursor_x, canvas_rect.y + cursor_y + TEXT_FONT.get_height()), 1)

def choose_color(pos):
    for i, rect in enumerate(palette_rects):
        if rect.collidepoint(pos):
            return PALETTE[i]
    return None

def set_brush(index):
    global brush_index
    brush_index = max(0, min(2, index))

running = True
while running:
    mouse = pygame.mouse.get_pos()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.KEYDOWN:
            if text_active:
                if event.key == pygame.K_RETURN:
                    commit_text()
                elif event.key == pygame.K_ESCAPE:
                    cancel_text()
                elif event.key == pygame.K_BACKSPACE:
                    text_buffer = text_buffer[:-1]
                elif event.unicode and event.unicode.isprintable():
                    text_buffer += event.unicode
                continue

            if event.key == pygame.K_ESCAPE:
                drawing = False
                shape_start = None
                preview_end = None
            elif event.key == pygame.K_1:
                set_brush(0)
            elif event.key == pygame.K_2:
                set_brush(1)
            elif event.key == pygame.K_3:
                set_brush(2)
            elif (event.key == pygame.K_s and
                  (pygame.key.get_mods() & pygame.KMOD_CTRL)):
                save_canvas()
            else:
                shortcuts = {
                    pygame.K_p: "pencil", pygame.K_l: "line",
                    pygame.K_r: "rectangle", pygame.K_c: "circle",
                    pygame.K_e: "eraser", pygame.K_i: "picker",
                    pygame.K_q: "square", pygame.K_t: "right triangle",
                    pygame.K_y: "equilateral triangle", pygame.K_h: "rhombus",
                    pygame.K_f: "fill", pygame.K_x: "text",
                }
                if event.key in shortcuts:
                    activate_tool(shortcuts[event.key])

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            color = choose_color(event.pos)
            if color is not None:
                current_color = color
                continue
            if save_rect.collidepoint(event.pos):
                save_canvas()
                continue
            size_hit = next((i for i, r in enumerate(size_rects) if r.collidepoint(event.pos)), None)
            if size_hit is not None:
                set_brush(size_hit)
                continue
            tool_hit = next((tool for tool, rect in TOOL_RECTS.items() if rect.collidepoint(event.pos)), None)
            if tool_hit:
                activate_tool(tool_hit)
                continue
            if inside_canvas(event.pos):
                pos = canvas_pos(event.pos)
                if active_tool == "picker":
                    current_color = tuple(canvas.get_at(pos))[:3]
                    activate_tool("pencil")
                elif active_tool == "fill":
                    flood_fill(canvas, pos, current_color)
                elif active_tool == "text":
                    text_active = True
                    text_pos = pos
                    text_buffer = ""
                elif active_tool == "pencil":
                    drawing = True
                    last_pos = pos
                    draw_freehand(canvas, pos, pos, current_color, SIZES[brush_index])
                elif active_tool == "eraser":
                    drawing = True
                    last_pos = pos
                    draw_freehand(canvas, pos, pos, WHITE, SIZES[brush_index])
                else:
                    drawing = True
                    shape_start = pos
                    preview_end = pos

        elif event.type == pygame.MOUSEMOTION:
            if drawing and inside_canvas(event.pos):
                pos = canvas_pos(event.pos)
                if active_tool == "pencil":
                    draw_freehand(canvas, last_pos, pos, current_color, SIZES[brush_index])
                    last_pos = pos
                elif active_tool == "eraser":
                    draw_freehand(canvas, last_pos, pos, WHITE, SIZES[brush_index])
                    last_pos = pos
                else:
                    preview_end = pos

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            if drawing:
                if active_tool not in ("pencil", "eraser") and shape_start is not None:
                    end = canvas_pos(event.pos)
                    end = (max(0, min(CANVAS_W - 1, end[0])), max(0, min(CANVAS_H - 1, end[1])))
                    color = current_color
                    draw_shape(canvas, active_tool, shape_start, end, color, SIZES[brush_index])
                drawing = False
                shape_start = None
                preview_end = None

    screen.fill(BG)
    draw_toolbar()
    draw_canvas()
    if pygame.time.get_ticks() < status_until:
        msg = SMALL_FONT.render(status_message, True, (55, 105, 65))
        screen.blit(msg, (14, HEIGHT - 18))
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
