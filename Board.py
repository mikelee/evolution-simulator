from Block import Block
from Creature import Creature

class Board:
    gap = 10
    
    def __init__(self, size, grid):
        self.size = size
        self.grid = grid
        self.width = len(grid[0])
        self.height = len(grid)
        self.block_width = (self.size[0] - (self.gap * (self.width + 1))) / self.width
        self.block_height = (self.size[1] - (self.gap * (self.height + 1))) / self.height

    def draw(self, pygame, screen, font):
        # this adds a gap along the outside border
        current_horizontal = self.gap
        current_vertical = self.gap

        for row in range(self.height):
            current_horizontal = self.gap

            for col in range(self.width):
                # create block
                block = Block(self.block_width, self.block_height)
                block_surf = block.draw(pygame)
                block_rect = block_surf.get_rect(topleft = (current_horizontal, current_vertical))
                screen.blit(block_surf, block_rect)

                # write the value of the grid cell on the block
                if len(self.grid[row][col]) > 0:
                    item = self.grid[row][col][0]
                    arr = []

                    for item in self.grid[row][col]:
                        if isinstance(item, Creature):
                            arr.append(str(item.id))
                        elif item == 'Food':
                            arr.append(item)
                    itemsString = ', '.join(arr)

                    if len(arr):
                        text = font.render(itemsString, True, '#EEEEEE')
                        text_rect = text.get_rect()
                        text_rect.center = block_rect.center
                        screen.blit(text, text_rect)

                # move pointer to the right for the next column
                current_horizontal += (self.block_width + self.gap)
            # move pointer down for the next row
            current_vertical += (self.block_height + self.gap)

    def set(self, coordinates, item):
        row, col = coordinates
        self.grid[row][col].append(item)