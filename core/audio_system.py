"""
1024 Game - Audio System
Handles 3D sound simulation and audio effects
"""

import pygame
import os
from typing import Optional, Tuple, Dict, List
from dataclasses import dataclass
import math
import threading
import time
from queue import Queue, Empty


@dataclass
class SoundSource:
    x: float
    y: float
    z: float
    radius: float
    volume: float
    looping: bool
    playing: bool


class AudioSystem:
    """Manages 3D sound simulation and audio playback"""
    
    def __init__(self, settings: Optional[Dict] = None):
        self.settings = settings or {}
        self.music_volume = self.settings.get('music_volume', 0.5)
        self.sound_volume = self.settings.get('sound_volume', 0.7)
        self.sound_3d_enabled = self.settings.get('3d_sound', True)
        
        self.sounds: Dict[str, pygame.mixer.Sound] = {}
        self.music_tracks: List[str] = []
        self.current_music: Optional[str] = None
        self.sound_sources: Dict[int, SoundSource] = {}
        self.source_counter = 0
        
        self._initialized = False
        self._thread: Optional[threading.Thread] = None
        self._running = False
        self._command_queue: Queue = Queue()
        self._listener_pos = (0.0, 0.0, 0.0)
        
        self._load_audio_assets()
        
    def _load_audio_assets(self) -> None:
        """Load audio assets"""
        try:
            pygame.mixer.init(frequency=44100, size=-16, channels=2, buffer=4096)
            pygame.mixer.set_num_channels(32)
            
            audio_dir = os.path.join(os.path.dirname(__file__), '../assets/audio')
            
            # Load sound effects
            sound_files = {
                'merge': 'merge.wav',
                'move': 'move.wav',
                'tile_spawn': 'tile_spawn.wav',
                'level_complete': 'level_complete.wav',
                'game_over': 'game_over.wav',
                'click': 'click.wav',
                'button_hover': 'button_hover.wav',
                'achievement_unlocked': 'achievement_unlocked.wav'
            }
            
            for name, filename in sound_files.items():
                filepath = os.path.join(audio_dir, filename)
                if os.path.exists(filepath):
                    try:
                        self.sounds[name] = pygame.mixer.Sound(filepath)
                    except:
                        pass  # Sound file might be missing
            
            # Load music tracks
            music_dir = os.path.join(audio_dir, 'music')
            if os.path.exists(music_dir):
                for filename in os.listdir(music_dir):
                    if filename.endswith(('.wav', '.mp3', '.ogg')):
                        self.music_tracks.append(os.path.join(music_dir, filename))
            
            self._initialized = True
            
        except Exception as e:
            print("Audio initialization failed: %s" % e)
            self._initialized = False
    
    def start(self) -> None:
        """Start audio processing thread"""
        if self._running:
            return
            
        self._running = True
        self._thread = threading.Thread(target=self._audio_thread, daemon=True)
        self._thread.start()
    
    def stop(self) -> None:
        """Stop audio processing"""
        self._running = False
        if self._thread:
            self._command_queue.put(None)
            self._thread.join(timeout=2.0)
            self._thread = None
            
        pygame.mixer.stop()
    
    def _audio_thread(self) -> None:
        """Background audio processing thread"""
        while self._running:
            try:
                command = self._command_queue.get(timeout=0.1)
                
                if command is None:
                    break
                    
                cmd_type, *args = command
                
                if cmd_type == 'play_sound':
                    sound_name, x, y, z = args
                    self._play_3d_sound(sound_name, x, y, z)
                    
                elif cmd_type == 'update_listener':
                    self._listener_pos = args[0]
                    
                elif cmd_type == 'play_music':
                    self._play_music_track(args[0])
                    
                elif cmd_type == 'stop_music':
                    pygame.mixer.music.stop()
                    
            except Empty:
                continue
            except Exception as e:
                print("Audio thread error: %s" % e)
    
    def _play_3d_sound(self, sound_name: str, x: float, y: float, z: float = 0.0) -> None:
        """Play a sound with 3D positioning"""
        if not self._initialized:
            return
            
        sound = self.sounds.get(sound_name)
        if not sound:
            return
            
        if self.sound_3d_enabled:
            # Calculate 3D effects
            dx = x - self._listener_pos[0]
            dy = y - self._listener_pos[1]
            dz = z - self._listener_pos[2]
            
            distance = math.sqrt(dx**2 + dy**2 + dz**2)
            
            # Calculate volume based on distance
            max_distance = 500.0
            volume = max(0.0, 1.0 - distance / max_distance)
            volume *= self.sound_volume
            
            if volume > 0:
                # Calculate panning (left-right balance)
                pan_range = 200.0  # pixels
                pan = max(-1.0, min(1.0, dx / pan_range))
                
                # Apply 3D effects using pygame mixer channels
                channel = pygame.mixer.find_channel()
                if channel:
                    # Set volume for left/right based on pan
                    left_vol = volume * (1.0 - pan) / 2 if pan > 0 else volume
                    right_vol = volume * (1.0 + pan) / 2 if pan < 0 else volume
                    
                    channel.set_volume(left_vol, right_vol)
                    channel.play(sound)
                    
                    # Store sound source info
                    self.sound_sources[id(channel)] = SoundSource(
                        x=x, y=y, z=z, radius=50, volume=volume,
                        looping=False, playing=True
                    )
        else:
            # Play without 3D effects
            channel = pygame.mixer.find_channel()
            if channel:
                channel.set_volume(self.sound_volume)
                channel.play(sound)
    
    def play_sound(self, sound_name: str, x: float = 0.0, y: float = 0.0, z: float = 0.0) -> None:
        """Queue a sound to be played"""
        if self._running:
            self._command_queue.put(('play_sound', sound_name, x, y, z))
    
    def play_move_sound(self, direction: str, grid_center: Tuple[float, float]) -> None:
        """Play move sound with direction-based positioning"""
        x, y = grid_center
        offset = 50
        
        if direction == 'up':
            self.play_sound('move', x, y - offset)
        elif direction == 'down':
            self.play_sound('move', x, y + offset)
        elif direction == 'left':
            self.play_sound('move', x - offset, y)
        elif direction == 'right':
            self.play_sound('move', x + offset, y)
        else:
            self.play_sound('move', x, y)
    
    def play_merge_sound(self, row: int, col: int, grid_offset: Tuple[float, float], 
                        cell_size: float, padding: float) -> None:
        """Play merge sound at tile position"""
        x = grid_offset[0] + col * (cell_size + padding) + cell_size // 2
        y = grid_offset[1] + row * (cell_size + padding) + cell_size // 2
        self.play_sound('merge', x, y)
    
    def play_level_complete_sound(self) -> None:
        """Play level complete sound"""
        self.play_sound('level_complete', self._listener_pos[0], self._listener_pos[1])
    
    def play_game_over_sound(self) -> None:
        """Play game over sound"""
        self.play_sound('game_over', self._listener_pos[0], self._listener_pos[1])
    
    def play_click_sound(self) -> None:
        """Play click sound"""
        self.play_sound('click', self._listener_pos[0], self._listener_pos[1])
    
    def play_achievement_sound(self) -> None:
        """Play achievement unlocked sound"""
        self.play_sound('achievement_unlocked', self._listener_pos[0], self._listener_pos[1])
    
    def _play_music_track(self, track_index: int = 0) -> None:
        """Play music track"""
        if not self.music_tracks:
            return
            
        try:
            track_path = self.music_tracks[track_index % len(self.music_tracks)]
            pygame.mixer.music.load(track_path)
            pygame.mixer.music.set_volume(self.music_volume)
            pygame.mixer.music.play(-1)  # Loop indefinitely
            self.current_music = track_path
            
        except Exception as e:
            print("Failed to play music: %s" % e)
    
    def play_music(self, track_index: int = 0) -> None:
        """Queue music playback"""
        if self._running:
            self._command_queue.put(('play_music', track_index))
    
    def stop_music(self) -> None:
        """Stop music"""
        if self._running:
            self._command_queue.put(('stop_music',))
    
    def set_listener_position(self, x: float, y: float, z: float = 0.0) -> None:
        """Set listener position for 3D audio"""
        self._listener_pos = (x, y, z)
    
    def update_listener(self, pos: Tuple[float, float, float]) -> None:
        """Queue listener position update"""
        if self._running:
            self._command_queue.put(('update_listener', pos))
    
    def update_settings(self, settings: Dict) -> None:
        """Update audio settings"""
        self.music_volume = settings.get('music_volume', self.music_volume)
        self.sound_volume = settings.get('sound_volume', self.sound_volume)
        self.sound_3d_enabled = settings.get('3d_sound', self.sound_3d_enabled)
        
        # Update current music volume
        pygame.mixer.music.set_volume(self.music_volume)
    
    def is_initialized(self) -> bool:
        return self._initialized
    
    def fade_out_music(self, milliseconds: int = 1000) -> None:
        """Fade out music"""
        pygame.mixer.music.fadeout(milliseconds)
    
    def create_continuous_sound(self, sound_name: str, x: float, y: float, 
                               z: float = 0.0) -> int:
        """Create continuous sound source"""
        self.source_counter += 1
        self.sound_sources[self.source_counter] = SoundSource(
            x=x, y=y, z=z, radius=100, volume=1.0, looping=True, playing=True
        )
        
        # Start playing the sound
        self.play_sound(sound_name, x, y, z)
        
        return self.source_counter
    
    def stop_continuous_sound(self, source_id: int) -> None:
        """Stop continuous sound source"""
        if source_id in self.sound_sources:
            del self.sound_sources[source_id]
    
    def get_sound_position(self, source_id: int) -> Optional[Tuple[float, float, float]]:
        """Get position of sound source"""
        source = self.sound_sources.get(source_id)
        if source:
            return (source.x, source.y, source.z)
        return None
    
    def set_sound_position(self, source_id: int, x: float, y: float, z: float = 0.0) -> None:
        """Update position of sound source"""
        source = self.sound_sources.get(source_id)
        if source:
            source.x = x
            source.y = y
            source.z = z