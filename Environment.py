import functools
import random
from Board import Board
from Creature import Creature

class Environment:
    def __init__(self, size, width, height, creatures) -> None:
        self.board = Board(size, [[[] for col in range(width)] for row in range(height)])
        self.conflicts = []
        self.creatures = creatures
        self.emptyBlocks = []
        self.size = size

        for i, row in enumerate(self.board.grid):
            for j, col in enumerate(row):
                # all blocks are initially empty
                self.emptyBlocks.append((i, j))
        self.spawnCreatures()
    
    def refresh(self, pygame, screen, font):
        for creature in self.creatures:
            creature.update(self)

        for i, row in enumerate(self.board.grid):
            for j, col in enumerate(row):
                if len(self.board.grid[i][j]) > 1:
                    conflict = {
                        'creatures': [],
                        'food': False,
                        'location': (i, j)
                    }

                    for item in self.board.grid[i][j]:
                        if isinstance(item, Creature):
                            conflict['creatures'].append(item)
                        elif item == 'Food':
                            conflict['food'] = True
                    self.conflicts.append(conflict)
        
        for conflict in self.conflicts:
            self.resolveConflict(conflict)
        self.conflicts.clear()

        self.board.draw(pygame, screen, font)

    def resolveConflict(self, conflict):
        if len(conflict['creatures']) > 1:
            def fight(creature1, creature2):
                if creature1.dna['strength'] > creature2.dna['strength']:
                    creature2.die(self)
                    return creature1
                elif creature2.dna['strength'] > creature1.dna['strength']:
                    creature1.die(self)
                    return creature2
                else:
                    ran = random.randint(1,2)
                    if ran == 1:
                        creature2.die(self)
                        return creature1
                    else:
                        creature1.die(self)
                        return creature2
                    
            survivor = functools.reduce(fight, conflict['creatures'])
        else:
            survivor = conflict['creatures'][0]

        if conflict['food']:
            for creature in self.creatures:
                if creature.id == survivor.id:
                    survivor.eat(10)
                    # remove food
                    row, col = conflict['location']
                    self.board.grid[row][col].remove('Food')

                    self.spawnFood()
    
    def getItemLocation(self, item):
        for i, row in enumerate(self.board.grid):
            for j, col in enumerate(row):
                try:
                    if self.board.grid[i][j].index(item) != -1:
                        return (i, j)
                except:
                    continue

    def getRanEmpty(self):
        ranCoordinates = random.choice(self.emptyBlocks)
        return ranCoordinates

    def spawnFood(self):
        coordinates = self.getRanEmpty()
        self.board.set(coordinates, 'Food')

        for index, item in enumerate(self.emptyBlocks):
            if item == coordinates:
                del self.emptyBlocks[index]
                
    def spawnCreatures(self):
        for creature in self.creatures:
            coordinates = self.getRanEmpty()
            self.board.set(coordinates, creature)

            for i, emptyBlock in enumerate(self.emptyBlocks):
                if emptyBlock == coordinates:
                    del self.emptyBlocks[i]