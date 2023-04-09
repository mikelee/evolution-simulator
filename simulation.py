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

play = True

while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                play = not play

        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    if play:
        environment.refresh(pygame, screen, font)
    else:
        environment.draw(pygame, screen, font)
        pause_surf = pygame.Surface(size)
        pause_rect = pause_surf.get_rect()
        pause_surf.fill('black')
        pause_surf.set_alpha(100)

        pause_text = font.render('Paused', True, '#EEEEEE')
        pause_text_rect = pause_text.get_rect()
        pause_text_rect.center = pause_rect.center
        
        screen.blit(pause_surf, (0, 0))
        screen.blit(pause_text, pause_text_rect)
    pygame.display.update()
    clock.tick(.5)