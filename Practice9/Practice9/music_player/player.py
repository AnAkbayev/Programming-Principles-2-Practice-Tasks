"""Playlist and pygame.mixer.music wrapper."""
from pathlib import Path
import wave
import pygame

SUPPORTED = {".wav", ".mp3", ".ogg"}

class MusicPlayer:
    def __init__(self):
        self.music_dir = Path(__file__).parent / "music"
        self.music_dir.mkdir(exist_ok=True)
        self.tracks = sorted(
            p for p in self.music_dir.rglob("*")
            if p.is_file() and p.suffix.lower() in SUPPORTED
        )
        self.index = 0
        self.started_at_ms = 0
        self.paused_at_ms = 0
        self.paused = False
        self.duration_cache = {}
        self.mixer_ready = False
        try:
            pygame.mixer.init()
            self.mixer_ready = True
        except pygame.error as exc:
            print("Audio device could not be initialized:", exc)

    def has_track(self):
        return bool(self.tracks)

    def current_track_name(self):
        if not self.tracks:
            return "No audio files in music/"
        return self.tracks[self.index].name

    def playlist_position(self):
        return self.index + 1 if self.tracks else 0

    def playlist_length(self):
        return len(self.tracks)

    def _duration(self, path):
        if path in self.duration_cache:
            return self.duration_cache[path]
        duration = 0.0
        if path.suffix.lower() == ".wav":
            try:
                with wave.open(str(path), "rb") as wav:
                    duration = wav.getnframes() / float(wav.getframerate())
            except (wave.Error, OSError, ZeroDivisionError):
                pass
        self.duration_cache[path] = duration
        return duration

    def play(self):
        if not self.mixer_ready or not self.tracks:
            return
        if self.paused:
            pygame.mixer.music.unpause()
            self.paused = False
            return
        try:
            pygame.mixer.music.load(str(self.tracks[self.index]))
            pygame.mixer.music.play()
            self.started_at_ms = pygame.time.get_ticks()
            self.paused_at_ms = 0
        except pygame.error as exc:
            print("Could not play track:", exc)

    def stop(self):
        if self.mixer_ready:
            pygame.mixer.music.stop()
        self.paused = False
        self.started_at_ms = 0
        self.paused_at_ms = 0

    def next_track(self):
        if not self.tracks:
            return
        self.index = (self.index + 1) % len(self.tracks)
        self.stop()
        self.play()

    def previous_track(self):
        if not self.tracks:
            return
        self.index = (self.index - 1) % len(self.tracks)
        self.stop()
        self.play()

    def is_playing(self):
        return self.mixer_ready and pygame.mixer.music.get_busy() and not self.paused

    def progress(self):
        if not self.tracks:
            return 0.0, 0.0
        duration = self._duration(self.tracks[self.index])
        if self.started_at_ms == 0:
            return 0.0, duration
        if self.paused:
            elapsed = self.paused_at_ms / 1000.0
        else:
            elapsed = max(0, (pygame.time.get_ticks() - self.started_at_ms) / 1000.0)
        if duration:
            elapsed = min(elapsed, duration)
        return elapsed, duration

    def update(self):
        if self.mixer_ready and self.tracks and self.started_at_ms and not self.paused:
            if not pygame.mixer.music.get_busy():
                # Advance automatically when the current track ends.
                self.index = (self.index + 1) % len(self.tracks)
                self.started_at_ms = 0
                self.play()

    def shutdown(self):
        if self.mixer_ready:
            pygame.mixer.music.stop()
            pygame.mixer.quit()
