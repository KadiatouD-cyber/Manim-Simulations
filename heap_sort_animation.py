from manim import *
import numpy as np

# Configure for vertical Instagram Reels format
config.pixel_height = 1920
config.pixel_width = 1080
config.frame_rate = 60
config.frame_height = 16.0
config.frame_width = 9.0

class HeapSort(Scene):
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
        title = Text("Heap Sort", font_size=60, weight=BOLD, color=light_purple)
        title.shift(UP * 6.5)
        self.add(title)
        
        # Subtitle
        subtitle = Text("Building & Sorting with Binary Heaps", font_size=32, color=accent_cyan)
        subtitle.next_to(title, DOWN, buff=0.3)
        self.play(FadeIn(subtitle))
        self.wait(1)
        self.play(FadeOut(subtitle))
        
        # Array to sort
        array = [12, 11, 13, 5, 6, 7]
        n = len(array)
        
        # Display initial array
        array_label = Text("Initial Array:", font_size=36, color=light_purple)
        array_label.shift(UP * 5)
        
        # Create array visualization
        array_boxes = self.create_array_visual(array, UP * 4, primary_purple)
        
        self.play(FadeIn(array_label))
        self.play(LaggedStart(*[FadeIn(box) for box in array_boxes], lag_ratio=0.1))
        self.wait(1.5)
        
        # Phase 1: Build Max Heap
        phase1_text = Text("Phase 1: Build Max Heap", font_size=40, color=accent_cyan, weight=BOLD)
        phase1_text.shift(UP * 2.5)
        self.play(FadeIn(phase1_text))
        self.wait(1)
        
        # Create tree visualization
        tree = self.create_heap_tree(array, DOWN * 0.5, primary_purple, light_purple)
        self.play(LaggedStart(*[FadeIn(node) for node in tree], lag_ratio=0.08))
        self.wait(1)
        
        # Heapify process
        temp_array = array.copy()
        
        # Build max heap (heapify from last non-leaf node)
        for i in range(n // 2 - 1, -1, -1):
            self.heapify_visual(temp_array, n, i, tree, array_boxes, primary_purple, accent_cyan)
        
        self.play(FadeOut(phase1_text))
        self.wait(0.5)
        
        # Phase 2: Extract elements
        phase2_text = Text("Phase 2: Extract & Sort", font_size=40, color=accent_cyan, weight=BOLD)
        phase2_text.shift(UP * 2.5)
        self.play(FadeIn(phase2_text))
        self.wait(1)
        
        # Extract elements one by one
        node_list = tree.node_list
        
        for i in range(n - 1, 0, -1):
            # Highlight root (max element)
            self.play(node_list[0].animate.set_color(GREEN), run_time=0.3)
            self.play(array_boxes[0].animate.set_color(GREEN), run_time=0.3)
            self.wait(0.3)
            
            # Swap root with last element
            temp_array[0], temp_array[i] = temp_array[i], temp_array[0]
            
            self.play(
                Swap(node_list[0][1], node_list[i][1]),
                Swap(array_boxes[0][1], array_boxes[i][1]),
                run_time=0.6
            )
            
            # Mark sorted element
            self.play(
                node_list[i].animate.set_color(deep_purple),
                array_boxes[i].animate.set_color(deep_purple),
                run_time=0.3
            )
            
            # Update tree and array displays
            node_list[0][1].set_value(temp_array[0])
            node_list[i][1].set_value(temp_array[i])
            array_boxes[0][1].set_value(temp_array[0])
            array_boxes[i][1].set_value(temp_array[i])
            
            # Reset color
            self.play(node_list[0].animate.set_color(primary_purple), run_time=0.2)
            self.play(array_boxes[0].animate.set_color(primary_purple), run_time=0.2)
            
            # Heapify reduced heap
            if i > 1:
                self.heapify_visual(temp_array, i, 0, tree, array_boxes, primary_purple, accent_cyan)
            
            self.wait(0.3)
        
        # Mark first element as sorted
        self.play(
            node_list[0].animate.set_color(deep_purple),
            array_boxes[0].animate.set_color(deep_purple),
            run_time=0.5
        )
        
        self.play(FadeOut(phase2_text))
        self.wait(0.5)
        
        # Show sorted result
        sorted_text = Text("Sorted!", font_size=48, color=GREEN, weight=BOLD)
        sorted_text.shift(UP * 2.5)
        self.play(FadeIn(sorted_text, scale=1.2))
        self.wait(1.5)
        
        # Complexity analysis
        self.play(
            FadeOut(sorted_text),
            FadeOut(tree),
            FadeOut(array_label)
        )
        
        complexity_title = Text("Time Complexity", font_size=44, color=accent_cyan, weight=BOLD)
        complexity_title.shift(UP * 4)
        
        complexity_info = VGroup(
            MathTex(r"\text{Build Heap: } O(n)", font_size=40, color=light_purple),
            MathTex(r"\text{Extract Max: } O(n \log n)", font_size=40, color=light_purple),
            MathTex(r"\text{Total: } O(n \log n)", font_size=48, color=GREEN).set_stroke(width=2)
        ).arrange(DOWN, buff=0.5, aligned_edge=LEFT)
        complexity_info.shift(UP * 1.5)
        
        space_info = MathTex(r"\text{Space: } O(1)", font_size=40, color=accent_cyan)
        space_info.next_to(complexity_info, DOWN, buff=0.8)
        
        self.play(FadeIn(complexity_title))
        self.play(LaggedStart(*[FadeIn(line) for line in complexity_info], lag_ratio=0.3))
        self.play(FadeIn(space_info))
        self.wait(2)
        
        # Clean up for ending
        self.play(
            FadeOut(complexity_title),
            FadeOut(complexity_info),
            FadeOut(space_info),
            FadeOut(array_boxes)
        )
        
        # Key properties
        properties_title = Text("Key Properties", font_size=44, color=accent_cyan, weight=BOLD)
        properties_title.shift(UP * 5)
        
        properties = VGroup(
            Text("✓ In-place sorting", font_size=36, color=light_purple),
            Text("✓ Not stable", font_size=36, color=light_purple),
            Text("✓ Guaranteed O(n log n)", font_size=36, color=light_purple),
            Text("✓ Uses binary heap structure", font_size=36, color=light_purple),
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        properties.shift(UP * 1.5)
        
        self.play(FadeIn(properties_title))
        self.play(LaggedStart(*[FadeIn(prop, shift=RIGHT*0.3) for prop in properties], lag_ratio=0.2))
        self.wait(2.5)
        
        self.play(FadeOut(properties_title), FadeOut(properties), FadeOut(title))
        
        # Follow for more
        follow_text = VGroup(
            Text("Follow for more", font_size=52, color=accent_cyan, weight=BOLD),
            Text("algorithms explained", font_size=36, color=light_purple)
        ).arrange(DOWN, buff=0.4)
        follow_text.shift(UP * 2)
        
        arrow = Arrow(
            follow_text.get_bottom() + DOWN * 0.5,
            follow_text.get_bottom() + DOWN * 2,
            color=accent_cyan,
            stroke_width=10,
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
    
    def create_array_visual(self, array, position, color):
        """Create visual representation of array"""
        boxes = VGroup()
        box_width = 0.8
        
        for i, val in enumerate(array):
            # Box
            square = Square(side_length=box_width, color=color, stroke_width=3)
            # Value
            number = Integer(val, font_size=32, color=WHITE)
            number.move_to(square.get_center())
            
            box_group = VGroup(square, number)
            box_group.shift(RIGHT * (i - len(array)/2 + 0.5) * box_width * 1.2)
            boxes.add(box_group)
        
        boxes.move_to(position)
        return boxes
    
    def create_heap_tree(self, array, position, node_color, text_color):
        """Create binary tree visualization of heap - returns list of nodes only"""
        n = len(array)
        all_objects = VGroup()
        node_list = []  # Keep track of actual nodes separately
        
        # Calculate positions for binary tree
        def get_position(index, level, max_levels):
            h_spacing = 2.5 / (2 ** level)
            level_start = 2 ** level - 1
            pos_in_level = index - level_start
            total_in_level = 2 ** level
            
            x = (pos_in_level - total_in_level/2 + 0.5) * h_spacing * 3
            y = -level * 1.2
            
            return np.array([x, y, 0])
        
        max_levels = int(np.log2(n)) + 1
        
        # First pass: create all nodes and store them
        for i in range(n):
            level = int(np.log2(i + 1))
            pos = get_position(i, level, max_levels)
            
            circle = Circle(radius=0.35, color=node_color, stroke_width=3, fill_opacity=0.2, fill_color=node_color)
            number = Integer(array[i], font_size=28, color=text_color)
            
            node = VGroup(circle, number)
            node.move_to(position + pos)
            node_list.append(node)
        
        # Second pass: create edges
        for i in range(n):
            level = int(np.log2(i + 1))
            left_child = 2 * i + 1
            right_child = 2 * i + 2
            
            if left_child < n:
                edge_left = Line(
                    node_list[i].get_center() + DOWN * 0.35,
                    node_list[left_child].get_center() + UP * 0.35,
                    color=node_color,
                    stroke_width=2
                )
                all_objects.add(edge_left)
            
            if right_child < n:
                edge_right = Line(
                    node_list[i].get_center() + DOWN * 0.35,
                    node_list[right_child].get_center() + UP * 0.35,
                    color=node_color,
                    stroke_width=2
                )
                all_objects.add(edge_right)
        
        # Add all nodes to the group
        for node in node_list:
            all_objects.add(node)
        
        # Store node_list as an attribute for easy access
        all_objects.node_list = node_list
        
        return all_objects
    
    def heapify_visual(self, array, heap_size, root_idx, tree, array_boxes, color, highlight_color):
        """Visualize heapify process"""
        largest = root_idx
        left = 2 * root_idx + 1
        right = 2 * root_idx + 2
        
        # Find largest among root, left, right
        if left < heap_size and array[left] > array[largest]:
            largest = left
        
        if right < heap_size and array[right] > array[largest]:
            largest = right
        
        # If largest is not root, swap and continue heapifying
        if largest != root_idx:
            # Highlight nodes being compared
            node_list = tree.node_list
            
            if root_idx < len(node_list) and largest < len(node_list):
                self.play(
                    node_list[root_idx].animate.set_color(highlight_color),
                    node_list[largest].animate.set_color(highlight_color),
                    run_time=0.2
                )
                self.wait(0.3)
                
                # Swap in array
                array[root_idx], array[largest] = array[largest], array[root_idx]
                
                # Swap visually in tree
                self.play(
                    Swap(node_list[root_idx][1], node_list[largest][1]),
                    run_time=0.5
                )
                
                node_list[root_idx][1].set_value(array[root_idx])
                node_list[largest][1].set_value(array[largest])
                
                # Update array visualization
                if root_idx < len(array_boxes) and largest < len(array_boxes):
                    self.play(
                        Swap(array_boxes[root_idx][1], array_boxes[largest][1]),
                        run_time=0.5
                    )
                    array_boxes[root_idx][1].set_value(array[root_idx])
                    array_boxes[largest][1].set_value(array[largest])
                
                # Reset colors
                self.play(
                    node_list[root_idx].animate.set_color(color),
                    node_list[largest].animate.set_color(color),
                    run_time=0.2
                )
                
                # Recursively heapify the affected subtree
                self.heapify_visual(array, heap_size, largest, tree, array_boxes, color, highlight_color)