#!/usr/bin/env python3
"""Particle System for visual effects"""

import pygame
import random
import math
from typing import List, Tuple


class Particle:
    """Single particle entity"""

    def __init__(self, x: float, y: float, color: Tuple[int, int, int]):
        self.x = x
        self.y = y
        self.color = color
        
        # Random direction and speed
        angle = random.uniform(0, 2 * math.pi)
        speed = random.uniform(50, 200)
        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed
        
        # Lifetime
        self.lifetime = random.uniform(0.3, 1.0)
        self.age = 0
        self.size = random.uniform(2, 6)
        self.gravity = random.uniform(50, 150)

    def update(self, dt: float) -> bool:
        """Update particle position and return if still alive"""
        self.x += self.vx * dt
        self.y += self.vy * dt
        self.vy += self.gravity * dt
        self.age += dt
        
        # Apply air resistance
        self.vx *= 0.98
        self.vy *= 0.98
        
        return self.age < self.lifetime

    def draw(self, surface: pygame.Surface, camera_offset: Tuple[float, float] = (0, 0)):
        """Draw particle with alpha based on lifetime"""
        alpha = int(255 * (1 - self.age / self.lifetime))
        size = int(self.size * (1 - self.age / self.lifetime))
        
        if size > 0 and alpha > 0:
            color = (*self.color, alpha)
            
            # Create surface with alpha
            s = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
            pygame.draw.circle(s, color, (size, size), size)
            
            pos = (int(self.x - camera_offset[0]), int(self.y - camera_offset[1]))
            surface.blit(s, pos)


class ParticleSystem:
    """Manages particle effects"""

    def __init__(self):
        self.particles: List[Particle] = []
        self.particle_groups: List[List[Particle]] = []

    def create_explosion(self, x: float, y: float, color: Tuple[int, int, int], count: int = 20):
        """Create explosion particle effect"""
        for _ in range(count):
            self.particles.append(Particle(x, y, color))

    def create_celebration(self, x: float, y: float, count: int = 30):
        """Create celebration effect with multiple colors"""
        colors = [
            (255, 215, 0),  # Gold
            (255, 105, 180),  # Pink
            (138, 43, 226),  # Blue violet
            (50, 205, 50),   # Lime
            (255, 69, 0)     # Orange red
        ]
        for _ in range(count):
            color = random.choice(colors)
            self.particles.append(Particle(x, y, color))

    def create_tile_merge(self, x: float, y: float, value: int):
        """Create particle effect for tile merge"""
        # Get color based on tile value
        from src.engine.constants import TILE_VALUES
        tile_color = TILE_VALUES.get(value, ((200, 200, 200),))[0]
        color = tuple(int(c) for c in tile_color.lstrip('#')) if isinstance(tile_color, str) else tile_color
        
        if isinstance(color, str):
            color = (200, 200, 200)
        
        self.create_explosion(x, y, color, 15)

    def create_smoke(self, x: float, y: float, count: int = 10):
        """Create smoke effect"""
        for _ in range(count):
            gray = random.randint(100, 200)
            p = Particle(x, y, (gray, gray, gray))
            p.vy = random.uniform(-50, -100)
            p.gravity = -20
            self.particles.append(p)

    def update(self, dt: float):
        """Update all particles"""
        self.particles = [p for p in self.particles if p.update(dt)]

    def draw(self, surface: pygame.Surface, camera_offset: Tuple[float, float] = (0, 0)):
        """Draw all particles"""
        for particle in self.particles:
            particle.draw(surface, camera_offset)

    def clear(self):
        """Clear all particles"""
        self.particles.clear()

    def get_particle_count(self) -> int:
        """Get current particle count"""
        return len(self.particles)
