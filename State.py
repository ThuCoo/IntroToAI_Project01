from typing import List, Tuple, Dict
from Vehicle import Vehicle, max

class State:
    def __init__(self, vehicles: Dict[int, Vehicle], moves: List[Tuple[int, int]] = None, cost: int = 0):
        self.vehicles = vehicles
        self.moves = moves if moves is not None else []
        self.cost = cost
        self.heuristic = 0
        self._validate_positions()

    def _validate_positions(self):
        for vid, vehicle in self.vehicles.items():
            if vehicle.dir == "h":
                if (vehicle.pos[0] < 0 or 
                    vehicle.pos[0] + vehicle.len > max + 1 or
                    vehicle.pos[1] < 0 or 
                    vehicle.pos[1] > max):
                    raise ValueError(f"Vehicle {vid} out of bounds: {vehicle.pos}")
            else:
                if (vehicle.pos[0] < 0 or 
                    vehicle.pos[0] > max or
                    vehicle.pos[1] < 0 or 
                    vehicle.pos[1] + vehicle.len > max + 1):
                    raise ValueError(f"Vehicle {vid} out of bounds: {vehicle.pos}")

    def __eq__(self, other):
        if not isinstance(other, State):
            return False
        
        # Compare vehicle positions and directions
        return all(
            v.pos == other.vehicles[vid].pos and 
            v.dir == other.vehicles[vid].dir
            for vid, v in self.vehicles.items()
        )

    def __hash__(self):
        return hash(tuple(
            (vid, v.pos[0], v.pos[1], v.dir, v.len)
            for vid, v in sorted(self.vehicles.items(), key=lambda x: x[0])
        ))

    def __lt__(self, other):
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)