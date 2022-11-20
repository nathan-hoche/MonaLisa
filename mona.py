from PIL import Image, ImageDraw
import random
import numpy as np
import colour
import sys

def getRandomColor() -> None:
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

class subject():
    def __init__(self, size:tuple[int, int], type:str, image:Image=None) -> None:
        self.type = type
        self.image = image if image != None else Image.new(type, size, getRandomColor())
        self.draw = ImageDraw.Draw(self.image)
        self.imgArray = [] if image == None else np.array(self.image)
        self.size = size
        self.fitness = -1
    
    def getImage(self) -> Image:
        return self.image

    def drawPolygon(self, nbPolygon:int=-1) -> None:
        if nbPolygon == -1:
            nbPolygon = random.randint(3, 6)
        region = (int(self.size[0] / 8), int(self.size[1] / 8))
        for _ in range(nbPolygon):
            nbPoints = random.randint(3, 6)
            pos = (random.randint(0, self.size[0]), random.randint(0, self.size[1]))
            point = []
            for _ in range(nbPoints):
                point.append((random.randint(pos[0] - region[0], pos[0] + region[0]),
                           random.randint(pos[1] - region[1], pos[1] + region[1])))
            self.draw.polygon(point, fill=getRandomColor())
            self.imgArray = np.array(self.image)

    def getFitness(self, targetImage=None) -> float:
        if (self.fitness == -1):
            self.fitness = np.mean(colour.delta_E(self.imgArray, targetImage, method='CIE1976'))
        return self.fitness

class generation:
    def __init__(self, image):
        self.image = Image.open(image)
        self.size = self.image.size
        self.imgArray = np.array(self.image)
        self.nbSubject = 0
        self.population = []
    
    def create_population(self, nbSubject:int, load:Image=None) -> None:
        self.nbSubject = nbSubject
        if load != None:
            for _ in range(nbSubject -1):
                img = Image.open(load)
                self.population.append(subject(self.size, self.image.mode, img))
            for x in self.population:
                x.drawPolygon(1)
            # ADD Parent without mutation
            img = Image.open(load)
            self.population.append(subject(self.size, self.image.mode, img))
        else:
            for _ in range(nbSubject):
                self.population.append(subject(self.size, self.image.mode))
            for x in self.population:
                x.drawPolygon()
        print("Population create with", nbSubject, "subject.")

    def fitness(self) -> list[subject]:
        return sorted(self.population, key=lambda x: x.getFitness(self.imgArray))
    
    def crossover(self, parent:subject) -> None:
        res = [parent]
        for s in self.population:
            if s != parent:
                crossover = random.randint(0, self.size[0])
                # Children 1
                image = Image.new(self.image.mode, self.size, (0, 0, 0))
                image.paste(parent.getImage().crop((0, 0, crossover, self.size[1])), (0, 0))
                image.paste(s.getImage().crop((crossover, 0, self.size[0], self.size[1])), (crossover, 0))
                res.append(subject(self.size, self.image.mode, image))
                # Children 2
                image = Image.new(self.image.mode, self.size, (0, 0, 0))
                image.paste(s.getImage().crop((0, 0, crossover, self.size[1])), (0, 0))
                image.paste(parent.getImage().crop((crossover, 0, self.size[0], self.size[1])), (crossover, 0))
                res.append(subject(self.size, self.image.mode, image))

        self.population = res
    
    def mutation(self) -> None:
        isParent = True
        for subject in self.population:
            if isParent:
                isParent = False
            else:
                subject.drawPolygon(1)

    def main(self, nbGeneration:int) -> None:
        print("Starting Generation")
        for x in range(nbGeneration):
            print("Generation: " + str(x + 1) + '/' + str(nbGeneration), end="\t")
            sortedPopulation = self.fitness()
                
            print("Fitness:", sortedPopulation[0].getFitness())
            if (x + 1 == nbGeneration):
                sortedPopulation[0].getImage().save("res.png")
                break
            elif (x % 5 == 0):
                sortedPopulation[0].getImage().save("step/generation"+ str(x) + ".png")
            self.population = sortedPopulation[:self.nbSubject]
            self.crossover(sortedPopulation[0])
            self.mutation()

args = sys.argv

if len(args) == 4:
    gen = generation(args[1])
    gen.create_population(int(args[2]))
    gen.main(int(args[3]))
elif len(args) == 5:
    gen = generation(args[1])
    gen.create_population(int(args[2]), args[4])
    gen.main(int(args[3]))
else:
    print("Usage: python mona.py [image] [nbSubject] [nbGeneration]")
    print("\tExample: python mona.py image.png 100 500\n")
    print("In case you want to load a previous generation:")
    print("Usage: python mona.py [image] [nbSubject] [nbGeneration] [load]")
    print("\tExample: python mona.py image.png 100 500 load.png")