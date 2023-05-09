class Stats:
    def __init__(self, size, creatures) -> None:
        self.size = size
        self.creatures = creatures

    def refresh(self, pygame, screen, font):
        self.draw(pygame, screen)

        for creature in self.creatures:
            self.draw_stats(creature)

    def draw(self, pygame, screen, font):
        # draw background
        stats_surf = pygame.Surface(self.size)
        stats_surf.fill('#4a4a4a')
        stats_rect = stats_surf.get_rect(topleft = (600, 0))
        screen.blit(stats_surf, stats_rect)

        headings = ('id', 'energy', 'lifespan', 'metabolism', 'movement', 'sight', 'storage', 'strength')
        ROW_HEIGHT = 50;
        COl_WIDTH = (self.size[0] / len(headings))

        # draw headings
        x = 600
        y = 0

        for heading in headings:
            box = pygame.Surface((COl_WIDTH, ROW_HEIGHT))
            box_rect = box.get_rect(topleft = (x, y))

            text = font.render(heading, True, '#EEEEEE')
            text_rect = text.get_rect()
            text_rect.center = box_rect.center

            screen.blit(text, text_rect)

            x += COl_WIDTH
        
        # draw creatures' stats
        for creature in self.creatures:
            x = 600
            y += ROW_HEIGHT

            for heading in headings:
                if heading == 'id':
                    text = font.render(str(creature.id), True, '#EEEEEE')
                elif heading == 'energy':
                    text = font.render(str(creature.energy), True, '#EEEEEE')
                else:
                    text = font.render(str(creature.dna[heading]), True, '#EEEEEE')

                box = pygame.Surface((COl_WIDTH, ROW_HEIGHT))
                box_rect = box.get_rect(topleft = (x, y))

                text_rect = text.get_rect()
                text_rect.center = box_rect.center

                screen.blit(text, text_rect)

                x += COl_WIDTH