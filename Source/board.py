from dataclasses import dataclass
from typing import List, Tuple
import copy

GRID_SIZE = 6
EXIT_POS = (5, 2)  # Exit tại cột 6, hàng 3 (chỉ số từ 0)

@dataclass
class Vehicle:
    id: int
    length: int
    is_horizontal: bool
    row: int
    col: int

@dataclass
class State:
    vehicles: List[Vehicle]
    parent: 'State' = None
    move: Tuple[int, int] = None  # (vehicle_id, distance)
    cost: int = 0  # Tổng chi phí đường đi (cho UCS)
    heuristic: int = 0  # Giá trị heuristic (cho A*)

    def __hash__(self):
        return hash(tuple((v.id, v.row, v.col) for v in self.vehicles))

    def __eq__(self, other):
        if not isinstance(other, State):
            return False
        return all(v1.row == v2.row and v1.col == v2.col for v1, v2 in zip(self.vehicles, other.vehicles))

    def __lt__(self, other):
        return (self.cost + self.heuristic) < (other.cost + other.heuristic)

class Board:
    def __init__(self, vehicles: List[Vehicle]):
        self.initial_state = State(vehicles=vehicles)

    def is_goal(self, state: State) -> bool:
        target = next(v for v in state.vehicles if v.id == 0)  # Xe mục tiêu (Q&A #7)
        return target.is_horizontal and target.row == EXIT_POS[1] and target.col + target.length - 1 >= EXIT_POS[0]

    def get_valid_moves(self, state: State) -> List[Tuple[int, int]]:
        moves = []
        grid = [[None for _ in range(GRID_SIZE)] for _ in range(GRID_SIZE)]
        
        # Tạo lưới với vị trí các xe
        for vehicle in state.vehicles:
            for i in range(vehicle.length):
                if vehicle.is_horizontal:
                    grid[vehicle.row][vehicle.col + i] = vehicle.id
                else:
                    grid[vehicle.row + i][vehicle.col] = vehicle.id

        # Kiểm tra các nước đi hợp lệ (Q&A #16: hỗ trợ di chuyển nhiều ô)
        for vehicle in state.vehicles:
            if vehicle.is_horizontal:
                # Di chuyển sang trái
                for d in range(1, vehicle.col + 1):
                    if grid[vehicle.row][vehicle.col - d] is not None:
                        break
                    moves.append((vehicle.id, -d))
                # Di chuyển sang phải
                for d in range(1, GRID_SIZE - (vehicle.col + vehicle.length) + 1):
                    if grid[vehicle.row][vehicle.col + vehicle.length + d - 1] is not None:
                        break
                    moves.append((vehicle.id, d))
            else:
                # Di chuyển lên
                for d in range(1, vehicle.row + 1):
                    if grid[vehicle.row - d][vehicle.col] is not None:
                        break
                    moves.append((vehicle.id, -d))
                # Di chuyển xuống
                for d in range(1, GRID_SIZE - (vehicle.row + vehicle.length) + 1):
                    if grid[vehicle.row + vehicle.length + d - 1][vehicle.col] is not None:
                        break
                    moves.append((vehicle.id, d))
        return moves

    def apply_move(self, state: State, move: Tuple[int, int]) -> State:
        vehicle_id, distance = move
        new_vehicles = copy.deepcopy(state.vehicles)
        vehicle = next(v for v in new_vehicles if v.id == vehicle_id)
        
        if vehicle.is_horizontal:
            vehicle.col += distance
        else:
            vehicle.row += distance
            
        # Chi phí = số ô di chuyển × độ dài xe (Q&A #16, #27)
        cost = state.cost + abs(distance) * vehicle.length
        return State(vehicles=new_vehicles, parent=state, move=move, cost=cost)

    def heuristic(self, state: State) -> int:
        # Heuristic: số xe chặn đường (Q&A #4)
        target = next(v for v in state.vehicles if v.id == 0)
        if target.row != EXIT_POS[1]:
            return float('inf')
        blocking = 0
        for col in range(target.col + target.length, GRID_SIZE):
            for vehicle in state.vehicles:
                if vehicle.is_horizontal and vehicle.row == target.row and vehicle.col <= col < vehicle.col + vehicle.length:
                    blocking += 1
                elif not vehicle.is_horizontal and vehicle.col == col and vehicle.row <= target.row < vehicle.row + vehicle.length:
                    blocking += 1
        return blocking