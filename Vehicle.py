import pygame
import random

max = 5  # 6x6 grid (0-5)
scaleBase = 120

def randomColor(oldImg):
    randColor = (random.randint(0, 255),
                    random.randint(0, 255),
                    random.randint(0, 255),
                    255)
    newImg = oldImg.copy()
    for x in range(newImg.get_width()):
        for y in range(newImg.get_height()):
            curColor = newImg.get_at((x, y))
            if curColor.a > 0:
                new_color = (randColor[0],
                            randColor[1],
                            randColor[2],
                            curColor.a)
                newImg.set_at((x, y), new_color)
    
    return newImg

class Vehicle:

    def __init__(self, kind, pos, dir, id=None):
        if type(kind) is str:
            self.kind = kind
            if self.kind == "c" or self.kind == "x":
                self.imgName = "./Asset/Vehicle/Car.png"
                self.len = 2
            elif self.kind == "t":
                self.imgName = "./Asset/Vehicle/Truck.png"
                self.len = 3
            else:
                raise Exception(kind, "is not allowed.")
        else:
            raise Exception(kind, "is not correct type.")
        self.img = pygame.image.load(self.imgName)
        # if self.kind != "x" : self.img = randomColor(self.img)
        self.img = pygame.transform.scale(self.img, (self.len * scaleBase, scaleBase))

        self.id = id

        if dir == "h" or dir == "v":
            self.dir = dir
            if dir == "v":
                self.img = pygame.transform.rotate(self.img, 90)
        else:
            raise Exception(dir, "is not allowed.")
        
        if type(pos) is list:
            if pos[0] < 0 or pos[1] < 0 or pos[0] > max or pos[1] > max:
                raise Exception("Position has to be >= (0, 0) and <= (5, 5)")
            else:
                self.pos = pos.copy()  # Store a copy to avoid reference issues