import os
import random
import re
import sys

import numpy as np
from PIL import Image

from monalisa.subject import subject


class generation:
    def __init__(self, image):
        self.image = Image.open(image)
        self.size = self.image.size
        self.imgArray = np.array(self.image)
        self.nbSubject = 0
        self.population = []
        self.stuck = 1
        self.lastFitness = 0

    def create_population(self, nbSubject: int, load: Image = None) -> None:
        self.nbSubject = nbSubject
        if load != None:
            for _ in range(nbSubject - 1):
                img = Image.open(load)
                self.population.append(subject(self.size, self.image.mode, img))
            for x in self.population:
                x.drawPolygon(1, subdivise=1)
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

    def crossover(self, parent: subject) -> None:
        res = [parent]
        for s in self.population:
            if s != parent:
                crossover = random.randint(0, self.size[0])
                # Children 1
                image = Image.new(self.image.mode, self.size, (0, 0, 0))
                image.paste(
                    parent.getImage().crop((0, 0, crossover, self.size[1])), (0, 0)
                )
                image.paste(
                    s.getImage().crop((crossover, 0, self.size[0], self.size[1])),
                    (crossover, 0),
                )
                res.append(subject(self.size, self.image.mode, image))
                # Children 2
                image = Image.new(self.image.mode, self.size, (0, 0, 0))
                image.paste(s.getImage().crop((0, 0, crossover, self.size[1])), (0, 0))
                image.paste(
                    parent.getImage().crop((crossover, 0, self.size[0], self.size[1])),
                    (crossover, 0),
                )
                res.append(subject(self.size, self.image.mode, image))

        self.population = res

    def mutation(self) -> None:
        isParent = True
        for subject in self.population:
            if isParent:
                isParent = False
            else:
                subject.drawPolygon(1, subdivise=self.stuck)

    def save(self, parent: subject, x: int, nbGeneration: int) -> None:
        if x + 1 == nbGeneration:
            parent.getImage().save("res.png")
            exit(0)
        elif x % 5 == 0:
            parent.getImage().save(f"step/generation{x:05d}.png")

    def equilibrate(self, fitness: float) -> None:
        print("Fitness:", fitness, end="\t")
        if self.lastFitness == fitness and self.stuck < 200:
            self.stuck += 1
        else:
            self.lastFitness = fitness
            self.stuck -= 1
            if self.stuck < 1:
                self.stuck = 1
        print("Stuck:", self.stuck)

    def main(self, nbGeneration: int, start=0) -> None:
        print("Starting Generation")
        nbGeneration += start
        for x in range(start, nbGeneration):
            print("Generation: " + str(x + 1) + "/" + str(nbGeneration), end="\t")
            sortedPopulation = self.fitness()
            self.equilibrate(sortedPopulation[0].getFitness())
            self.save(sortedPopulation[0], x, nbGeneration)
            self.population = sortedPopulation[: self.nbSubject]
            self.crossover(sortedPopulation[0])
            self.mutation()


def get_previous_number():
    files = os.listdir("step")

    def extract_number(f):
        s = re.findall(r"\d+", f)
        return (int(s[0]) if s else 0, f)

    last = max(files, key=extract_number)
    print(f"Last: {last}")
    return extract_number(last)[0]


def main():
    args = sys.argv

    if len(args) == 4:
        gen = generation(args[1])
        gen.create_population(int(args[2]))
        gen.main(int(args[3]))
    elif len(args) == 5:
        gen = generation(args[1])
        gen.create_population(int(args[2]), args[4])
        gen.main(int(args[3]), start=get_previous_number())
    else:
        print("Usage: python mona.py [image] [nbSubject] [nbGeneration]")
        print("\tExample: python mona.py image.png 100 500\n")
        print("In case you want to load a previous generation:")
        print("Usage: python mona.py [image] [nbSubject] [nbGeneration] [load]")
        print("\tExample: python mona.py image.png 100 500 load.png")


if __name__ == "__main__":
    main()
