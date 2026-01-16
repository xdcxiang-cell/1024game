"""
1024 Game - Particle System Tests
Comprehensive tests for the particle effect system
"""

import unittest
import os
import sys
import pygame
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.particle_system import ParticleSystem, Particle, ParticleEmitter, ExplosionEmitter, TrailEmitter, TextEmitter


class TestParticleSystem(unittest.TestCase):
    """Test cases for the Particle System"""

    def setUp(self):
        """Set up pygame for testing"""
        pygame.init()
        self.screen = pygame.display.set_mode((800, 600))
        self.particle_system = ParticleSystem(self.screen)

    def tearDown(self):
        """Clean up"""
        pygame.quit()

    def test_particle_creation(self):
        """Test particle creation"""
        particle = Particle(
            x=100, y=100,
            vx=1.0, vy=-1.0,
            life=1.0,
            color=(255, 255, 0),
            size=5,
            decay_rate=0.1
        )

        self.assertEqual(particle.x, 100)
        self.assertEqual(particle.y, 100)
        self.assertEqual(particle.life, 1.0)
        self.assertEqual(particle.color, (255, 255, 0))
        self.assertEqual(particle.size, 5)

    def test_particle_update(self):
        """Test particle updating"""
        particle = Particle(
            x=100, y=100,
            vx=10.0, vy=-10.0,
            life=1.0,
            color=(255, 255, 0),
            size=5,
            decay_rate=0.1
        )

        particle.update(0.1)

        self.assertEqual(particle.x, 101.0)
        self.assertEqual(particle.y, 99.0)
        self.assertEqual(particle.life, 0.99)

    def test_particle_death(self):
        """Test particle death"""
        particle = Particle(
            x=100, y=100,
            vx=0, vy=0,
            life=0.1,
            color=(255, 255, 0),
            size=5,
            decay_rate=1.0
        )

        particle.update(0.2)
        self.assertTrue(particle.life <= 0)

    def test_particle_emitter_creation(self):
        """Test emitter creation"""
        emitter = ParticleEmitter(
            x=400, y=300,
            particle_count=10,
            color=(255, 0, 0),
            particle_life=1.0
        )

        self.assertEqual(emitter.x, 400)
        self.assertEqual(emitter.y, 300)
        self.assertEqual(emitter.particle_count, 10)

    def test_explosion_emitter(self):
        """Test explosion emitter"""
        emitter = ExplosionEmitter(
            x=400, y=300,
            particle_count=50,
            color=(255, 100, 0),
            explosion_force=200
        )

        particles = emitter.emit()
        self.assertEqual(len(particles), 50)

        # Check particles have different velocities
        velocities = [(p.vx, p.vy) for p in particles]
        self.assertGreater(len(set(velocities)), 1)

    def test_trail_emitter(self):
        """Test trail emitter"""
        emitter = TrailEmitter(
            x=400, y=300,
            particle_count=20,
            color=(0, 255, 255),
            direction=(1.0, 0.0),
            spread=0.5
        )

        particles = emitter.emit()
        self.assertEqual(len(particles), 20)

    def test_text_emitter(self):
        """Test text emitter"""
        emitter = TextEmitter(
            x=400, y=300,
            text="+100",
            color=(0, 255, 0),
            font_size=24
        )

        particles = emitter.emit()
        self.assertGreater(len(particles), 0)

    def test_particle_system_add_emitter(self):
        """Test adding emitters to particle system"""
        emitter = ExplosionEmitter(
            x=400, y=300,
            particle_count=50,
            color=(255, 0, 0)
        )

        self.particle_system.add_emitter(emitter)
        self.assertEqual(len(self.particle_system.emitters), 1)

    def test_particle_system_update(self):
        """Test particle system updating"""
        emitter = ExplosionEmitter(
            x=400, y=300,
            particle_count=50,
            color=(255, 0, 0)
        )

        self.particle_system.add_emitter(emitter)
        self.particle_system.update(0.1)

        self.assertGreater(len(self.particle_system.particles), 0)

    def test_particle_system_render(self):
        """Test particle system rendering"""
        emitter = ExplosionEmitter(
            x=400, y=300,
            particle_count=50,
            color=(255, 0, 0)
        )

        self.particle_system.add_emitter(emitter)
        self.particle_system.update(0.1)
        self.particle_system.render()

    def test_particle_system_clear(self):
        """Test clearing particle system"""
        emitter = ExplosionEmitter(
            x=400, y=300,
            particle_count=50,
            color=(255, 0, 0)
        )

        self.particle_system.add_emitter(emitter)
        self.particle_system.update(0.1)
        self.particle_system.clear()

        self.assertEqual(len(self.particle_system.particles), 0)
        self.assertEqual(len(self.particle_system.emitters), 0)

    def test_merge_effect(self):
        """Test merge effect"""
        self.particle_system.create_merge_effect(400, 300, 1024)
        self.assertEqual(len(self.particle_system.emitters), 1)

    def test_level_up_effect(self):
        """Test level up effect"""
        self.particle_system.create_level_up_effect(400, 300)
        self.assertEqual(len(self.particle_system.emitters), 1)

    def test_game_over_effect(self):
        """Test game over effect"""
        self.particle_system.create_game_over_effect(400, 300)
        self.assertEqual(len(self.particle_system.emitters), 1)

    def test_score_text_effect(self):
        """Test score text effect"""
        self.particle_system.create_score_text(400, 300, 100)
        self.assertEqual(len(self.particle_system.emitters), 1)

    def test_explosion_force(self):
        """Test explosion force parameter"""
        emitter_low = ExplosionEmitter(
            x=400, y=300,
            particle_count=10,
            color=(255, 0, 0),
            explosion_force=50
        )

        emitter_high = ExplosionEmitter(
            x=400, y=300,
            particle_count=10,
            color=(255, 0, 0),
            explosion_force=200
        )

        particles_low = emitter_low.emit()
        particles_high = emitter_high.emit()

        avg_speed_low = sum((p.vx**2 + p.vy**2)**0.5 for p in particles_low) / 10
        avg_speed_high = sum((p.vx**2 + p.vy**2)**0.5 for p in particles_high) / 10

        self.assertLess(avg_speed_low, avg_speed_high)

    def test_particle_color_variation(self):
        """Test particle color variations"""
        emitter = ExplosionEmitter(
            x=400, y=300,
            particle_count=5,
            color=(255, 100, 0)
        )

        particles = emitter.emit()
        colors = [p.color for p in particles]

        # Colors should vary slightly
        self.assertGreater(len(set(colors)), 1)

    def test_particle_system_performance(self):
        """Test particle system performance"""
        import time

        for _ in range(10):
            emitter = ExplosionEmitter(
                x=400, y=300,
                particle_count=100,
                color=(255, 0, 0)
            )
            self.particle_system.add_emitter(emitter)

        start = time.time()
        for _ in range(100):
            self.particle_system.update(0.016)
        end = time.time()

        # Should complete in reasonable time
        self.assertLess(end - start, 1.0)

    def test_particle_off_screen_removal(self):
        """Test particles are removed when off screen"""
        emitter = ParticleEmitter(
            x=1000, y=1000,  # Off screen
            particle_count=10,
            color=(255, 255, 255),
            particle_life=1.0
        )

        self.particle_system.add_emitter(emitter)
        self.particle_system.update(0.1)

        self.particle_system.update(0.1)

        # Particles should be removed
        self.assertEqual(len(self.particle_system.particles), 0)


if __name__ == '__main__':
    unittest.main()
