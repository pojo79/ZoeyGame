import pygame
import random

vec2 = pygame.math.Vector2

class ParticleSystem(object):

    def __init__(self, num_particles, origin, image = None):
        self.origin = origin
        self.particles = pygame.sprite.Group()
        self.image = image
        self.num_particles = num_particles
        self.create_particles()
        self.weight = 3

    def create_particles(self):
        for num in range(self.num_particles):
            self.particles.add(Particle(self.image, self.origin))
            

    def update_particles(self):
        for particle in self.particles:
            if particle.kill == True:
                self.particles.remove(particle)
            else:
                particle.update(self.weight)

    def draw_particles(self, surface):
        for particle in self.particles:
            surface.blit(particle.image, (particle.rect.x,particle.rect.y))
            

    def has_particles(self):
        if len(self.particles) > 0:
            return True
        else:
            return False
    
    def world_shift(self,xdiff):
        for particle in self.particles:
            particle.rect.x += xdiff

class Particle(pygame.sprite.Sprite):

    def __init__(self, image, origin):
        pygame.sprite.Sprite.__init__(self)
        self.born = pygame.time.get_ticks()
        self.lifespan = random.uniform(2, 800)
        self.image = image
        self.kill = False
        self.rect = self.image.get_rect()
        self.rect.move_ip(origin[0], origin[1])


    def update(self, weight):
        self.rect.x += random.uniform(-1.0, 1.2) * weight
        self.rect.y += random.uniform(-1.0, 1.2) * weight

        if self.lifespan <= pygame.time.get_ticks() - self.born:
            self.kill = True
