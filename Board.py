from Vehicle import *

mapPath = "./Asset/Map.txt"

class Board:
    def makeGrid(self, size):
        self.grid = []
        for _ in range(size):
            self.grid.append([0] * size)

    def clearGrid(self):
        for i in range(len(self.grid)):
            for j in range(len(self.grid[0])):
                self.grid[i][j] = 0

    def pushVehicle(self, vehicle):
        vehicle.id = self.counter
        self.counter += 1

        if vehicle.dir == "h":
            if (vehicle.pos[0] < 0 or vehicle.pos[1] < 0 or 
                vehicle.pos[0] > self.row - vehicle.len or 
                vehicle.pos[1] > self.col - 1):
                return False
                
            for i in range(vehicle.pos[0], vehicle.pos[0] + vehicle.len):
                if self.grid[i][vehicle.pos[1]] != 0:
                    return False
                    
            self.vehicles[vehicle.id] = vehicle
            for i in range(vehicle.pos[0], vehicle.pos[0] + vehicle.len):
                self.grid[i][vehicle.pos[1]] = vehicle.id
            return True
             
        elif vehicle.dir == "v":
            if (vehicle.pos[0] < 0 or vehicle.pos[1] < 0 or 
                vehicle.pos[0] > self.row - 1 or 
                vehicle.pos[1] > self.col - vehicle.len):
                return False
                
            for i in range(vehicle.pos[1], vehicle.pos[1] + vehicle.len):
                if self.grid[vehicle.pos[0]][i] != 0:
                    return False
                    
            self.vehicles[vehicle.id] = vehicle
            for i in range(vehicle.pos[1], vehicle.pos[1] + vehicle.len):
                self.grid[vehicle.pos[0]][i] = vehicle.id
            return True

    def stagePrep(self):
        self.clearGrid()
        self.vehicles = {}
        self.counter = 1
        cur = self.stage[self.level]
        for c in cur:
            self.pushVehicle(Vehicle(c[0], [c[1], c[2]], c[3]))

    def __init__(self, row=6, col=6):
        self.row = row
        self.col = col
        self.grid = []
        self.makeGrid(self.row)
        self.level = 0
        self.vehicles = {}
        self.stage = []
        self.counter = 1

        with open(mapPath, "r") as file:
            for line in file:
                vehs = line.strip().split()
                stage = []
                for veh in vehs:
                    block = []
                    for v in veh:
                        block.append(int(v) if v.isdigit() else v)
                    stage.append(block)
                self.stage.append(stage)

    def move(self, vehicle, val):
        if vehicle.id not in self.vehicles:
            return False

        veh = self.vehicles[vehicle.id]
        cur = veh.pos.copy()

        if veh.kind == "x" and veh.pos[0] == 4:
            self.vehicles[veh.id].pos = [6, 2]
            return True

        if veh.dir == "h":
            newCur = [veh.pos[0] + val, veh.pos[1]]
            
            if (newCur[0] < 0 or newCur[1] < 0 or 
                newCur[0] > self.row - veh.len or 
                newCur[1] > self.col - 1):
                return False
            
            for i in range(veh.pos[0], veh.pos[0] + veh.len):
                self.grid[i][veh.pos[1]] = 0
            
            for i in range(newCur[0], newCur[0] + veh.len):
                if self.grid[i][newCur[1]] != 0:
                    for i in range(cur[0], cur[0] + veh.len):
                        self.grid[i][cur[1]] = veh.id
                    return False
            
            veh.pos = newCur
            for i in range(newCur[0], newCur[0] + veh.len):
                self.grid[i][newCur[1]] = veh.id
            return True
                
        elif veh.dir == "v":
            newCur = [veh.pos[0], veh.pos[1] + val]
            
            if (newCur[0] < 0 or newCur[1] < 0 or 
                newCur[0] > self.row - 1 or 
                newCur[1] > self.col - veh.len):
                return False
            
            for i in range(veh.pos[1], veh.pos[1] + veh.len):
                self.grid[veh.pos[0]][i] = 0
            
            for i in range(newCur[1], newCur[1] + veh.len):
                if self.grid[newCur[0]][i] != 0:
                    for i in range(cur[1], cur[1] + veh.len):
                        self.grid[cur[0]][i] = veh.id
                    return False
            
            veh.pos = newCur
            for i in range(newCur[1], newCur[1] + veh.len):
                self.grid[newCur[0]][i] = veh.id
            return True