"""
1024 Game - Particle System
Handles particle effects and animations
"""

import pygame
import math
import random
from typing import List, Tuple, Optional
from dataclasses import dataclass
from abc import ABC, abstractmethod


@dataclass
class Particle:
    x: float
    y: float
    vx: float
    vy: float
    life: float
    max_life: float
    color: Tuple[int, int, int]
    size: float
    alpha: float = 255


class ParticleSystem:
    """Manages particle effects"""
    
    def __init__(self):
        self.particles: List[Particle] = []
        self.emitters: List['ParticleEmitter'] = []
        self.surface_cache: dict = {}
        
    def update(self, delta_time: float) -> None:
        """Update all particles"""
        # Update emitters
        for emitter in self.emitters:
            emitter.update(delta_time)
            self.particles.extend(emitter.emit())
        
        # Update particles
        new_particles = []
        for p in self.particles:
            p.x += p.vx * delta_time
            p.y += p.vy * delta_time
            p.vy += 500 * delta_time  # gravity
            p.life -= delta_time
            p.alpha = int(255 * (p.life / p.max_life))
            
            if p.life > 0:
                new_particles.append(p)
        
        self.particles = new_particles
    
    def render(self, surface: pygame.Surface, offset_x: float = 0, offset_y: float = 0) -> None:
        """Render all particles"""
        for p in self.particles:
            if p.alpha <= 0:
                continue
                
            size = int(p.size * (p.life / p.max_life))
            if size < 1:
                continue
                
            color = (*p.color[:3], p.alpha)
            
            # Create surface with alpha
            cache_key = (size, color)
            if cache_key not in self.surface_cache:
                s = pygame.Surface((size * 2, size * 2), pygame.SRCALPHA)
                pygame.draw.circle(s, color, (size, size), size)
                self.surface_cache[cache_key] = s
            
            particle_surface = self.surface_cache[cache_key]
            x = int(p.x + offset_x - particle_surface.get_width() // 2)
            y = int(p.y + offset_y - particle_surface.get_height() // 2)
            surface.blit(particle_surface, (x, y))
    
    def add_emitter(self, emitter: 'ParticleEmitter') -> None:
        """Add a particle emitter"""
        self.emitters.append(emitter)
    
    def remove_emitter(self, emitter: 'ParticleEmitter') -> None:
        """Remove a particle emitter"""
        if emitter in self.emitters:
            self.emitters.remove(emitter)
    
    def create_merge_effect(self, x: float, y: float, value: int) -> None:
        """Create particle effect for merge"""
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
            2048: (237, 194, 46),
        }
        
        color = colors.get(value, (255, 255, 255))
        
        # Add explosion emitter
        emitter = ExplosionEmitter(x, y, color)
        self.add_emitter(emitter)
        
        # Add text effect
        self.add_emitter(TextEmitter(x, y, str(value), color))
    
    def create_move_effect(self, x: float, y: float) -> None:
        """Create particle effect for move"""
        emitter = TrailEmitter(x, y)
        self.add_emitter(emitter)
    
    def clear(self) -> None:
        """Clear all particles"""
        self.particles.clear()
        self.emitters.clear()
    
    def get_active_particle_count(self) -> int:
        """Get number of active particles"""
        return len(self.particles) + sum(len(e.particles) for e in self.emitters)


class ParticleEmitter(ABC):
    """Base class for particle emitters"""
    
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y
        self.active = True
        self.particles: List[Particle] = []
    
    @abstractmethod
    def update(self, delta_time: float) -> None:
        """Update emitter"""
        pass
    
    @abstractmethod
    def emit(self) -> List[Particle]:
        """Emit particles"""
        pass
    
    def is_active(self) -> bool:
        return self.active


class ExplosionEmitter(ParticleEmitter):
    """Emits particles in explosion pattern"""
    
    def __init__(self, x: float, y: float, color: Tuple[int, int, int], 
                 particle_count: int = 20, speed: float = 150):
        super().__init__(x, y)
        self.color = color
        self.particle_count = particle_count
        self.speed = speed
        self.emitted = False
    
    def update(self, delta_time: float) -> None:
        if not self.emitted:
            for _ in range(self.particle_count):
                angle = random.uniform(0, 2 * math.pi)
                speed = random.uniform(self.speed * 0.5, self.speed)
                vx = math.cos(angle) * speed
                vy = math.sin(angle) * speed
                
                p = Particle(
                    x=self.x,
                    y=self.y,
                    vx=vx,
                    vy=vy,
                    life=random.uniform(0.5, 1.0),
                    max_life=1.0,
                    color=self.color,
                    size=random.uniform(3, 6)
                )
                self.particles.append(p)
            self.emitted = True
        
        if not self.particles:
            self.active = False
    
    def emit(self) -> List[Particle]:
        particles = self.particles.copy()
        self.particles.clear()
        return particles


class TrailEmitter(ParticleEmitter):
    """Emits trail particles"""
    
    def __init__(self, x: float, y: float, particle_count: int = 5):
        super().__init__(x, y)
        self.particle_count = particle_count
        self.lifetime = 0.3
        self.spawn_timer = 0
    
    def update(self, delta_time: float) -> None:
        self.spawn_timer -= delta_time
        if self.spawn_timer <= 0:
            for _ in range(2):
                p = Particle(
                    x=self.x + random.uniform(-10, 10),
                    y=self.y + random.uniform(-10, 10),
                    vx=random.uniform(-50, 50),
                    vy=random.uniform(-50, 50),
                    life=self.lifetime,
                    max_life=self.lifetime,
                    color=(200, 200, 200),
                    size=2
                )
                self.particles.append(p)
            self.spawn_timer = 0.05
        
        self.lifetime -= delta_time
        if self.lifetime <= 0:
            self.active = False
    
    def emit(self) -> List[Particle]:
        particles = self.particles.copy()
        self.particles.clear()
        return particles


class TextEmitter(ParticleEmitter):
    """Emits text particles"""
    
    def __init__(self, x: float, y: float, text: str, color: Tuple[int, int, int]):
        super().__init__(x, y)
        self.text = text
        self.color = color
        self.emitted = False
    
    def update(self, delta_time: float) -> None:
        if not self.emitted:
            # Create text surface
            font = pygame.font.Font(None, 48)
            text_surface = font.render(self.text, True, self.color)
            
            # Extract pixels as particles
            for px in range(text_surface.get_width()):
                for py in range(text_surface.get_height()):
                    alpha = text_surface.get_at((px, py))[3]
                    if alpha > 0:
                        p = Particle(
                            x=self.x + px - text_surface.get_width() / 2,
                            y=self.y + py - text_surface.get_height() / 2,
                            vx=random.uniform(-50, 50),
                            vy=random.uniform(-100, -50),
                            life=1.0,
                            max_life=1.0,
                            color=self.color,
                            size=1
                        )
                        self.particles.append(p)
            self.emitted = True
        
        if not self.particles:
            self.active = False
    
    def emit(self) -> List[Particle]:
        particles = self.particles.copy()
        self.particles.clear()
        return particles


class ContinuousEmitter(ParticleEmitter):
    """Emits particles continuously"""
    
    def __init__(self, x: float, y: float, color: Tuple[int, int, int], 
                 rate: float = 10, duration: Optional[float] = None):
        super().__init__(x, y)
        self.color = color
        self.rate = rate
        self.duration = duration
        self.time_left = duration
        self.spawn_timer = 0
    
    def update(self, delta_time: float) -> None:
        if self.duration is not None:
            self.time_left -= delta_time
            if self.time_left <= 0:
                self.active = False
                return
        
        self.spawn_timer += delta_time
        spawn_interval = 1.0 / self.rate
        
        while self.spawn_timer >= spawn_interval:
            self.spawn_timer -= spawn_interval
            
            p = Particle(
                x=self.x,
                y=self.y,
                vx=random.uniform(-100, 100),
                vy=random.uniform(-100, 100),
                life=random.uniform(0.5, 1.5),
                max_life=1.5,
                color=self.color,
                size=random.uniform(2, 4)
            )
            self.particles.append(p)
    
    def emit(self) -> List[Particle]:
        particles = self.particles.copy()
        self.particles.clear()
        return particles