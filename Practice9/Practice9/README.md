# Practice 09 — Game Development with Pygame (Part 1)

Three independent Pygame applications are included.

## Requirements

- Python 3.9+
- Pygame 2.x

Install dependencies:

```bash
python -m pip install -r requirements.txt
```

## Run each application

From the `Practice7` project root:

```bash
python mickeys_clock/main.py
python music_player/main.py
python moving_ball/main.py
```

On Windows with the Python launcher, you can use `py -3.13` instead of `python`.

## Applications

### 1. Mickey's Clock
- Reads local system time.
- Displays minutes and seconds (`MM:SS`).
- The right glove hand indicates minutes; the left glove hand indicates seconds.
- Refreshes continuously; press Escape to quit.
- The supplied glove sprite is a simple original cartoon-style graphic.

### 2. Music Player
- Uses `pygame.mixer.music`.
- Keyboard: P = play, S = stop, N = next, B = previous, Q = quit.
- Shows current filename, playlist position and playback progress for WAV files.
- Automatically discovers `.wav`, `.mp3`, and `.ogg` files in `music/`.
- Two short generated WAV sample tracks are included. Add your own tracks to `music/`.

### 3. Moving Ball
- Red ball with radius 25 px on a white background.
- Arrow keys move the ball by 20 px.
- Moves that would take any part of the ball outside the window are ignored.
- Escape or window close quits.

## Suggested Git commits

```bash
git add .
git commit -m "Add Practice 09 Pygame applications"
git commit -m "Implement Mickey clock and animated glove hands"
git commit -m "Add keyboard music player and sample playlist"
git commit -m "Add boundary-checked moving ball game"
```
