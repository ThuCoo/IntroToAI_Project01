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

        if vehicle.dir == "h":
            # Corrected boundary checks and placement
            if (vehicle.pos[0] < 0 or vehicle.pos[1] < 0 or 
                vehicle.pos[0] >= self.row or 
                vehicle.pos[1] + vehicle.len > self.col):
                return False
                
            for j in range(vehicle.pos[1], vehicle.pos[1] + vehicle.len):
                if self.grid[vehicle.pos[0]][j] != 0:
                    return False
                    
            self.vehicles[vehicle.id] = vehicle
            for j in range(vehicle.pos[1], vehicle.pos[1] + vehicle.len):
                self.grid[vehicle.pos[0]][j] = vehicle.id
            return True
             
        elif vehicle.dir == "v":
            # Corrected boundary checks and placement
            if (vehicle.pos[0] < 0 or vehicle.pos[1] < 0 or 
                vehicle.pos[0] + vehicle.len > self.row or 
                vehicle.pos[1] >= self.col):
                return False
                
            for i in range(vehicle.pos[0], vehicle.pos[0] + vehicle.len):
                if self.grid[i][vehicle.pos[1]] != 0:
                    return False
                    
            self.vehicles[vehicle.id] = vehicle
            for i in range(vehicle.pos[0], vehicle.pos[0] + vehicle.len):
                self.grid[i][vehicle.pos[1]] = vehicle.id
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

        # Special case: red car exiting
        if veh.kind == "x" and veh.dir == "h" and veh.pos[0] == 2 and veh.pos[1] + veh.len == 5:
            return True

        if veh.dir == "h":
            # Move columns
            new_col = veh.pos[1] + direction
            if new_col < 0 or new_col + veh.len > self.col:
                return False
            
            # Clear old position
            for j in range(veh.pos[1], veh.pos[1] + veh.len):
                self.grid[veh.pos[0]][j] = 0
            
            # Check new position
            for j in range(new_col, new_col + veh.len):
                if self.grid[veh.pos[0]][j] != 0:
                    # Restore original position
                    for j in range(veh.pos[1], veh.pos[1] + veh.len):
                        self.grid[veh.pos[0]][j] = veh.id
                    return False
            
            # Update position
            veh.pos[1] = new_col
            for j in range(new_col, new_col + veh.len):
                self.grid[veh.pos[0]][j] = veh.id
            return True
                
        elif veh.dir == "v":
            # Move rows
            new_row = veh.pos[0] + direction
            if new_row < 0 or new_row + veh.len > self.row:
                return False
            
            # Clear old position
            for i in range(veh.pos[0], veh.pos[0] + veh.len):
                self.grid[i][veh.pos[1]] = 0
            
            # Check new position
            for i in range(new_row, new_row + veh.len):
                if self.grid[i][veh.pos[1]] != 0:
                    # Restore original position
                    for i in range(veh.pos[0], veh.pos[0] + veh.len):
                        self.grid[i][veh.pos[1]] = veh.id
                    return False
            
            # Update position
            veh.pos[0] = new_row
            for i in range(new_row, new_row + veh.len):
                self.grid[i][veh.pos[1]] = veh.id
            return True

    def is_goal(self, state):
        # Find red car (kind 'x')
        for vid, vehicle in state.vehicles.items():
            if vehicle.kind == 'x':
                # Check if at exit position (row 2, touching right edge)
                if vehicle.dir == 'h' and \
                   vehicle.pos[0] == 2 and \
                   vehicle.pos[1] + vehicle.len == self.col:
                    return True
        return False

    def get_valid_moves(self, state):
        valid_moves = []
        for vid, vehicle in state.vehicles.items():
            # Horizontal vehicles can move left/right
            if vehicle.dir == "h":
                # Check left
                step = -1
                while True:
                    new_col = vehicle.pos[1] + step
                    if new_col < 0:
                        break
                    if self._can_move(vid, step, state.vehicles):
                        valid_moves.append((vid, step))
                        step -= 1
                    else:
                        break

                # Check right
                step = 1
                while True:
                    new_col = vehicle.pos[1] + step
                    if new_col + vehicle.len > self.col:
                        break
                    if self._can_move(vid, step, state.vehicles):
                        valid_moves.append((vid, step))
                        step += 1
                    else:
                        break

            # Vertical vehicles can move up/down
            else:
                # Check up
                step = -1
                while True:
                    new_row = vehicle.pos[0] + step
                    if new_row < 0:
                        break
                    if self._can_move(vid, step, state.vehicles):
                        valid_moves.append((vid, step))
                        step -= 1
                    else:
                        break

                # Check down
                step = 1
                while True:
                    new_row = vehicle.pos[0] + step
                    if new_row + vehicle.len > self.row:
                        break
                    if self._can_move(vid, step, state.vehicles):
                        valid_moves.append((vid, step))
                        step += 1
                    else:
                        break
        return valid_moves

    def _can_move(self, vehicle_id, step, vehicles):
        vehicle = vehicles[vehicle_id]
        if vehicle.dir == "h":
            if step < 0:  # Moving left
                check_col = vehicle.pos[1] + step
                if check_col < 0:
                    return False
                return self.grid[vehicle.pos[0]][check_col] == 0
            else:  # Moving right
                check_col = vehicle.pos[1] + vehicle.len - 1 + step
                if check_col >= self.col:
                    return False
                return self.grid[vehicle.pos[0]][check_col] == 0
        else:  # Vertical
            if step < 0:  # Moving up
                check_row = vehicle.pos[0] + step
                if check_row < 0:
                    return False
                return self.grid[check_row][vehicle.pos[1]] == 0
            else:  # Moving down
                check_row = vehicle.pos[0] + vehicle.len - 1 + step
                if check_row >= self.row:
                    return False
                return self.grid[check_row][vehicle.pos[1]] == 0

    def apply_move(self, state, move):
        vehicle_id, step = move
        new_vehicles = {}
        for vid, vehicle in state.vehicles.items():
            if vid == vehicle_id:
                # Create moved vehicle
                if vehicle.dir == "h":
                    new_pos = [vehicle.pos[0], vehicle.pos[1] + step]
                else:
                    new_pos = [vehicle.pos[0] + step, vehicle.pos[1]]
                new_vehicle = Vehicle(vehicle.kind, new_pos, vehicle.dir, vid)
                new_vehicle.len = vehicle.len
                new_vehicles[vid] = new_vehicle
            else:
                # Copy other vehicles
                new_vehicles[vid] = Vehicle(vehicle.kind, vehicle.pos.copy(), vehicle.dir, vid)
                new_vehicles[vid].len = vehicle.len
        
        # Create new state
        new_moves = state.moves + [move]
        new_cost = state.cost + 1
        return State(new_vehicles, new_moves, new_cost)

    def heuristic(self, state):
        # Simple heuristic: distance of red car to exit
        for vid, vehicle in state.vehicles.items():
            if vehicle.kind == 'x':
                # Distance to right edge
                return self.col - (vehicle.pos[1] + vehicle.len)
        return 0