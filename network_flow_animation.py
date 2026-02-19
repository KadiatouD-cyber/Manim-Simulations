from manim import *
import numpy as np

# Configure for vertical Instagram Reels format
config.pixel_height = 1920
config.pixel_width = 1080
config.frame_rate = 60
config.frame_height = 16.0
config.frame_width = 9.0

class NetworkFlow(Scene):
    def construct(self):
        # TechFlux color scheme
        primary_purple = "#9D4EDD"
        light_purple = "#C77DFF"
        pink_purple = "#E0AAFF"
        deep_purple = "#7B2CBF"
        accent_cyan = "#00D9FF"
        
        # Set dark background
        self.camera.background_color = "#0a0a0a"
        
        # TechFlux branding (stays throughout)
        techflux = Text("TechFlux", font_size=44, weight=BOLD, color=primary_purple)
        techflux.to_corner(DR, buff=0.5)
        self.add(techflux)
        
        # Title
        title = Text("Network Flow", font_size=60, weight=BOLD, color=light_purple)
        title.shift(UP * 6.8)
        self.add(title)
        
        # Subtitle
        subtitle = Text("Maximum Flow Problem", font_size=32, color=accent_cyan)
        subtitle.next_to(title, DOWN, buff=0.3)
        self.play(FadeIn(subtitle))
        self.wait(1)
        self.play(FadeOut(subtitle))
        
        # Problem statement
        problem = Text("Find maximum flow from Source to Sink", font_size=28, color=light_purple)
        problem.shift(UP * 6)
        self.play(FadeIn(problem))
        self.wait(1)
        
        # Create network graph
        # Node positions - adjusted to fit within frame
        source_pos = LEFT * 2.8 + UP * 2
        a_pos = LEFT * 0.3 + UP * 3.5
        b_pos = LEFT * 0.3 + UP * 0.5
        c_pos = RIGHT * 1.8 + UP * 3.5
        d_pos = RIGHT * 1.8 + UP * 0.5
        sink_pos = RIGHT * 3.8 + UP * 2
        
        positions = {
            'S': source_pos,
            'A': a_pos,
            'B': b_pos,
            'C': c_pos,
            'D': d_pos,
            'T': sink_pos
        }
        
        # Create nodes
        nodes = {}
        for name, pos in positions.items():
            if name == 'S':
                color = GREEN
                label = "Source"
            elif name == 'T':
                color = RED
                label = "Sink"
            else:
                color = accent_cyan
                label = name
            
            circle = Circle(radius=0.35, color=color, fill_opacity=0.3, stroke_width=3)
            circle.move_to(pos)
            text = Text(label if name in ['S', 'T'] else name, font_size=24, color=WHITE, weight=BOLD)
            text.move_to(pos)
            
            node = VGroup(circle, text)
            nodes[name] = node
        
        # Edge capacities (capacity, flow)
        edges_data = {
            ('S', 'A'): (10, 0),
            ('S', 'B'): (5, 0),
            ('A', 'C'): (9, 0),
            ('A', 'B'): (4, 0),
            ('B', 'D'): (10, 0),
            ('C', 'T'): (10, 0),
            ('C', 'D'): (6, 0),
            ('D', 'T'): (10, 0),
        }
        
        # Create edges with labels
        edges = {}
        edge_labels = {}
        
        for (start, end), (capacity, flow) in edges_data.items():
            start_pos = positions[start]
            end_pos = positions[end]
            
            # Create arrow
            arrow = Arrow(
                start_pos + (end_pos - start_pos) * 0.12,
                end_pos - (end_pos - start_pos) * 0.12,
                buff=0,
                stroke_width=3,
                color=deep_purple,
                max_tip_length_to_length_ratio=0.15
            )
            
            # Label position (middle of edge)
            mid_point = (start_pos + end_pos) / 2
            # Offset label slightly
            offset = np.array([0, 0.3, 0]) if start != 'A' or end != 'B' else np.array([0, -0.3, 0])
            
            label = Text(f"{flow}/{capacity}", font_size=20, color=light_purple)
            label.move_to(mid_point + offset)
            
            edges[(start, end)] = arrow
            edge_labels[(start, end)] = label
        
        # Show graph
        self.play(LaggedStart(*[FadeIn(node) for node in nodes.values()], lag_ratio=0.1))
        self.wait(0.5)
        self.play(LaggedStart(*[Create(edge) for edge in edges.values()], lag_ratio=0.08))
        self.play(LaggedStart(*[FadeIn(label) for label in edge_labels.values()], lag_ratio=0.08))
        self.wait(1)
        
        # Max flow display
        flow_label = Text("Max Flow: ", font_size=36, color=accent_cyan, weight=BOLD)
        flow_label.shift(DOWN * 2.5)
        flow_value = Integer(0, font_size=40, color=GREEN)
        flow_value.next_to(flow_label, RIGHT, buff=0.3)
        
        self.play(FadeIn(VGroup(flow_label, flow_value)))
        
        # Simulate Ford-Fulkerson algorithm
        # Path 1: S -> A -> C -> T (flow = 9)
        path1 = ['S', 'A', 'C', 'T']
        path1_flow = 9
        
        self.wait(0.5)
        path_text = Text("Path 1: S → A → C → T", font_size=28, color=GREEN)
        path_text.shift(DOWN * 3.5)
        self.play(FadeIn(path_text))
        
        # Highlight path
        path_edges = [edges[('S', 'A')], edges[('A', 'C')], edges[('C', 'T')]]
        self.play(*[edge.animate.set_color(GREEN).set_stroke_width(5) for edge in path_edges])
        self.wait(0.5)
        
        # Update flow
        edges_data[('S', 'A')] = (10, 9)
        edges_data[('A', 'C')] = (9, 9)
        edges_data[('C', 'T')] = (10, 9)
        
        self.play(
            edge_labels[('S', 'A')].animate.become(Text("9/10", font_size=20, color=light_purple).move_to(edge_labels[('S', 'A')])),
            edge_labels[('A', 'C')].animate.become(Text("9/9", font_size=20, color=light_purple).move_to(edge_labels[('A', 'C')])),
            edge_labels[('C', 'T')].animate.become(Text("9/10", font_size=20, color=light_purple).move_to(edge_labels[('C', 'T')])),
            flow_value.animate.set_value(9),
            run_time=1
        )
        
        # Reset edge colors
        self.play(*[edge.animate.set_color(deep_purple).set_stroke_width(3) for edge in path_edges])
        self.play(FadeOut(path_text))
        self.wait(0.5)
        
        # Path 2: S -> A -> B -> D -> T (flow = 1)
        path2_text = Text("Path 2: S → A → B → D → T", font_size=28, color=GREEN)
        path2_text.shift(DOWN * 3.5)
        self.play(FadeIn(path2_text))
        
        path2_edges = [edges[('S', 'A')], edges[('A', 'B')], edges[('B', 'D')], edges[('D', 'T')]]
        self.play(*[edge.animate.set_color(GREEN).set_stroke_width(5) for edge in path2_edges])
        self.wait(0.5)
        
        edges_data[('S', 'A')] = (10, 10)
        edges_data[('A', 'B')] = (4, 1)
        edges_data[('B', 'D')] = (10, 1)
        edges_data[('D', 'T')] = (10, 1)
        
        self.play(
            edge_labels[('S', 'A')].animate.become(Text("10/10", font_size=20, color=light_purple).move_to(edge_labels[('S', 'A')])),
            edge_labels[('A', 'B')].animate.become(Text("1/4", font_size=20, color=light_purple).move_to(edge_labels[('A', 'B')])),
            edge_labels[('B', 'D')].animate.become(Text("1/10", font_size=20, color=light_purple).move_to(edge_labels[('B', 'D')])),
            edge_labels[('D', 'T')].animate.become(Text("1/10", font_size=20, color=light_purple).move_to(edge_labels[('D', 'T')])),
            flow_value.animate.set_value(10),
            run_time=1
        )
        
        self.play(*[edge.animate.set_color(deep_purple).set_stroke_width(3) for edge in path2_edges])
        self.play(FadeOut(path2_text))
        self.wait(0.5)
        
        # Path 3: S -> B -> D -> C -> T (flow = 5)
        path3_text = Text("Path 3: S → B → D → T", font_size=28, color=GREEN)
        path3_text.shift(DOWN * 3.5)
        self.play(FadeIn(path3_text))
        
        path3_edges = [edges[('S', 'B')], edges[('B', 'D')], edges[('D', 'T')]]
        self.play(*[edge.animate.set_color(GREEN).set_stroke_width(5) for edge in path3_edges])
        self.wait(0.5)
        
        edges_data[('S', 'B')] = (5, 5)
        edges_data[('B', 'D')] = (10, 6)
        edges_data[('D', 'T')] = (10, 6)
        
        self.play(
            edge_labels[('S', 'B')].animate.become(Text("5/5", font_size=20, color=light_purple).move_to(edge_labels[('S', 'B')])),
            edge_labels[('B', 'D')].animate.become(Text("6/10", font_size=20, color=light_purple).move_to(edge_labels[('B', 'D')])),
            edge_labels[('D', 'T')].animate.become(Text("6/10", font_size=20, color=light_purple).move_to(edge_labels[('D', 'T')])),
            flow_value.animate.set_value(15),
            run_time=1
        )
        
        self.play(*[edge.animate.set_color(deep_purple).set_stroke_width(3) for edge in path3_edges])
        self.play(FadeOut(path3_text))
        self.wait(1)
        
        # Final result
        result_text = Text("Maximum Flow Achieved!", font_size=36, color=GREEN, weight=BOLD)
        result_text.shift(DOWN * 3.5)
        self.play(FadeIn(result_text, scale=1.2))
        self.wait(2)
        
        # Clean up for explanations
        self.play(
            FadeOut(VGroup(*nodes.values())),
            FadeOut(VGroup(*edges.values())),
            FadeOut(VGroup(*edge_labels.values())),
            FadeOut(flow_label),
            FadeOut(flow_value),
            FadeOut(result_text),
            FadeOut(problem)
        )
        
        # Key concepts
        concepts_title = Text("Key Concepts", font_size=44, color=accent_cyan, weight=BOLD)
        concepts_title.shift(UP * 5)
        
        concepts = VGroup(
            Text("• Capacity: Maximum flow per edge", font_size=32, color=light_purple),
            Text("• Augmenting path: Route from S to T", font_size=32, color=light_purple),
            Text("• Residual capacity: Remaining space", font_size=32, color=light_purple),
            Text("• Bottleneck: Smallest capacity in path", font_size=32, color=light_purple),
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        concepts.shift(UP * 1.5)
        
        self.play(FadeIn(concepts_title))
        self.play(LaggedStart(*[FadeIn(concept, shift=RIGHT*0.3) for concept in concepts], lag_ratio=0.2))
        self.wait(2.5)
        
        self.play(FadeOut(concepts_title), FadeOut(concepts))
        
        # Applications
        app_title = Text("Real-World Applications", font_size=40, color=accent_cyan, weight=BOLD)
        app_title.shift(UP * 4.5)
        
        applications = VGroup(
            Text("• Network routing & bandwidth", font_size=32, color=light_purple),
            Text("• Supply chain optimization", font_size=32, color=light_purple),
            Text("• Traffic flow management", font_size=32, color=light_purple),
            Text("• Bipartite matching problems", font_size=32, color=light_purple),
            Text("• Image segmentation", font_size=32, color=light_purple),
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        applications.shift(UP * 1)
        
        self.play(FadeIn(app_title))
        self.play(LaggedStart(*[FadeIn(app, shift=RIGHT*0.3) for app in applications], lag_ratio=0.15))
        self.wait(2.5)
        
        self.play(FadeOut(app_title), FadeOut(applications), FadeOut(title))
        
        # Follow for more
        follow_text = VGroup(
            Text("Follow for more", font_size=50, color=accent_cyan, weight=BOLD),
            Text("algorithms explained", font_size=34, color=light_purple)
        ).arrange(DOWN, buff=0.4)
        follow_text.shift(UP * 1.5)
        
        arrow = Arrow(
            follow_text.get_bottom() + DOWN * 0.5,
            follow_text.get_bottom() + DOWN * 1.8,
            color=accent_cyan,
            stroke_width=9,
            max_tip_length_to_length_ratio=0.3
        )
        
        self.play(FadeIn(follow_text, scale=1.2), GrowArrow(arrow))
        
        self.play(
            follow_text.animate.scale(1.1),
            arrow.animate.shift(DOWN * 0.3),
            rate_func=there_and_back,
            run_time=0.8
        )
        
        self.wait(2)
        
        self.play(FadeOut(follow_text), FadeOut(arrow), FadeOut(techflux))
        self.wait(0.5)