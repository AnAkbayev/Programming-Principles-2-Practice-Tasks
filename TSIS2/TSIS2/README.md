# TSIS 2 — Paint Application

A Pygame drawing application implementing the TSIS 2 extended drawing tools.

## Requirements
- Python 3.9+
- Pygame

Install Pygame:

```bash
python -m pip install pygame
```

## Run

From this directory:

```bash
python paint.py
```

## Features
- Pencil/freehand drawing and straight lines with live preview
- Rectangle, circle, square, right triangle, equilateral triangle and rhombus
- Eraser and color picker
- Three stroke widths: 2 px, 5 px and 10 px
- Exact-color flood fill
- Text placement with Enter to confirm and Escape to cancel
- Ctrl+S or the toolbar button saves timestamped PNG files in `saves/`

## Keyboard shortcuts

| Key | Action |
|---|---|
| P | Pencil |
| L | Straight line |
| R | Rectangle |
| C | Circle |
| E | Eraser |
| I | Color picker |
| Q | Square |
| T | Right triangle |
| Y | Equilateral triangle |
| H | Rhombus |
| F | Flood fill |
| X | Text |
| 1 / 2 / 3 | Small / medium / large brush |
| Ctrl+S | Save PNG |
| Enter | Confirm text |
| Escape | Cancel text |

## Project structure

```text
TSIS2/
├── paint.py
├── tools.py
├── README.md
└── assets/
```
