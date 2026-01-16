import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.particle_system import Particle, ParticleSystem
from src.audio_engine import AudioEngine, Sound3D


class TestParticle:
    def test_initialization(self):
        particle = Particle(100, 100, (255, 0, 0), 5, (10, 10), 1.0)

        assert particle.x == 100
        assert particle.y == 100
        assert particle.color == (255, 0, 0)
        assert particle.size == 5
        assert particle.velocity == (10, 10)
        assert particle.lifetime == 1.0
        assert particle.alpha == 255

    def test_update(self):
        particle = Particle(100, 100, (255, 0, 0), 5, (10, 10), 1.0)

        alive = particle.update(0.1)

        assert alive is True
        assert particle.x == 101
        assert particle.y == 101
        assert particle.lifetime == 0.9

    def test_update_dead(self):
        particle = Particle(100, 100, (255, 0, 0), 5, (10, 10), 0.1)

        alive = particle.update(0.2)

        assert alive is False

    def test_alpha_decay(self):
        particle = Particle(100, 100, (255, 0, 0), 5, (10, 10), 1.0)

        particle.update(0.5)

        assert particle.alpha == 127


class TestParticleSystem:
    def test_initialization(self):
        system = ParticleSystem()

        assert system.enabled is True
        assert system.particle_count == 20
        assert len(system.particles) == 0

    def test_emit_creates_particles(self):
        system = ParticleSystem()
        system.enabled = True
        system.emit(100, 100, (255, 0, 0), count=10)

        assert len(system.particles) == 10

    def test_emit_disabled(self):
        system = ParticleSystem()
        system.set_enabled(False)

        system.emit(100, 100, (255, 0, 0), count=10)

        assert len(system.particles) == 0

    def test_emit_merge(self):
        system = ParticleSystem()

        system.emit_merge(100, 100, 4)

        assert len(system.particles) == 30

    def test_emit_spawn(self):
        system = ParticleSystem()

        system.emit_spawn(100, 100)

        assert len(system.particles) == 15

    def test_emit_win(self):
        system = ParticleSystem()

        system.emit_win(100, 100)

        assert len(system.particles) == 60

    def test_emit_game_over(self):
        system = ParticleSystem()

        system.emit_game_over(100, 100)

        assert len(system.particles) == 40

    def test_update(self):
        system = ParticleSystem()
        system.emit(100, 100, (255, 0, 0), count=10)

        system.update(0.1)

        assert len(system.particles) == 10

    def test_update_remove_dead(self):
        system = ParticleSystem()
        system.enabled = True
        system.particle_lifetime = 0.1
        system.emit(100, 100, (255, 0, 0), count=10)

        system.update(0.2)

        assert len(system.particles) == 0

    def test_clear(self):
        system = ParticleSystem()
        system.emit(100, 100, (255, 0, 0), count=10)

        system.clear()

        assert len(system.particles) == 0

    def test_set_enabled(self):
        system = ParticleSystem()

        system.set_enabled(False)

        assert system.enabled is False

    def test_get_particle_count(self):
        system = ParticleSystem()
        system.emit(100, 100, (255, 0, 0), count=10)

        count = system.get_particle_count()

        assert count == 10


class TestSound3D:
    def test_initialization(self):
        sound = Sound3D(100, 100, 0.5)

        assert sound.x == 100
        assert sound.y == 100
        assert sound.volume == 0.5

    def test_calculate_pan_center(self):
        sound = Sound3D(400, 300, 1.0)

        pan = sound.calculate_pan(400, 800)

        assert pan == 0.0

    def test_calculate_pan_left(self):
        sound = Sound3D(100, 300, 1.0)

        pan = sound.calculate_pan(400, 800)

        assert pan < 0

    def test_calculate_pan_right(self):
        sound = Sound3D(700, 300, 1.0)

        pan = sound.calculate_pan(400, 800)

        assert pan > 0

    def test_calculate_distance_volume_center(self):
        sound = Sound3D(400, 300, 1.0)

        volume = sound.calculate_distance_volume(400, 300, 800, 600)

        assert volume == 1.0

    def test_calculate_distance_volume_far(self):
        sound = Sound3D(0, 0, 1.0)

        volume = sound.calculate_distance_volume(400, 300, 800, 600)

        assert volume < 1.0


class TestAudioEngine:
    def test_initialization(self):
        from src.config import Config
        config = Config()
        config._config['audio']['volume'] = 0.7
        config._config['audio']['sfx_volume'] = 0.8
        
        engine = AudioEngine()

        assert engine.enabled is True
        assert engine.master_volume == 0.7
        assert engine.sfx_volume == 0.8

    def test_generate_tone(self):
        engine = AudioEngine()

        sound = engine.generate_tone(440, 0.1, 0.5)

        assert sound is not None

    def test_generate_merge_sound(self):
        engine = AudioEngine()

        sound = engine.generate_merge_sound(4)

        assert sound is not None

    def test_generate_move_sound(self):
        engine = AudioEngine()

        sound = engine.generate_move_sound()

        assert sound is not None

    def test_generate_spawn_sound(self):
        engine = AudioEngine()

        sound = engine.generate_spawn_sound()

        assert sound is not None

    def test_generate_win_sound(self):
        engine = AudioEngine()

        sound = engine.generate_win_sound()

        assert sound is not None

    def test_generate_game_over_sound(self):
        engine = AudioEngine()

        sound = engine.generate_game_over_sound()

        assert sound is not None

    def test_generate_ui_sound(self):
        engine = AudioEngine()

        sound = engine.generate_ui_sound('click')

        assert sound is not None

    def test_set_enabled(self):
        engine = AudioEngine()

        engine.set_enabled(False)

        assert engine.enabled is False

    def test_set_master_volume(self):
        engine = AudioEngine()

        engine.set_master_volume(0.5)

        assert engine.master_volume == 0.5

    def test_set_master_volume_clamp(self):
        engine = AudioEngine()

        engine.set_master_volume(1.5)

        assert engine.master_volume == 1.0

    def test_set_sfx_volume(self):
        engine = AudioEngine()

        engine.set_sfx_volume(0.5)

        assert engine.sfx_volume == 0.5

    def test_set_listener_position(self):
        engine = AudioEngine()

        engine.set_listener_position(500, 400)

        assert engine.listener_pos == (500, 400)

    def test_set_screen_size(self):
        engine = AudioEngine()

        engine.set_screen_size(1024, 768)

        assert engine.screen_size == (1024, 768)
