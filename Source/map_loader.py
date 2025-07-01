from board import Vehicle
from typing import List
import os

def load_map(map_file: str) -> List[Vehicle]:
    vehicles = []
    file_path = os.path.join("Map", map_file) if not os.path.isabs(map_file) else map_file
    print(f"Attempting to load map file: {os.path.abspath(file_path)}")
    try:
        with open(file_path, 'r') as f:
            lines = f.readlines()
            num_vehicles = int(lines[0].strip())
            for line in lines[1:]:
                line = line.strip()
                if not line or line.startswith('#'):
                    continue
                line = line.split('#')[0].strip()
                if line:
                    id, length, is_horizontal, row, col = map(int, line.split(','))
                    vehicles.append(Vehicle(id, length, is_horizontal == 1, row, col))
            if len(vehicles) != num_vehicles:
                print(f"Warning: Expected {num_vehicles} vehicles, but loaded {len(vehicles)} in {map_file}")
    except FileNotFoundError:
        print(f"Map file {map_file} not found at {os.path.abspath(file_path)}.")
    except ValueError as e:
        print(f"Error parsing {map_file}: {e}")
    return vehicles

def save_map(vehicles: List[Vehicle], map_file: str):
    try:
        os.makedirs("Map", exist_ok=True)
        file_path = os.path.join("Map", map_file)
        with open(file_path, 'w') as f:
            f.write(f"{len(vehicles)}\n")
            for v in vehicles:
                is_horizontal = 1 if v.is_horizontal else 0
                f.write(f"{v.id},{v.length},{is_horizontal},{v.row},{v.col}\n")
    except OSError as e:
        print(f"Error saving map {map_file}: {e}")