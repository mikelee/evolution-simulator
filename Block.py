class Block:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
    
    def draw(self, pygame, screen, coordinates):
        block_surf = pygame.Surface((self.width, self.height))
        block_surf.fill('#D15466')

        block_rect = block_surf.get_rect(topleft = coordinates)
        screen.blit(block_surf, block_rect)
        return block_rect