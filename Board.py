from Vehicle import *
from State import State

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

        if vehicle.dir == "h":  # Horizontal
            if (vehicle.pos[0] < 0 or vehicle.pos[1] < 0 or 
                vehicle.pos[1] >= self.row or 
                vehicle.pos[0] + vehicle.len > self.col):
                return False
                
            for i in range(vehicle.pos[0], vehicle.pos[0] + vehicle.len):
                if self.grid[vehicle.pos[1]][i] != 0:
                    return False
                    
            self.vehicles[vehicle.id] = vehicle
            for i in range(vehicle.pos[0], vehicle.pos[0] + vehicle.len):
                self.grid[vehicle.pos[1]][i] = vehicle.id
            return True
             
        elif vehicle.dir == "v":  # Vertical
            if (vehicle.pos[0] < 0 or vehicle.pos[1] < 0 or 
                vehicle.pos[0] >= self.col or 
                vehicle.pos[1] + vehicle.len > self.row):
                return False
                
            for i in range(vehicle.pos[1], vehicle.pos[1] + vehicle.len):
                if self.grid[i][vehicle.pos[0]] != 0:
                    return False
                    
            self.vehicles[vehicle.id] = vehicle
            for i in range(vehicle.pos[1], vehicle.pos[1] + vehicle.len):
                self.grid[i][vehicle.pos[0]] = vehicle.id
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

    def move(self, vehicle_id, direction):
        if vehicle_id not in self.vehicles:
            return False

        veh = self.vehicles[vehicle_id]
        cur = veh.pos.copy()

        if veh.kind == "x" and veh.pos[0] == 4:
            self.vehicles[veh.id].pos = [6, 2]
            return True

        if veh.dir == "h":
            new_col = veh.pos[0] + direction
            if new_col < 0 or new_col + veh.len > self.col:
                return False
            
            # Clear old position
            for i in range(veh.pos[0], veh.pos[0] + veh.len):
                self.grid[veh.pos[1]][i] = 0
            
            # Check new position
            for i in range(new_col, new_col + veh.len):
                if self.grid[veh.pos[1]][i] != 0:
                    # Restore original position
                    for i in range(veh.pos[0], veh.pos[0] + veh.len):
                        self.grid[veh.pos[1]][i] = veh.id
                    return False
            
            # Update position
            veh.pos[0] = new_col
            for i in range(new_col, new_col + veh.len):
                self.grid[veh.pos[1]][i] = veh.id
            return True
                
        elif veh.dir == "v":
            new_row = veh.pos[1] + direction
            if new_row < 0 or new_row + veh.len > self.row:
                return False
            
            for i in range(veh.pos[1], veh.pos[1] + veh.len):
                self.grid[i][veh.pos[0]] = 0
            
            for i in range(new_row, new_row + veh.len):
                if self.grid[i][veh.pos[0]] != 0:
                    for i in range(veh.pos[1], veh.pos[1] + veh.len):
                        self.grid[i][veh.pos[0]] = veh.id
                    return False
            
            veh.pos[1] = new_row
            for i in range(new_row, new_row + veh.len):
                self.grid[i][veh.pos[0]] = veh.id
            return True

    def is_goal(self, state):
        for vid, vehicle in state.vehicles.items():
            if vehicle.kind == 'x':
                if vehicle.dir == 'h' and \
                   vehicle.pos[1] == 2 and \
                   vehicle.pos[0] + vehicle.len == self.col:
                    return True
        return False

    def get_valid_moves(self, state):
        valid_moves = []
        for vid, vehicle in state.vehicles.items():
            if vehicle.dir == "h":
                # Check move left (direction -1)
                new_col = vehicle.pos[0] - 1
                if new_col >= 0 and self._can_move(vid, -1, state.vehicles):
                    valid_moves.append((vid, -1))
                
                # Check move right (direction +1)
                new_col = vehicle.pos[0] + 1
                if new_col + vehicle.len <= self.col and self._can_move(vid, 1, state.vehicles):
                    valid_moves.append((vid, 1))
            else:
                # Check move up (direction -1)
                new_row = vehicle.pos[1] - 1
                if new_row >= 0 and self._can_move(vid, -1, state.vehicles):
                    valid_moves.append((vid, -1))
                
                # Check move down (direction +1)
                new_row = vehicle.pos[1] + 1
                if new_row + vehicle.len <= self.row and self._can_move(vid, 1, state.vehicles):
                    valid_moves.append((vid, 1))
        return valid_moves

    def _can_move(self, vehicle_id, step, vehicles):
        vehicle = vehicles[vehicle_id]
        if vehicle.dir == "h":
            if step < 0:  # Moving left
                check_col = vehicle.pos[0] + step
                if check_col < 0:
                    return False
                # Check for collision
                for vid, v in vehicles.items():
                    if vid == vehicle_id:
                        continue
                    if v.dir == "h" and v.pos[1] == vehicle.pos[1]:
                        if check_col >= v.pos[0] and check_col < v.pos[0] + v.len:
                            return False
                    elif v.dir == "v" and v.pos[0] == check_col:
                        if vehicle.pos[1] >= v.pos[1] and vehicle.pos[1] < v.pos[1] + v.len:
                            return False
                return True
            else:  # Moving right
                check_col = vehicle.pos[0] + vehicle.len - 1 + step
                if check_col >= self.col:
                    return False
                for vid, v in vehicles.items():
                    if vid == vehicle_id:
                        continue
                    if v.dir == "h" and v.pos[1] == vehicle.pos[1]:
                        if check_col >= v.pos[0] and check_col < v.pos[0] + v.len:
                            return False
                    elif v.dir == "v" and v.pos[0] == check_col:
                        if vehicle.pos[1] >= v.pos[1] and vehicle.pos[1] < v.pos[1] + v.len:
                            return False
                return True
        else:
            if step < 0:  # Moving up
                check_row = vehicle.pos[1] + step
                if check_row < 0:
                    return False
                for vid, v in vehicles.items():
                    if vid == vehicle_id:
                        continue
                    if v.dir == "v" and v.pos[0] == vehicle.pos[0]:
                        if check_row >= v.pos[1] and check_row < v.pos[1] + v.len:
                            return False
                    elif v.dir == "h" and v.pos[1] == check_row:
                        if vehicle.pos[0] >= v.pos[0] and vehicle.pos[0] < v.pos[0] + v.len:
                            return False
                return True
            else:  # Moving down
                check_row = vehicle.pos[1] + vehicle.len - 1 + step
                if check_row >= self.row:
                    return False
                for vid, v in vehicles.items():
                    if vid == vehicle_id:
                        continue
                    if v.dir == "v" and v.pos[0] == vehicle.pos[0]:
                        if check_row >= v.pos[1] and check_row < v.pos[1] + v.len:
                            return False
                    elif v.dir == "h" and v.pos[1] == check_row:
                        if vehicle.pos[0] >= v.pos[0] and vehicle.pos[0] < v.pos[0] + v.len:
                            return False
                return True

    def apply_move(self, state, move):
        vehicle_id, step = move
        new_vehicles = {}
        for vid, vehicle in state.vehicles.items():
            if vid == vehicle_id:
                if vehicle.dir == "h":
                    new_pos = [vehicle.pos[0] + step, vehicle.pos[1]]
                else:
                    new_pos = [vehicle.pos[0], vehicle.pos[1] + step]
                new_vehicle = Vehicle(vehicle.kind, new_pos, vehicle.dir, vid)
                new_vehicle.len = vehicle.len
                new_vehicles[vid] = new_vehicle
            else:
                new_vehicles[vid] = Vehicle(vehicle.kind, vehicle.pos.copy(), vehicle.dir, vid)
                new_vehicles[vid].len = vehicle.len
        
        new_moves = state.moves + [move]
        new_cost = state.cost + 1
        return State(new_vehicles, new_moves, new_cost)

    def heuristic(self, state):
        distance = 0
        blocking_vehicles = 0
        for vid, vehicle in state.vehicles.items():
            if vehicle.kind == 'x':
                distance = self.col - (vehicle.pos[0] + vehicle.len)
                for other_vid, other_v in state.vehicles.items():
                    if other_vid != vid and vehicle.pos[1] == other_v.pos[1]:
                        if other_v.pos[0] > vehicle.pos[0] + vehicle.len - 1:
                            blocking_vehicles += 1
        return distance + blocking_vehicles # Distance to exit + Count vehicles blocking the path in the same row