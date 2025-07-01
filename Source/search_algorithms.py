from board import State, Board
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
        initial_state = self.board.initial_state
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

    def dfs(self, max_depth: int = 100) -> Tuple[Optional[State], int, float, int]:
        tracemalloc.start()
        start_time = time.time()
        self.expanded_nodes = 0
        visited = set()

        def backtrack(state: State, depth: int) -> Optional[State]:
            self.expanded_nodes += 1
            if depth > max_depth:
                return None
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

        result = backtrack(self.board.initial_state, 0)
        self.search_time = time.time() - start_time
        _, peak_memory = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        return result, self.expanded_nodes, self.search_time, peak_memory

    def ucs(self) -> Tuple[Optional[State], int, float, int]:
        tracemalloc.start()
        start_time = time.time()
        self.expanded_nodes = 0
        visited = set()
        pq = [(0, self.board.initial_state)]  # (cost, state)
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
        visited = set()
        pq = [(0, self.board.initial_state)]  # (f_score, state)
        heapq.heapify(pq)
        g_scores = {self.board.initial_state: 0}

        while pq:
            f_score, state = heapq.heappop(pq)
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
                        g_score = g_scores[state] + new_state.cost
                        if new_state not in g_scores or g_score < g_scores[new_state]:
                            g_scores[new_state] = g_score
                            new_state.heuristic = self.board.heuristic(new_state)
                            f_score = g_score + new_state.heuristic
                            heapq.heappush(pq, (f_score, new_state))

        self.search_time = time.time() - start_time
        _, peak_memory = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        return None, self.expanded_nodes, self.search_time, peak_memory