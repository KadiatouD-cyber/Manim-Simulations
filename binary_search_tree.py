from manim import *
import numpy as np

config.pixel_height = 1920
config.pixel_width = 1080
config.frame_rate = 60
config.frame_height = 16.0
config.frame_width = 9.0

class BinarySearchTree(Scene):
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
        techflux.to_corner(DR, buff=0.5)
        self.add(techflux)
        
        # Title
        title = Text("Binary Search Tree", font_size=52, weight=BOLD, color=light_purple)
        title.to_edge(UP, buff=1.2)
        self.add(title)
        
        # Subtitle
        subtitle = Text("O(log n) search time", font_size=32, color=accent_cyan)
        subtitle.next_to(title, DOWN, buff=0.3)
        self.play(FadeIn(subtitle), run_time=0.5)
        self.wait(0.8)
        self.play(FadeOut(subtitle), run_time=0.3)
        
        # Node class for visualization
        class TreeNode:
            def __init__(self, value, position):
                self.value = value
                self.position = position
                self.left = None
                self.right = None
                
                # Visual elements
                self.circle = Circle(
                    radius=0.4,
                    color=light_purple,
                    fill_color=primary_purple,
                    fill_opacity=1,
                    stroke_width=4
                )
                self.circle.move_to(position)
                
                self.label = Text(str(value), font_size=32, color=WHITE, weight=BOLD)
                self.label.move_to(position)
                
                self.group = VGroup(self.circle, self.label)
        
        # Tree structure
        nodes = {}
        edges = VGroup()
        
        def create_node(value, position):
            node = TreeNode(value, position)
            nodes[value] = node
            return node
        
        def add_edge(parent, child):
            edge = Line(
                parent.circle.get_center(),
                child.circle.get_center(),
                color=deep_purple,
                stroke_width=3
            )
            edges.add(edge)
            return edge
        
        # Values to insert
        values_to_insert = [50, 30, 70, 20, 40, 60, 80]
        
        # Show insertion process
        insert_label = Text("Inserting values:", font_size=32, color=accent_cyan, weight=BOLD)
        insert_label.shift(UP * 5.5)
        self.play(FadeIn(insert_label), run_time=0.4)
        
        # Root node
        root = create_node(50, UP * 2)
        self.play(
            FadeIn(root.circle, scale=0.5),
            Write(root.label),
            run_time=0.6
        )
        self.wait(0.5)
        
        # Insert 30 (left of 50)
        comparison_label = Text("30 < 50 → Go left", font_size=28, color=accent_cyan)
        comparison_label.next_to(insert_label, DOWN, buff=0.3)
        self.play(FadeIn(comparison_label), run_time=0.4)
        
        self.play(root.circle.animate.set_stroke(accent_cyan, width=6), run_time=0.3)
        self.play(root.circle.animate.set_stroke(light_purple, width=4), run_time=0.3)
        
        node_30 = create_node(30, UP * 0.5 + LEFT * 2)
        edge_50_30 = add_edge(root, node_30)
        
        self.play(
            Create(edge_50_30),
            FadeIn(node_30.circle, scale=0.5),
            Write(node_30.label),
            run_time=0.6
        )
        root.left = node_30
        self.play(FadeOut(comparison_label), run_time=0.3)
        self.wait(0.3)
        
        # Insert 70 (right of 50)
        comparison_label = Text("70 > 50 → Go right", font_size=28, color=accent_cyan)
        comparison_label.next_to(insert_label, DOWN, buff=0.3)
        self.play(FadeIn(comparison_label), run_time=0.4)
        
        self.play(root.circle.animate.set_stroke(accent_cyan, width=6), run_time=0.3)
        self.play(root.circle.animate.set_stroke(light_purple, width=4), run_time=0.3)
        
        node_70 = create_node(70, UP * 0.5 + RIGHT * 2)
        edge_50_70 = add_edge(root, node_70)
        
        self.play(
            Create(edge_50_70),
            FadeIn(node_70.circle, scale=0.5),
            Write(node_70.label),
            run_time=0.6
        )
        root.right = node_70
        self.play(FadeOut(comparison_label), run_time=0.3)
        self.wait(0.3)
        
        # Insert 20 (left of 30)
        comparison_label = Text("20 < 50 → left, 20 < 30 → left", font_size=26, color=accent_cyan)
        comparison_label.next_to(insert_label, DOWN, buff=0.3)
        self.play(FadeIn(comparison_label), run_time=0.4)
        
        self.play(root.circle.animate.set_stroke(accent_cyan, width=6), run_time=0.25)
        self.play(root.circle.animate.set_stroke(light_purple, width=4), run_time=0.25)
        self.play(node_30.circle.animate.set_stroke(accent_cyan, width=6), run_time=0.25)
        self.play(node_30.circle.animate.set_stroke(light_purple, width=4), run_time=0.25)
        
        node_20 = create_node(20, DOWN * 1 + LEFT * 3)
        edge_30_20 = add_edge(node_30, node_20)
        
        self.play(
            Create(edge_30_20),
            FadeIn(node_20.circle, scale=0.5),
            Write(node_20.label),
            run_time=0.6
        )
        node_30.left = node_20
        self.play(FadeOut(comparison_label), run_time=0.3)
        self.wait(0.3)
        
        # Insert 40 (right of 30)
        comparison_label = Text("40 < 50 → left, 40 > 30 → right", font_size=26, color=accent_cyan)
        comparison_label.next_to(insert_label, DOWN, buff=0.3)
        self.play(FadeIn(comparison_label), run_time=0.4)
        
        self.play(root.circle.animate.set_stroke(accent_cyan, width=6), run_time=0.25)
        self.play(root.circle.animate.set_stroke(light_purple, width=4), run_time=0.25)
        self.play(node_30.circle.animate.set_stroke(accent_cyan, width=6), run_time=0.25)
        self.play(node_30.circle.animate.set_stroke(light_purple, width=4), run_time=0.25)
        
        node_40 = create_node(40, DOWN * 1 + LEFT * 1)
        edge_30_40 = add_edge(node_30, node_40)
        
        self.play(
            Create(edge_30_40),
            FadeIn(node_40.circle, scale=0.5),
            Write(node_40.label),
            run_time=0.6
        )
        node_30.right = node_40
        self.play(FadeOut(comparison_label), run_time=0.3)
        self.wait(0.3)
        
        # Insert 60 (left of 70)
        comparison_label = Text("60 > 50 → right, 60 < 70 → left", font_size=26, color=accent_cyan)
        comparison_label.next_to(insert_label, DOWN, buff=0.3)
        self.play(FadeIn(comparison_label), run_time=0.4)
        
        self.play(root.circle.animate.set_stroke(accent_cyan, width=6), run_time=0.25)
        self.play(root.circle.animate.set_stroke(light_purple, width=4), run_time=0.25)
        self.play(node_70.circle.animate.set_stroke(accent_cyan, width=6), run_time=0.25)
        self.play(node_70.circle.animate.set_stroke(light_purple, width=4), run_time=0.25)
        
        node_60 = create_node(60, DOWN * 1 + RIGHT * 1)
        edge_70_60 = add_edge(node_70, node_60)
        
        self.play(
            Create(edge_70_60),
            FadeIn(node_60.circle, scale=0.5),
            Write(node_60.label),
            run_time=0.6
        )
        node_70.left = node_60
        self.play(FadeOut(comparison_label), run_time=0.3)
        self.wait(0.3)
        
        # Insert 80 (right of 70)
        comparison_label = Text("80 > 50 → right, 80 > 70 → right", font_size=26, color=accent_cyan)
        comparison_label.next_to(insert_label, DOWN, buff=0.3)
        self.play(FadeIn(comparison_label), run_time=0.4)
        
        self.play(root.circle.animate.set_stroke(accent_cyan, width=6), run_time=0.25)
        self.play(root.circle.animate.set_stroke(light_purple, width=4), run_time=0.25)
        self.play(node_70.circle.animate.set_stroke(accent_cyan, width=6), run_time=0.25)
        self.play(node_70.circle.animate.set_stroke(light_purple, width=4), run_time=0.25)
        
        node_80 = create_node(80, DOWN * 1 + RIGHT * 3)
        edge_70_80 = add_edge(node_70, node_80)
        
        self.play(
            Create(edge_70_80),
            FadeIn(node_80.circle, scale=0.5),
            Write(node_80.label),
            run_time=0.6
        )
        node_70.right = node_80
        self.play(FadeOut(comparison_label), FadeOut(insert_label), run_time=0.3)
        self.wait(1)
        
        # Search demonstration
        search_label = Text("Searching for 60:", font_size=32, color=GREEN, weight=BOLD)
        search_label.shift(UP * 5.5)
        self.play(FadeIn(search_label), run_time=0.4)
        
        # Search path: 50 -> 70 -> 60
        search_path = [root, node_70, node_60]
        
        for i, node in enumerate(search_path):
            if i == len(search_path) - 1:
                # Found it!
                self.play(
                    node.circle.animate.set_stroke(GREEN, width=6).set_fill(GREEN, opacity=0.3),
                    run_time=0.5
                )
                found_text = Text("Found!", font_size=28, color=GREEN, weight=BOLD)
                found_text.next_to(node.circle, DOWN, buff=0.3)
                self.play(FadeIn(found_text, scale=1.2), run_time=0.4)
                self.wait(1)
                self.play(
                    FadeOut(found_text),
                    node.circle.animate.set_stroke(light_purple, width=4).set_fill(primary_purple, opacity=1),
                    run_time=0.5
                )
            else:
                self.play(node.circle.animate.set_stroke(accent_cyan, width=6), run_time=0.3)
                self.wait(0.2)
                self.play(node.circle.animate.set_stroke(light_purple, width=4), run_time=0.3)
        
        self.play(FadeOut(search_label), run_time=0.3)
        self.wait(0.5)
        
        # Properties
        all_nodes = VGroup(
            root.group, node_30.group, node_70.group,
            node_20.group, node_40.group, node_60.group, node_80.group
        )
        
        self.play(
            all_nodes.animate.shift(UP * 1),
            edges.animate.shift(UP * 1),
            run_time=0.8
        )
        
        props_title = Text("BST Properties:", font_size=36, color=accent_cyan, weight=BOLD)
        props_title.shift(DOWN * 4)
        self.play(FadeIn(props_title), run_time=0.4)
        
        properties = VGroup(
            Text("• Left subtree < Node < Right subtree", font_size=26, color=light_purple),
            Text("• Search: O(log n) average case", font_size=26, color=light_purple),
            Text("• Insert: O(log n) average case", font_size=26, color=light_purple),
            Text("• Used in databases & file systems", font_size=26, color=pink_purple)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        properties.next_to(props_title, DOWN, buff=0.4)
        
        self.play(LaggedStart(*[FadeIn(p, shift=RIGHT * 0.3) for p in properties], lag_ratio=0.3))
        self.wait(3)
        
        # Fade out
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1)
        self.wait(0.5)