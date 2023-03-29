class Block:
    def __init__(self, width: int, height: int) -> None:
        self.width = width
        self.height = height
    
    def draw(self, pygame):
        block = pygame.Surface((self.width, self.height))
        block.fill('#D15466')
        return block