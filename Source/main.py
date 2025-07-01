import asyncio
import platform
import os
from board import Board
from search_algorithms import SearchAlgorithms
from gui import GUI
from map_loader import load_map

async def main():
    print(f"Current working directory: {os.getcwd()}")
    map_file = "/Users/apple/Downloads/AI TEST/Source/Map/map1.txt"  # Use absolute path
    print(f"Attempting to load map file: {map_file}")
    vehicles = load_map(map_file)
    if not vehicles:
        print(f"Failed to load {map_file}. Please check if it exists.")
        return
    board = Board(vehicles)
    search_algorithms = SearchAlgorithms(board)
    gui = GUI(board, search_algorithms)
    await gui.main()

if platform.system() == "Emscripten":
    asyncio.ensure_future(main())
else:
    if __name__ == "__main__":
        asyncio.run(main())