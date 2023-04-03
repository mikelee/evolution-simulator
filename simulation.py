import pygame
from sys import exit
from Creature import Creature
from Environment import Environment

pygame.init();

font = pygame.font.SysFont(None, 24)

size = width, height = 1200, 800

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

creature1 = Creature()
creature2 = Creature()
creature3 = Creature()
creatures = [creature1, creature2, creature3]

environment = Environment(size, 5, 5, creatures)
environment.spawnFood()
environment.spawnFood()
environment.spawnFood()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

    environment.refresh(pygame, screen, font)
    pygame.display.update()
    clock.tick(.5)