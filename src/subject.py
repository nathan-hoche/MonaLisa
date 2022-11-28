import random
from PIL import Image, ImageDraw
import numpy as np
import colour

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

    def drawPolygon(self, nbPolygon:int=-1, subdivise:int=8) -> None:
        if nbPolygon == -1:
            nbPolygon = random.randint(3, 6)
        region = (int(self.size[0] / subdivise), int(self.size[1] / subdivise))
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
