import pygame
import random
import math
from typing import List, Tuple, Optional
from src.config import Config


class Sound3D:
    def __init__(self, x: float, y: float, volume: float = 1.0):
        self.x = x
        self.y = y
        self.volume = volume

    def calculate_pan(self, listener_x: float, screen_width: float) -> float:
        relative_x = (self.x - listener_x) / (screen_width / 2)
        return max(-1.0, min(1.0, relative_x))

    def calculate_distance_volume(self, listener_x: float, listener_y: float,
                                  screen_width: float, screen_height: float) -> float:
        dx = (self.x - listener_x) / screen_width
        dy = (self.y - listener_y) / screen_height
        distance = math.sqrt(dx * dx + dy * dy)
        return self.volume * max(0.0, 1.0 - distance * 0.5)


class AudioEngine:
    def __init__(self):
        pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=512)
        self.config = Config()
        self.enabled = self.config.get('audio', 'enabled', default=True)
        self.master_volume = self.config.get('audio', 'volume', default=0.7)
        self.sfx_volume = self.config.get('audio', 'sfx_volume', default=0.8)
        self.sounds = {}
        self.listener_pos = (400, 300)
        self.screen_size = (800, 600)

    def generate_tone(self, frequency: float, duration: float, volume: float = 0.5) -> pygame.mixer.Sound:
        sample_rate = 44100
        n_samples = int(sample_rate * duration)
        buffer = bytearray()

        for i in range(n_samples):
            t = float(i) / sample_rate
            value = int(32767 * volume * math.sin(2 * math.pi * frequency * t))
            buffer.extend([value & 0xFF, (value >> 8) & 0xFF])

        return pygame.mixer.Sound(buffer=bytes(buffer))

    def generate_merge_sound(self, tile_value: int) -> pygame.mixer.Sound:
        base_freq = 200 + min(tile_value, 2048) / 10
        duration = 0.1 + min(tile_value, 2048) / 10000
        return self.generate_tone(base_freq, duration, 0.3)

    def generate_move_sound(self) -> pygame.mixer.Sound:
        return self.generate_tone(150, 0.05, 0.2)

    def generate_spawn_sound(self) -> pygame.mixer.Sound:
        return self.generate_tone(300, 0.08, 0.25)

    def generate_win_sound(self) -> pygame.mixer.Sound:
        return self.generate_tone(523.25, 0.5, 0.4)

    def generate_game_over_sound(self) -> pygame.mixer.Sound:
        return self.generate_tone(100, 0.8, 0.3)

    def generate_ui_sound(self, sound_type: str = 'click') -> pygame.mixer.Sound:
        if sound_type == 'click':
            return self.generate_tone(800, 0.05, 0.2)
        elif sound_type == 'hover':
            return self.generate_tone(600, 0.03, 0.15)
        elif sound_type == 'back':
            return self.generate_tone(400, 0.1, 0.25)
        return self.generate_tone(500, 0.05, 0.2)

    def play_sound_3d(self, sound: pygame.mixer.Sound, x: float, y: float):
        if not self.enabled or not sound:
            return

        sound_3d = Sound3D(x, y)
        pan = sound_3d.calculate_pan(self.listener_pos[0], self.screen_size[0])
        volume = sound_3d.calculate_distance_volume(
            self.listener_pos[0], self.listener_pos[1],
            self.screen_size[0], self.screen_size[1]
        )

        final_volume = self.master_volume * self.sfx_volume * volume

        if final_volume > 0.01:
            sound.set_volume(final_volume)
            sound.play()

    def play_merge(self, tile_value: int, x: float, y: float):
        sound = self.generate_merge_sound(tile_value)
        self.play_sound_3d(sound, x, y)

    def play_move(self, x: float, y: float):
        sound = self.generate_move_sound()
        self.play_sound_3d(sound, x, y)

    def play_spawn(self, x: float, y: float):
        sound = self.generate_spawn_sound()
        self.play_sound_3d(sound, x, y)

    def play_win(self, x: float, y: float):
        sound = self.generate_win_sound()
        self.play_sound_3d(sound, x, y)

    def play_game_over(self, x: float, y: float):
        sound = self.generate_game_over_sound()
        self.play_sound_3d(sound, x, y)

    def play_ui(self, sound_type: str = 'click'):
        sound = self.generate_ui_sound(sound_type)
        if self.enabled and sound:
            sound.set_volume(self.master_volume * self.sfx_volume * 0.5)
            sound.play()

    def set_listener_position(self, x: float, y: float):
        self.listener_pos = (x, y)

    def set_screen_size(self, width: int, height: int):
        self.screen_size = (width, height)

    def set_enabled(self, enabled: bool):
        self.enabled = enabled

    def set_master_volume(self, volume: float):
        self.master_volume = max(0.0, min(1.0, volume))

    def set_sfx_volume(self, volume: float):
        self.sfx_volume = max(0.0, min(1.0, volume))

    def cleanup(self):
        pygame.mixer.quit()
