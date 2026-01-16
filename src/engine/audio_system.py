#!/usr/bin/env python3
"""Audio System - 3D Sound Simulation with positional audio"""

import pygame
import math
from typing import Optional, Tuple


class AudioSystem:
    """Manages game audio with 3D sound simulation"""

    def __init__(self):
        pygame.mixer.init()
        self.mixer = pygame.mixer
        self.mixer.set_num_channels(16)
        
        # Master volume
        self.master_volume = 0.7
        self.sfx_volume = 0.8
        self.music_volume = 0.5
        
        # 3D audio settings
        self.listener_pos = (0, 0, 0)
        self.doppler_factor = 1.0
        
        # Sound cache
        self.sounds = {}
        self.music = None
        
        # Preload dummy sounds (will be replaced with actual sounds)
        self._init_sounds()

    def _init_sounds(self):
        """Initialize sound system with placeholder sounds"""
        # Create dummy sounds using frequencies
        self.sounds['move'] = self._create_beep(440, 0.1)
        self.sounds['merge'] = self._create_beep(523, 0.15)
        self.sounds['merge_big'] = self._create_beep(659, 0.2)
        self.sounds['game_over'] = self._create_beep(200, 0.5)
        self.sounds['win'] = self._create_tune([523, 659, 784, 1047], 0.2)
        self.sounds['click'] = self._create_beep(880, 0.05)
        self.sounds['level_up'] = self._create_tune([440, 523, 587, 659, 784], 0.1)

    def _create_beep(self, frequency: float, duration: float) -> pygame.mixer.Sound:
        """Create a simple beep sound"""
        sample_rate = 44100
        samples = int(sample_rate * duration)
        
        # Generate sine wave
        import numpy as np
        t = np.linspace(0, duration, samples, False)
        wave = np.sin(2 * np.pi * frequency * t)
        
        # Apply envelope
        envelope = np.exp(-3 * t / duration)
        wave *= envelope
        
        # Convert to 16-bit PCM
        wave = (wave * 32767).astype(np.int16)
        
        # Create stereo sound
        stereo_wave = np.column_stack((wave, wave))
        
        sound = pygame.mixer.Sound(stereo_wave)
        return sound

    def _create_tune(self, frequencies: list, duration: float) -> pygame.mixer.Sound:
        """Create a simple melody"""
        sample_rate = 44100
        samples_per_note = int(sample_rate * duration)
        
        import numpy as np
        wave = np.array([], dtype=np.float32)
        
        for freq in frequencies:
            t = np.linspace(0, duration, samples_per_note, False)
            note_wave = np.sin(2 * np.pi * freq * t)
            envelope = np.exp(-4 * t / duration)
            note_wave *= envelope
            wave = np.concatenate((wave, note_wave))
        
        # Convert to 16-bit PCM
        wave = (wave * 32767).astype(np.int16)
        
        # Create stereo sound
        stereo_wave = np.column_stack((wave, wave))
        
        sound = pygame.mixer.Sound(stereo_wave)
        return sound

    def play_sound(self, sound_name: str, position: Optional[Tuple[float, float, float]] = None,
                   volume: Optional[float] = None) -> pygame.mixer.Channel:
        """Play a sound with optional 3D positioning"""
        if sound_name not in self.sounds:
            return None
        
        sound = self.sounds[sound_name]
        channel = sound.play()
        
        if channel:
            # Apply volume
            if volume is None:
                volume = self.sfx_volume
            channel.set_volume(volume * self.master_volume)
            
            # Apply 3D positioning
            if position:
                self._apply_3d_position(channel, position)
        
        return channel

    def _apply_3d_position(self, channel: pygame.mixer.Channel, 
                           position: Tuple[float, float, float]):
        """Simulate 3D audio with panning and volume"""
        # Calculate distance from listener
        dx = position[0] - self.listener_pos[0]
        dy = position[1] - self.listener_pos[1]
        dz = position[2] - self.listener_pos[2]
        distance = math.sqrt(dx**2 + dy**2 + dz**2)
        
        # Volume falloff
        max_distance = 500
        volume_factor = max(0, 1 - distance / max_distance)
        
        # Panning (left-right)
        pan = dx / (max_distance if max_distance > 0 else 1)
        left_volume = max(0, min(1, 1 - pan))
        right_volume = max(0, min(1, 1 + pan))
        
        # Apply to channel
        current_volume = channel.get_volume()
        channel.set_volume(left_volume * current_volume * volume_factor,
                          right_volume * current_volume * volume_factor)

    def update_listener_position(self, position: Tuple[float, float, float]):
        """Update listener position for 3D audio"""
        self.listener_pos = position

    def play_move_sound(self, position: Optional[Tuple[float, float]] = None):
        """Play move sound"""
        pos_3d = (position[0], position[1], 0) if position else None
        self.play_sound('move', pos_3d)

    def play_merge_sound(self, value: int, position: Optional[Tuple[float, float]] = None):
        """Play merge sound with appropriate pitch"""
        pos_3d = (position[0], position[1], 0) if position else None
        if value >= 1024:
            self.play_sound('merge_big', pos_3d, volume=1.0)
        else:
            self.play_sound('merge', pos_3d)

    def play_game_over_sound(self):
        """Play game over sound"""
        self.play_sound('game_over', volume=0.8)

    def play_win_sound(self):
        """Play win sound"""
        self.play_sound('win', volume=1.0)

    def play_level_up_sound(self):
        """Play level up sound"""
        self.play_sound('level_up', volume=0.9)

    def play_click_sound(self):
        """Play click sound for UI"""
        self.play_sound('click', volume=0.5)

    def set_master_volume(self, volume: float):
        """Set master volume (0.0 - 1.0)"""
        self.master_volume = max(0.0, min(1.0, volume))

    def set_sfx_volume(self, volume: float):
        """Set SFX volume (0.0 - 1.0)"""
        self.sfx_volume = max(0.0, min(1.0, volume))

    def set_music_volume(self, volume: float):
        """Set music volume (0.0 - 1.0)"""
        self.music_volume = max(0.0, min(1.0, volume))
        if self.music:
            self.music.set_volume(self.music_volume)

    def fade_out_all(self, time_ms: int = 500):
        """Fade out all sounds"""
        pygame.mixer.fadeout(time_ms)

    def cleanup(self):
        """Clean up audio resources"""
        pygame.mixer.quit()
