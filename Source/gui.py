import pygame
import pygame.gfxdraw
import asyncio
import os
import csv
from board import State, Vehicle, GRID_SIZE, EXIT_POS
from map_loader import load_map
from typing import List, Optional

# Constants
CELL_SIZE = 80
WINDOW_SIZE = GRID_SIZE * CELL_SIZE + 200
FPS = 30

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)  # Target car
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
GRAY = (128, 128, 128)
YELLOW = (255, 255, 0)  # Exit
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)

class GUI:
    def __init__(self, board, search_algorithms):
        pygame.init()
        self.screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
        pygame.display.set_caption("Rush Hour")
        self.font = pygame.font.SysFont("arial", 24)
        self.clock = pygame.time.Clock()
        self.board = board
        self.search_algorithms = search_algorithms
        self.state = self.board.initial_state
        self.solution = None
        self.current_step = 0
        self.playing = False
        self.algorithm = None
        self.stats = {"nodes": 0, "time": 0.0, "memory": 0.0}
        self.map_num = 1

        # Buttons for algorithm selection (Q&A #22)
        self.buttons = {
            "BFS": pygame.Rect(WINDOW_SIZE - 180, 20, 80, 40),
            "DFS": pygame.Rect(WINDOW_SIZE - 180, 70, 80, 40),
            "UCS": pygame.Rect(WINDOW_SIZE - 180, 120, 80, 40),
            "A*": pygame.Rect(WINDOW_SIZE - 180, 170, 80, 40),
            "Play/Pause": pygame.Rect(WINDOW_SIZE - 180, 220, 80, 40),
            "Reset": pygame.Rect(WINDOW_SIZE - 180, 270, 80, 40),
            "Prev Map": pygame.Rect(WINDOW_SIZE - 180, 320, 80, 40),
            "Next Map": pygame.Rect(WINDOW_SIZE - 180, 370, 80, 40),
        }

    def draw_board(self, state: State):
        self.screen.fill(WHITE)
        # Draw 6x6 grid (Q&A #3)
        for i in range(GRID_SIZE):
            for j in range(GRID_SIZE):
                pygame.draw.rect(self.screen, BLACK, (j * CELL_SIZE, i * CELL_SIZE, CELL_SIZE, CELL_SIZE), 1)
        
        # Draw exit
        pygame.draw.rect(self.screen, YELLOW, (EXIT_POS[0] * CELL_SIZE, EXIT_POS[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
        
        # Draw vehicles (Q&A #7, #10: red car ID 0, length 2)
        colors = [RED, BLUE, GREEN, PURPLE, ORANGE, GRAY, (0, 128, 128), (255, 192, 203)]
        for vehicle in state.vehicles:
            color = colors[vehicle.id % len(colors)]
            if vehicle.is_horizontal:
                pygame.draw.rect(self.screen, color, 
                               (vehicle.col * CELL_SIZE + 2, vehicle.row * CELL_SIZE + 2, 
                                vehicle.length * CELL_SIZE - 4, CELL_SIZE - 4))
            else:
                pygame.draw.rect(self.screen, color,
                               (vehicle.col * CELL_SIZE + 2, vehicle.row * CELL_SIZE + 2,
                                CELL_SIZE - 4, vehicle.length * CELL_SIZE - 4))
            text = self.font.render(chr(65 + vehicle.id), True, BLACK)
            self.screen.blit(text, (vehicle.col * CELL_SIZE + 10, vehicle.row * CELL_SIZE + 10))

        # Draw buttons
        for name, rect in self.buttons.items():
            pygame.draw.rect(self.screen, GRAY, rect)
            text = self.font.render(name, True, BLACK)
            self.screen.blit(text, (rect.x + 10, rect.y + 10))

        # Draw stats (optional, Q&A #8)
        stats_text = [
            f"Map: {self.map_num}",
            f"Step: {self.current_step}",
            f"Cost: {self.state.cost}",
            f"Nodes: {self.stats['nodes']}",
            f"Time: {self.stats['time']:.2f}s",
            f"Memory: {self.stats['memory'] / 1024:.2f}KB"
        ]
        for i, text in enumerate(stats_text):
            self.screen.blit(self.font.render(text, True, BLACK), (WINDOW_SIZE - 180, 420 + i * 30))

        # No solution message (Q&A #1: some maps unsolvable)
        if self.solution is None and self.algorithm:
            self.screen.blit(self.font.render("No solution found!", True, RED), (20, WINDOW_SIZE - 30))

        pygame.display.flip()

        # Log stats for experiments (Q&A #5)
        if self.algorithm and self.solution:
            with open('stats.csv', 'a') as f:
                writer = csv.writer(f)
                writer.writerow([self.map_num, self.algorithm, self.stats['nodes'], self.stats['time'], self.stats['memory'] / 1024, self.current_step])

    async def main(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    pos = event.pos
                    for name, rect in self.buttons.items():
                        if rect.collidepoint(pos):
                            if name in ["BFS", "DFS", "UCS", "A*"]:
                                self.algorithm = name
                                self.current_step = 0
                                self.state = self.board.initial_state
                                self.playing = False
                                if name == "BFS":
                                    self.solution, self.stats["nodes"], self.stats["time"], self.stats["memory"] = self.search_algorithms.bfs()
                                elif name == "DFS":
                                    self.solution, self.stats["nodes"], self.stats["time"], self.stats["memory"] = self.search_algorithms.dfs()
                                elif name == "UCS":
                                    self.solution, self.stats["nodes"], self.stats["time"], self.stats["memory"] = self.search_algorithms.ucs()
                                elif name == "A*":
                                    self.solution, self.stats["nodes"], self.stats["time"], self.stats["memory"] = self.search_algorithms.a_star()
                            elif name == "Play/Pause":
                                if self.solution:
                                    self.playing = not self.playing
                            elif name == "Reset":
                                self.state = self.board.initial_state
                                self.current_step = 0
                                self.playing = False
                            elif name == "Prev Map":
                                new_map_num = max(1, self.map_num - 1)
                                if os.path.exists(os.path.join("Map", f"map{new_map_num}.txt")):
                                    self.map_num = new_map_num
                                    self.board.initial_state = State(vehicles=load_map(f"map{self.map_num}.txt"))
                                    self.state = self.board.initial_state
                                    self.solution = None
                                    self.current_step = 0
                                    self.playing = False
                                    self.algorithm = None
                            elif name == "Next Map":
                                new_map_num = min(10, self.map_num + 1)
                                if os.path.exists(os.path.join("Map", f"map{new_map_num}.txt")):
                                    self.map_num = new_map_num
                                    self.board.initial_state = State(vehicles=load_map(f"map{new_map_num}.txt"))
                                    self.state = self.board.initial_state
                                    self.solution = None
                                    self.current_step = 0
                                    self.playing = False
                                    self.algorithm = None

            if self.playing and self.solution:
                path = []
                state = self.solution
                while state:
                    path.append(state)
                    state = state.parent
                path.reverse()
                if self.current_step < len(path):
                    self.state = path[self.current_step]
                    self.current_step += 1
                    self.draw_board(self.state)
                    await asyncio.sleep(0.5)  # Minimal animation (Q&A #15)
                else:
                    self.playing = False

            self.draw_board(self.state)
            self.clock.tick(FPS)
            await asyncio.sleep(1.0 / FPS)

        pygame.quit()