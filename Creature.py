import itertools
import math
import random

class Creature:
    id_iter = itertools.count()

    def __init__(self, dna=None) -> None:
        if dna:
            self.dna = dna
        else:
            self.dna = self.getRanDNA()
        self.age = 0
        self.energy = self.dna['storage']
        self.id = next(Creature.id_iter)

    def checkEnergy(self):
        if (self.energy <= 0):
            return False
        return True

    def decide(self, environment):
        interests = self.scan(environment)        

        if len(interests):
            target = interests[0]

            # move towards closest interest
            if target['totalDistance'] <= self.dna['movement']:
                self.move(environment, (target['location'][0], target['location'][1]))
            else:
                percentDistance = self.dna['movement'] / target['totalDistance']
                rowChange = math.ceil(target['rowDistance'] * percentDistance)
                colChange = self.dna['movement'] - abs(rowChange)
                if target['colDistance'] < 0:
                    colChange *= -1

                currentRow, currentCol = environment.getItemLocation(self)

                newRow = currentRow + rowChange
                newCol = currentCol + colChange
 
                self.move(environment, (newRow, newCol))
        else:
            # wander around for food
            pass

    def die(self, environment):
        # remove creature from board
        row, col = environment.getItemLocation(self)
        environment.board.grid[row][col].remove(self)

        # remove creature from creatures list
        for i, creature in enumerate(environment.creatures):
            if self.id == creature.id:
                del environment.creatures[i]

    def eat(self, foodEnergy):
        self.energy = min(self.energy + foodEnergy, self.dna['storage'])

    def getRanDNA(self):
        return {
            'lifespan': self.getRanInt(20),
            'metabolism': self.getRanInt(10),
            'movement': self.getRanInt(10),
            'sight': self.getRanInt(10),
            'storage': self.getRanInt(10),
            'strength': self.getRanInt(10)
        }

    def getRanInt(self, limit):
        return random.randint(4, limit)

    def increaseAge(self):
        self.age += 1

        if self.age > self.dna['lifespan']:
            return False
        return True

    def move(self, environment, coordinates):
        # get location
        currentRow, currentCol = environment.getItemLocation(self)

        # remove creature from its current location in the environment
        environment.board.grid[currentRow][currentCol].remove(self)

        # add creature to enviroment at coordinates
        environment.board.grid[coordinates[0]][coordinates[1]].append(self)

    def reproduce(self, environment):
        location = environment.getItemLocation(self)

        offspring = Creature(self.dna)
        environment.board.set(location, offspring)
        environment.creatures.append(offspring)

        nearEmpty = self.scanNear(environment, location)
        self.move(environment, nearEmpty)

    def scan(self, environment):
        # get current location of creature
        currentRow, currentCol = environment.getItemLocation(self)

        scanDistance = self.dna['sight']
        start = [currentRow - scanDistance, currentCol - scanDistance]
        end = [currentRow + scanDistance, currentCol + scanDistance]

        # keep start and end in bounds
        start[0] = max(start[0], 0)
        start[1] = max(start[1], 0)
        end[0] = min(end[0], len(environment.board.grid))
        end[1] = min(end[1], len(environment.board.grid[0]))

        interests = []

        for scanRow in range(start[0], end[0]):
            for scanCol in range(start[1], end[1]):
                if environment.board.grid[scanRow][scanCol].count('Food'):
                    rowDistance = scanRow - currentRow
                    colDistance = scanCol - currentCol
                    totalDistance = abs(rowDistance) + abs(colDistance)
                    interests.append({
                        'location': (scanRow, scanCol),
                        'rowDistance': rowDistance,
                        'colDistance': colDistance,
                        'totalDistance': totalDistance
                        })

        interests.sort(key=lambda interest : interest['totalDistance'])
        return interests

    def scanNear(self, environment, location):
        currentRow, currentCol = location

        scanDistance = 1
        start = [currentRow - scanDistance, currentCol - scanDistance]
        end = [currentRow + scanDistance, currentCol + scanDistance]

        # keep start and end in bounds
        start[0] = max(start[0], 0)
        start[1] = max(start[1], 0)
        end[0] = min(end[0], len(environment.board.grid))
        end[1] = min(end[1], len(environment.board.grid[0]))

        for scanRow in range(start[0], end[0]):
            for scanCol in range(start[1], end[1]):
                if len((scanRow, scanCol) is not location and environment.board.grid[scanRow][scanCol]) == 0:
                    return (scanRow, scanCol)

    def update(self, environment):
        if self.age >= 10:
            self.reproduce(environment)

        stillYoung = self.increaseAge()
        hasEnergy = self.checkEnergy()

        if stillYoung and hasEnergy:
            self.decide(environment)
        else:
            self.die(environment)