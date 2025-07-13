from Board import Board
from State import State
from typing import List, Tuple, Optional
import queue
import heapq
import time
import tracemalloc

class SearchAlgorithms:
    def __init__(self, board: Board):
        self.board = board
        self.expanded_nodes = 0
        self.search_time = 0
        self.memory_used = 0

    def bfs(self) -> Tuple[Optional[State], int, float, int]:
        tracemalloc.start()
        start_time = time.time()
        self.expanded_nodes = 0
        visited = set()
        q = queue.Queue()
        initial_state = State(self.board.vehicles.copy())
        q.put(initial_state)
        visited.add(initial_state)

        while not q.empty():
            state = q.get()
            self.expanded_nodes += 1

            if self.board.is_goal(state):
                self.search_time = time.time() - start_time
                _, peak_memory = tracemalloc.get_traced_memory()
                tracemalloc.stop()
                return state, self.expanded_nodes, self.search_time, peak_memory

            for move in self.board.get_valid_moves(state):
                new_state = self.board.apply_move(state, move)
                if new_state not in visited:
                    visited.add(new_state)
                    q.put(new_state)

        self.search_time = time.time() - start_time
        _, peak_memory = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        return None, self.expanded_nodes, self.search_time, peak_memory

    def dfs(self, max_depth: int = 50) -> Tuple[Optional[State], int, float, int]:
        tracemalloc.start()
        start_time = time.time()
        self.expanded_nodes = 0
        visited = set()

        def backtrack(state: State, depth: int) -> Optional[State]:
            if depth > max_depth:
                return None
            self.expanded_nodes += 1
            if self.board.is_goal(state):
                return state
            if state not in visited:
                visited.add(state)
                for move in self.board.get_valid_moves(state):
                    new_state = self.board.apply_move(state, move)
                    result = backtrack(new_state, depth + 1)
                    if result:
                        return result
            return None

        initial_state = State(self.board.vehicles.copy())
        result = backtrack(initial_state, 0)
        self.search_time = time.time() - start_time
        _, peak_memory = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        return result, self.expanded_nodes, self.search_time, peak_memory

    def ucs(self) -> Tuple[Optional[State], int, float, int]:
        tracemalloc.start()
        start_time = time.time()
        self.expanded_nodes = 0
        visited = set()
        initial_state = State(self.board.vehicles.copy())
        pq = [(0, initial_state)]  # (cost, state)
        heapq.heapify(pq)

        while pq:
            cost, state = heapq.heappop(pq)
            self.expanded_nodes += 1

            if self.board.is_goal(state):
                self.search_time = time.time() - start_time
                _, peak_memory = tracemalloc.get_traced_memory()
                tracemalloc.stop()
                return state, self.expanded_nodes, self.search_time, peak_memory

            if state not in visited:
                visited.add(state)
                for move in self.board.get_valid_moves(state):
                    new_state = self.board.apply_move(state, move)
                    if new_state not in visited:
                        heapq.heappush(pq, (new_state.cost, new_state))

        self.search_time = time.time() - start_time
        _, peak_memory = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        return None, self.expanded_nodes, self.search_time, peak_memory

    def a_star(self) -> Tuple[Optional[State], int, float, int]:
        tracemalloc.start()
        start_time = time.time()
        self.expanded_nodes = 0
        initial_state = State(self.board.vehicles.copy())
        initial_state.heuristic = self.board.heuristic(initial_state)
        pq = [(initial_state.heuristic, initial_state)]  # (f_score, state)
        g_scores = {initial_state: 0}
        visited = set()

        while pq:
            f_score, state = heapq.heappop(pq)
            if self.board.is_goal(state):
                self.search_time = time.time() - start_time
                _, peak_memory = tracemalloc.get_traced_memory()
                tracemalloc.stop()
                return state, self.expanded_nodes, self.search_time, peak_memory

            if state in visited:
                continue
            visited.add(state)
            self.expanded_nodes += 1

            for move in self.board.get_valid_moves(state):
                new_state = self.board.apply_move(state, move)
                new_state.heuristic = self.board.heuristic(new_state)
                if new_state not in g_scores or new_state.cost < g_scores[new_state]:
                    g_scores[new_state] = new_state.cost
                    f_score = new_state.cost + new_state.heuristic
                    heapq.heappush(pq, (f_score, new_state))

        self.search_time = time.time() - start_time
        _, peak_memory = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        return None, self.expanded_nodes, self.search_time, peak_memory