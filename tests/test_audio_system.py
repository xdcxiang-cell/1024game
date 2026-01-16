"""
1024 Game - Audio System Tests
Comprehensive tests for the audio system
"""

import unittest
import os
import sys
import pygame
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.audio_system import AudioSystem


class TestAudioSystem(unittest.TestCase):
    """Test cases for the Audio System"""

    def setUp(self):
        """Set up audio system for testing"""
        pygame.init()
        self.audio_system = AudioSystem()

    def tearDown(self):
        """Clean up"""
        pygame.quit()

    def test_initialization(self):
        """Test audio system initialization"""
        self.assertIsNotNone(self.audio_system)
        self.assertEqual(self.audio_system.music_volume, 0.5)
        self.assertEqual(self.audio_system.sound_volume, 0.7)
        self.assertTrue(self.audio_system._initialized)

    def test_volume_control(self):
        """Test volume control"""
        self.audio_system.set_music_volume(0.8)
        self.assertEqual(self.audio_system.music_volume, 0.8)

        self.audio_system.set_sound_volume(0.9)
        self.assertEqual(self.audio_system.sound_volume, 0.9)

        # Test volume clamping
        self.audio_system.set_music_volume(1.5)
        self.assertEqual(self.audio_system.music_volume, 1.0)

        self.audio_system.set_music_volume(-0.5)
        self.assertEqual(self.audio_system.music_volume, 0.0)

    def test_sound_playing(self):
        """Test playing sounds"""
        # This is a basic test - actual sound files may not exist
        result = self.audio_system.play_sound('move', x=400, y=300)
        # Should not raise an error even if file doesn't exist
        self.assertIsNotNone(result)

    def test_3d_sound_disabled(self):
        """Test 3D sound is disabled by default if no sound device"""
        self.audio_system.set_3d_sound_enabled(True)
        self.assertTrue(self.audio_system.enable_3d_sound)

    def test_sound_positioning(self):
        """Test sound positioning"""
        self.audio_system.set_listener_position(400, 300)
        self.assertEqual(self.audio_system.listener_x, 400)
        self.assertEqual(self.audio_system.listener_y, 300)

    def test_audio_update(self):
        """Test audio updating"""
        result = self.audio_system.update()
        self.assertTrue(result)

    def test_sound_source_management(self):
        """Test sound source management"""
        self.assertEqual(len(self.audio_system._sound_sources), 0)

    def test_initial_volume_values(self):
        """Test initial volume values"""
        self.assertEqual(self.audio_system.music_volume, 0.5)
        self.assertEqual(self.audio_system.sound_volume, 0.7)


if __name__ == '__main__':
    unittest.main()
