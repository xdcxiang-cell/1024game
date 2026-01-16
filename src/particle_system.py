import pygame
import random
import math
from typing import List, Tuple, Optional
from src.config import Config


class Particle:
    def __init__(self, x: float, y: float, color: Tuple[int, int, int],
                 size: float, velocity: Tuple[float, float], lifetime: float):
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.velocity = velocity
        self.lifetime = lifetime
        self.max_lifetime = lifetime
        self.alpha = 255

    def update(self, dt: float) -> bool:
        self.x += self.velocity[0] * dt
        self.y += self.velocity[1] * dt
        self.lifetime -= dt
        self.alpha = int(255 * (self.lifetime / self.max_lifetime))
        return self.lifetime > 0

    def draw(self, surface: pygame.Surface):
        if self.lifetime > 0:
            s = pygame.Surface((int(self.size * 2), int(self.size * 2)), pygame.SRCALPHA)
            color_with_alpha = (*self.color, self.alpha)
            pygame.draw.circle(s, color_with_alpha, (int(self.size), int(self.size)), int(self.size))
            surface.blit(s, (int(self.x - self.size), int(self.y - self.size)))


class ParticleSystem:
    def __init__(self):
        self.particles: List[Particle] = []
        self.config = Config()
        self.enabled = self.config.get('particles', 'enabled', default=True)
        self.particle_count = self.config.get('particles', 'count', default=20)
        self.particle_lifetime = self.config.get('particles', 'lifetime', default=1.0)

    def emit(self, x: float, y: float, color: Tuple[int, int, int],
             count: Optional[int] = None, size_range: Tuple[float, float] = (2, 6),
             velocity_range: Tuple[float, float] = (50, 150)):
        if not self.enabled:
            return

        count = count or self.particle_count

        for _ in range(count):
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(*velocity_range)
            velocity = (math.cos(angle) * speed, math.sin(angle) * speed)
            size = random.uniform(*size_range)
            lifetime = self.particle_lifetime * random.uniform(0.8, 1.2)

            particle = Particle(x, y, color, size, velocity, lifetime)
            self.particles.append(particle)

    def emit_merge(self, x: float, y: float, tile_value: int):
        colors = {
            2: (238, 228, 218),
            4: (237, 224, 200),
            8: (242, 177, 121),
            16: (245, 149, 99),
            32: (246, 124, 95),
            64: (246, 94, 59),
            128: (237, 207, 114),
            256: (237, 204, 97),
            512: (237, 200, 80),
            1024: (237, 197, 63),
            2048: (237, 194, 46)
        }

        color = colors.get(tile_value, (255, 255, 255))
        self.emit(x, y, color, count=30, size_range=(3, 8), velocity_range=(100, 200))

    def emit_spawn(self, x: float, y: float):
        self.emit(x, y, (255, 255, 255), count=15, size_range=(2, 5), velocity_range=(50, 100))

    def emit_win(self, x: float, y: float):
        colors = [(255, 215, 0), (255, 165, 0), (255, 69, 0), (255, 255, 0)]
        for _ in range(3):
            color = random.choice(colors)
            self.emit(x, y, color, count=20, size_range=(4, 10), velocity_range=(150, 250))

    def emit_game_over(self, x: float, y: float):
        self.emit(x, y, (128, 128, 128), count=40, size_range=(3, 7), velocity_range=(80, 150))

    def update(self, dt: float):
        self.particles = [p for p in self.particles if p.update(dt)]

    def draw(self, surface: pygame.Surface):
        for particle in self.particles:
            particle.draw(surface)

    def clear(self):
        self.particles.clear()

    def set_enabled(self, enabled: bool):
        self.enabled = enabled

    def get_particle_count(self) -> int:
        return len(self.particles)
