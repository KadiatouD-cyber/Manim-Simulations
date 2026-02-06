from manim import *
import numpy as np
from queue import PriorityQueue

config.pixel_height = 1920
config.pixel_width = 1080
config.frame_rate = 60
config.frame_height = 16.0
config.frame_width = 9.0

class AStarPathfinding(Scene):
    def construct(self):
        # TechFlux Color Scheme
        primary_purple = "#9D4EDD"
        light_purple = "#C77DFF"
        pink_purple = "#E0AAFF"
        deep_purple = "#7B2CBF"
        accent_cyan = "#00D9FF"
        
        self.camera.background_color = "#0a0a0a"
        
        # TechFlux Branding
        techflux = Text("TechFlux", font_size=44, weight=BOLD, color=primary_purple)
        subtitle_brand = Text("Physics Explained", font_size=24, color=accent_cyan)
        brand_group = VGroup(techflux, subtitle_brand).arrange(DOWN, buff=0.1, aligned_edge=RIGHT)
        brand_group.to_corner(DR, buff=0.5)
        self.add(brand_group)
        
        # Title
        title = Text("A* Pathfinding Algorithm", font_size=48, weight=BOLD, color=light_purple)
        title.to_edge(UP, buff=1.2)
        self.add(title)
        
        # Subtitle
        subtitle = Text("Finding the shortest path", font_size=32, color=pink_purple)
        subtitle.next_to(title, DOWN, buff=0.3)
        self.play(FadeIn(subtitle), run_time=0.5)
        self.wait(0.8)
        self.play(FadeOut(subtitle), run_time=0.3)
        
        # Grid parameters
        rows, cols = 15, 9
        cell_size = 0.45
        
        # Create grid
        grid = VGroup()
        cells = {}
        
        grid_height = rows * cell_size
        grid_width = cols * cell_size
        start_x = -grid_width / 2 + cell_size / 2
        start_y = grid_height / 2 - cell_size / 2 - 1.5  # Shifted down
        
        for i in range(rows):
            for j in range(cols):
                cell = Square(
                    side_length=cell_size,
                    color=deep_purple,
                    fill_color=BLACK,
                    fill_opacity=1,
                    stroke_width=2
                )
                x = start_x + j * cell_size
                y = start_y - i * cell_size
                cell.move_to([x, y, 0])
                grid.add(cell)
                cells[(i, j)] = cell
        
        self.play(Create(grid), run_time=1)
        self.wait(0.3)
        
        # Define obstacles (walls)
        obstacles = [
            (2, 3), (3, 3), (4, 3), (5, 3), (6, 3), (7, 3),
            (7, 4), (7, 5), (7, 6),
            (3, 6), (4, 6), (5, 6), (6, 6),
            (10, 2), (11, 2), (12, 2),
            (10, 5), (11, 5), (12, 5),
            (9, 3), (9, 4),
        ]
        
        # Add obstacles
        obstacle_label = Text("Add obstacles", font_size=32, color=accent_cyan, weight=BOLD)
        obstacle_label.shift(DOWN * 6.5)
        self.play(FadeIn(obstacle_label), run_time=0.3)
        
        obstacle_anims = []
        for pos in obstacles:
            obstacle_anims.append(cells[pos].animate.set_fill(GRAY, opacity=1))
        
        self.play(*obstacle_anims, run_time=1)
        self.play(FadeOut(obstacle_label), run_time=0.3)
        self.wait(0.3)
        
        # Set start and end positions
        start_pos = (7, 1)
        end_pos = (7, 7)
        
        # Mark start
        start_label = Text("Start", font_size=32, color=GREEN, weight=BOLD)
        start_label.shift(DOWN * 6.5)
        self.play(FadeIn(start_label), run_time=0.3)
        
        self.play(
            cells[start_pos].animate.set_fill(GREEN, opacity=0.8),
            run_time=0.5
        )
        
        start_marker = Text("S", font_size=20, color=WHITE, weight=BOLD)
        start_marker.move_to(cells[start_pos].get_center())
        self.play(FadeIn(start_marker), run_time=0.3)
        self.play(FadeOut(start_label), run_time=0.3)
        
        # Mark end
        end_label = Text("Goal", font_size=32, color=RED, weight=BOLD)
        end_label.shift(DOWN * 6.5)
        self.play(FadeIn(end_label), run_time=0.3)
        
        self.play(
            cells[end_pos].animate.set_fill(RED, opacity=0.8),
            run_time=0.5
        )
        
        end_marker = Text("G", font_size=20, color=WHITE, weight=BOLD)
        end_marker.move_to(cells[end_pos].get_center())
        self.play(FadeIn(end_marker), run_time=0.3)
        self.play(FadeOut(end_label), run_time=0.3)
        
        self.wait(0.5)
        
        # A* Algorithm implementation
        def heuristic(pos1, pos2):
            # Manhattan distance
            return abs(pos1[0] - pos2[0]) + abs(pos1[1] - pos2[1])
        
        def get_neighbors(pos):
            neighbors = []
            directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Right, Down, Left, Up
            for d in directions:
                new_pos = (pos[0] + d[0], pos[1] + d[1])
                if (0 <= new_pos[0] < rows and 0 <= new_pos[1] < cols and 
                    new_pos not in obstacles):
                    neighbors.append(new_pos)
            return neighbors
        
        # Run A* algorithm
        search_label = Text("Searching...", font_size=32, color=accent_cyan, weight=BOLD)
        search_label.shift(DOWN * 6.5)
        self.play(FadeIn(search_label), run_time=0.3)
        
        open_set = PriorityQueue()
        open_set.put((0, start_pos))
        came_from = {}
        g_score = {start_pos: 0}
        f_score = {start_pos: heuristic(start_pos, end_pos)}
        
        visited = set()
        visited.add(start_pos)
        
        found = False
        
        # A* search with animation
        while not open_set.empty():
            current = open_set.get()[1]
            
            if current == end_pos:
                found = True
                break
            
            # Explore neighbors
            for neighbor in get_neighbors(current):
                tentative_g = g_score[current] + 1
                
                if neighbor not in g_score or tentative_g < g_score[neighbor]:
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + heuristic(neighbor, end_pos)
                    
                    if neighbor not in visited:
                        open_set.put((f_score[neighbor], neighbor))
                        visited.add(neighbor)
                        
                        # Animate exploration
                        if neighbor != end_pos:
                            self.play(
                                cells[neighbor].animate.set_fill(accent_cyan, opacity=0.4),
                                run_time=0.05
                            )
        
        self.play(FadeOut(search_label), run_time=0.3)
        
        if found:
            # Reconstruct path
            path = []
            current = end_pos
            while current in came_from:
                current = came_from[current]
                path.append(current)
            path.reverse()
            path.append(end_pos)
            
            # Show path
            path_label = Text("Path found!", font_size=32, color=GREEN, weight=BOLD)
            path_label.shift(DOWN * 6.5)
            self.play(FadeIn(path_label), run_time=0.3)
            
            # Animate path
            for i, pos in enumerate(path):
                if pos != start_pos and pos != end_pos:
                    self.play(
                        cells[pos].animate.set_fill(YELLOW, opacity=0.9),
                        run_time=0.1
                    )
            
            self.wait(1)
            self.play(FadeOut(path_label), run_time=0.3)
            
            # Show path length
            length_text = Text(f"Path length: {len(path)} steps", 
                             font_size=28, color=light_purple, weight=BOLD)
            length_text.shift(DOWN * 6.5)
            self.play(FadeIn(length_text), run_time=0.5)
            self.wait(1.5)
            self.play(FadeOut(length_text), run_time=0.3)
        
        # Key insights
        self.play(*[FadeOut(m) for m in [grid, start_marker, end_marker]], run_time=0.5)
        
        insights_title = Text("How A* Works:", font_size=40, color=accent_cyan, weight=BOLD)
        insights_title.shift(UP * 5)
        self.play(FadeIn(insights_title), run_time=0.4)
        
        insights = VGroup(
            Text("• Uses heuristic to estimate distance to goal", font_size=26, color=light_purple),
            Text("• Explores most promising paths first", font_size=26, color=light_purple),
            Text("• Guarantees shortest path if heuristic is valid", font_size=26, color=light_purple),
            Text("• Faster than Dijkstra's for single target", font_size=26, color=light_purple)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        insights.shift(UP * 1.5)
        
        self.play(LaggedStart(*[FadeIn(i, shift=RIGHT * 0.3) for i in insights], lag_ratio=0.3))
        self.wait(2.5)
        
        self.play(FadeOut(insights), FadeOut(insights_title), run_time=0.5)
        
        # Applications
        apps_title = Text("Real-World Uses:", font_size=40, color=accent_cyan, weight=BOLD)
        apps_title.shift(UP * 5)
        self.play(FadeIn(apps_title), run_time=0.4)
        
        applications = VGroup(
            Text("🎮 Video game AI navigation", font_size=32, color=light_purple),
            Text("🗺️ GPS route planning", font_size=32, color=light_purple),
            Text("🤖 Robot path planning", font_size=32, color=light_purple),
            Text("📦 Logistics optimization", font_size=32, color=light_purple)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.5)
        applications.shift(UP * 1)
        
        self.play(LaggedStart(*[FadeIn(app, shift=RIGHT * 0.3) for app in applications], lag_ratio=0.3))
        self.wait(2.5)
        
        # Fade out
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1)
        self.wait(0.5)