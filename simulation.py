import pygame
from sys import exit

pygame.init();

font = pygame.font.SysFont(None, 24)

size = width, height = 1200, 800

screen = pygame.display.set_mode(size)
clock = pygame.time.Clock()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    
    pygame.display.update()
    clock.tick(.5)