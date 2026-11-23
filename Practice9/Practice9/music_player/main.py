"""Keyboard-controlled music player."""
import pygame
from player import MusicPlayer

WIDTH, HEIGHT = 800, 500

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Practice 09 - Music Player")
    font = pygame.font.SysFont("arial", 24)
    small = pygame.font.SysFont("arial", 18)
    clock = pygame.time.Clock()
    player = MusicPlayer()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_q:
                    running = False
                elif event.key == pygame.K_p:
                    player.play()
                elif event.key == pygame.K_s:
                    player.stop()
                elif event.key == pygame.K_n:
                    player.next_track()
                elif event.key == pygame.K_b:
                    player.previous_track()

        player.update()
        screen.fill((24, 28, 38))
        title = font.render("PYGAME MUSIC PLAYER", True, (245, 245, 250))
        screen.blit(title, (40, 35))
        track = player.current_track_name()
        screen.blit(font.render("Now playing: " + track, True, (235, 205, 120)), (40, 115))
        state = "Playing" if player.is_playing() else ("Paused/Stopped" if player.has_track() else "No tracks found")
        screen.blit(small.render("Status: " + state, True, (205, 215, 225)), (40, 160))

        elapsed, duration = player.progress()
        bar = pygame.Rect(40, 220, 700, 18)
        pygame.draw.rect(screen, (70, 78, 92), bar, border_radius=8)
        fraction = min(1.0, elapsed / duration) if duration > 0 else 0
        fill = pygame.Rect(bar.x, bar.y, int(bar.width * fraction), bar.height)
        pygame.draw.rect(screen, (90, 185, 130), fill, border_radius=8)
        screen.blit(small.render(f"{format_time(elapsed)} / {format_time(duration)}", True, (210, 215, 225)), (40, 250))

        screen.blit(small.render("P: Play   S: Stop   N: Next   B: Previous   Q: Quit", True, (235, 235, 240)), (40, 330))
        screen.blit(small.render(f"Playlist: {player.playlist_position()} / {player.playlist_length()}", True, (175, 190, 205)), (40, 370))
        screen.blit(small.render("Add your own .wav, .mp3 or .ogg files to music/", True, (175, 190, 205)), (40, 405))
        pygame.display.flip()
        clock.tick(30)

    player.shutdown()
    pygame.quit()

def format_time(seconds):
    seconds = max(0, int(seconds))
    return f"{seconds // 60:02d}:{seconds % 60:02d}"

if __name__ == "__main__":
    main()
