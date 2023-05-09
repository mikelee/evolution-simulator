import itertools
import math
import random

class Creature:
    id_iter = itertools.count()

    def __init__(self, dna=None, location=None) -> None:
        if dna:
            self.dna = dna
        else:
            self.dna = self.getRanDNA()
        self.age = 0
        self.energy = self.dna['storage']
        self.id = next(Creature.id_iter)
        self.location = location

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

                currentRow, currentCol = self.location

                newRow = currentRow + rowChange
                newCol = currentCol + colChange
 
                self.move(environment, (newRow, newCol))
        else:
            # wander around for food
            pass

    def die(self, environment):
        # remove creature from board
        row, col = self.location
        environment.board.grid[row][col].remove(self)

        # remove creature from creatures list
        for i, creature in enumerate(environment.creatures):
            if self.id == creature.id:
                del environment.creatures[i]
        # There might still be another creature there that killed this creature
        if len(environment.board.grid[row][col]) == 0:
            environment.addEmptyBlock((row, col))

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
        currentRow, currentCol = self.location

        # remove creature from its current location in the environment
        environment.board.grid[currentRow][currentCol].remove(self)
        if len(environment.board.grid[currentRow][currentCol]) == 0:
            environment.addEmptyBlock((currentRow, currentCol))

        # add creature to enviroment at coordinates
        environment.board.grid[coordinates[0]][coordinates[1]].append(self)
        try:
            environment.removeEmptyBlock(coordinates)
        except:
            # the block the creature moved to was already occupied
            pass

        self.location = coordinates

    def replicateDNA(self, dna):
        mutationChance = .2

        newDNA = {}

        for attribute in dna:
            ran = random.random()

            if ran <= mutationChance:
                # mutation happens
                mutationSeverity = random.randint(1, 4)
                mutationDirection = 1 if random.random() < .5 else -1
            else:
                newDNA[attribute] = dna[attribute]
        return newDNA

    def reproduce(self, environment):
        emptyBlock = environment.getEmptyBlock()
        environment.removeEmptyBlock(emptyBlock)
        replicatedDNA = self.replicateDNA(self.dna)
        offspring = Creature(replicatedDNA, emptyBlock)
        environment.board.set(emptyBlock, offspring)
        environment.creatures.append(offspring)

    def scan(self, environment):
        # get current location of creature
        currentRow, currentCol = self.location

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


    def setLocation(self, coordinates):
        self.location = coordinates

    def update(self, environment):
        if self.age >= 10:
            self.reproduce(environment)

        stillYoung = self.increaseAge()
        hasEnergy = self.checkEnergy()

        if stillYoung and hasEnergy:
            self.decide(environment)
        else:
            self.die(environment)