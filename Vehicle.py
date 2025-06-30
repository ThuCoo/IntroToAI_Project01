import pygame
from pygame.locals import *

max = 5 # 6x6 grid
scaleBase = 120

class Vehicle :
    def __init__(self, kind, pos, dir, id = None) : # ID will be set automatically by board.pushVehicles
        if type(kind) is str :
            self.kind = kind
            if self.kind == "c" or self.kind == "x" : # x : the car that needs to pass to win
                self.imgName = "./Asset/Car.png"
                self.len = 2
            elif self.kind == "t" :
                self.imgName = "./Asset/Truck.png"
                self.len = 3
            else :
                raise Exception(kind, "is not allowed.")
        else :
            raise Exception(kind, "is not correct type.")
        self.img = pygame.image.load(self.imgName)
        self.img = pygame.transform.scale(self.img, (self.len * scaleBase, scaleBase))

        self.id = id

        if dir == "h" or dir == "v" :
            self.dir = dir
            if (dir == "v") :
                self.img = pygame.transform.rotate(self.img, 90)
        else :
            raise Exception(dir, "is not allowed.")
        

        if type(pos) is list :
            if pos[0] < 0 or pos[1] < 0 or pos[0] > max or pos[1] > max :
                raise Exception("Position has to be >= (0, 0) and <= (5, 5)")
            else :
                self.pos = [pos[0], pos[1]]
        