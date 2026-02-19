from manim import *
import numpy as np

config.pixel_height = 1920
config.pixel_width = 1080
config.frame_rate = 60
config.frame_height = 16.0
config.frame_width = 9.0

class DragonCurve(Scene):
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
        title = Text("Dragon Curve", font_size=56, weight=BOLD, color=light_purple)
        title.to_edge(UP, buff=1.2)
        self.add(title)
        
        # Subtitle
        subtitle = Text("Fractal paper folding", font_size=32, color=accent_cyan)
        subtitle.next_to(title, DOWN, buff=0.3)
        self.play(FadeIn(subtitle), run_time=0.5)
        self.wait(0.8)
        self.play(FadeOut(subtitle), run_time=0.3)
        
        # === PAPER FOLDING DEMONSTRATION ===
        fold_label = Text("Fold paper in half repeatedly", font_size=32, color=accent_cyan, weight=BOLD)
        fold_label.shift(UP * 5.5)
        self.play(FadeIn(fold_label), run_time=0.4)
        
        # Paper representation
        paper = Rectangle(width=4, height=0.8, color=light_purple, fill_opacity=0.3, stroke_width=3)
        paper.shift(UP * 2)
        
        paper_label = Text("Paper strip", font_size=24, color=GRAY)
        paper_label.next_to(paper, DOWN, buff=0.2)
        
        self.play(Create(paper), Write(paper_label), run_time=0.6)
        self.wait(0.5)
        
        # Fold 1
        fold_text_1 = Text("Fold 1", font_size=28, color=pink_purple, weight=BOLD)
        fold_text_1.next_to(fold_label, DOWN, buff=0.3)
        self.play(FadeIn(fold_text_1), run_time=0.3)
        
        paper_folded_1 = Rectangle(width=2, height=0.8, color=light_purple, fill_opacity=0.5, stroke_width=3)
        paper_folded_1.move_to(paper.get_center())
        
        self.play(
            Transform(paper, paper_folded_1),
            run_time=0.8
        )
        self.wait(0.5)
        
        # Fold 2
        fold_text_2 = Text("Fold 2", font_size=28, color=pink_purple, weight=BOLD)
        fold_text_2.move_to(fold_text_1.get_center())
        self.play(Transform(fold_text_1, fold_text_2), run_time=0.3)
        
        paper_folded_2 = Rectangle(width=1, height=0.8, color=light_purple, fill_opacity=0.7, stroke_width=3)
        paper_folded_2.move_to(paper.get_center())
        
        self.play(
            Transform(paper, paper_folded_2),
            run_time=0.8
        )
        self.wait(0.5)
        
        # Fold 3
        fold_text_3 = Text("Fold 3", font_size=28, color=pink_purple, weight=BOLD)
        fold_text_3.move_to(fold_text_1.get_center())
        self.play(Transform(fold_text_1, fold_text_3), run_time=0.3)
        
        paper_folded_3 = Rectangle(width=0.5, height=0.8, color=light_purple, fill_opacity=0.9, stroke_width=3)
        paper_folded_3.move_to(paper.get_center())
        
        self.play(
            Transform(paper, paper_folded_3),
            run_time=0.8
        )
        self.wait(0.8)
        
        # Unfold
        unfold_label = Text("Unfold and open at 90° angles", font_size=28, color=GREEN, weight=BOLD)
        unfold_label.move_to(fold_text_1.get_center())
        self.play(
            FadeOut(fold_text_1),
            FadeIn(unfold_label),
            run_time=0.4
        )
        
        self.play(
            FadeOut(paper),
            FadeOut(paper_label),
            FadeOut(fold_label),
            run_time=0.5
        )
        self.wait(0.3)
        
        # === DRAGON CURVE GENERATION ===
        curve_label = Text("The pattern that emerges:", font_size=32, color=accent_cyan, weight=BOLD)
        curve_label.shift(UP * 5.5)
        self.play(
            Transform(unfold_label, curve_label),
            run_time=0.5
        )
        self.wait(0.3)
        
        # Generate dragon curve using L-system
        def generate_dragon_sequence(iterations):
            """Generate dragon curve L-system sequence"""
            sequence = "F"
            for _ in range(iterations):
                new_sequence = ""
                for char in sequence:
                    if char == "F":
                        new_sequence += "F+G"
                    elif char == "G":
                        new_sequence += "F-G"
                    else:
                        new_sequence += char
                sequence = new_sequence
            return sequence
        
        def draw_dragon_curve(sequence, start_point, step_size, angle=90):
            """Convert sequence to points"""
            points = [start_point]
            current_pos = np.array(start_point)
            current_angle = 0  # Start facing right
            
            for char in sequence:
                if char == "F" or char == "G":
                    # Move forward
                    direction = np.array([
                        np.cos(current_angle * DEGREES),
                        np.sin(current_angle * DEGREES),
                        0
                    ])
                    current_pos = current_pos + direction * step_size
                    points.append(current_pos.copy())
                elif char == "+":
                    # Turn left
                    current_angle += angle
                elif char == "-":
                    # Turn right
                    current_angle -= angle
            
            return points
        
        # Iterate through levels
        max_iterations = 12
        
        for iteration in range(1, max_iterations + 1):
            # Generate sequence
            sequence = generate_dragon_sequence(iteration)
            
            # Calculate step size to fit in frame
            step_size = 3.5 / (2 ** (iteration / 2))
            
            # Generate points
            points = draw_dragon_curve(sequence, np.array([0, 0, 0]), step_size)
            
            # Create path
            if iteration == 1:
                # First iteration - simple line
                dragon_path = VMobject(stroke_width=4)
                dragon_path.set_points_as_corners(points)
                dragon_path.set_color(accent_cyan)
                dragon_path.shift(UP * 0.5)
                
                iter_label = Text(f"Iteration {iteration}", font_size=28, color=pink_purple, weight=BOLD)
                iter_label.next_to(unfold_label, DOWN, buff=0.3)
                
                self.play(
                    Create(dragon_path),
                    FadeIn(iter_label),
                    run_time=1
                )
                self.wait(0.5)
            else:
                # Subsequent iterations - transform
                new_dragon_path = VMobject(stroke_width=max(4 - iteration * 0.2, 1.5))
                new_dragon_path.set_points_as_corners(points)
                
                # Color gradient based on iteration
                colors = [accent_cyan, primary_purple, pink_purple, light_purple]
                color_index = iteration % len(colors)
                new_dragon_path.set_color(colors[color_index])
                new_dragon_path.shift(UP * 0.5)
                
                new_iter_label = Text(f"Iteration {iteration}", font_size=28, color=pink_purple, weight=BOLD)
                new_iter_label.move_to(iter_label.get_center())
                
                if iteration <= 8:
                    # Smooth transformation for lower iterations
                    self.play(
                        Transform(dragon_path, new_dragon_path),
                        Transform(iter_label, new_iter_label),
                        run_time=0.8
                    )
                    self.wait(0.3)
                else:
                    # Faster for higher iterations
                    self.play(
                        Transform(dragon_path, new_dragon_path),
                        Transform(iter_label, new_iter_label),
                        run_time=0.5
                    )
                    self.wait(0.2)
        
        # Final pause on complete dragon
        self.wait(2)
        
        # Clean up for properties
        self.play(
            FadeOut(dragon_path),
            FadeOut(iter_label),
            FadeOut(unfold_label),
            run_time=0.6
        )
        
        # === PROPERTIES ===
        props_title = Text("Dragon Curve Properties:", font_size=36, color=accent_cyan, weight=BOLD)
        props_title.shift(UP * 4.5)
        self.play(FadeIn(props_title), run_time=0.4)
        
        properties = VGroup(
            Text("• Self-similar fractal structure", font_size=28, color=light_purple),
            Text("• Never crosses itself", font_size=28, color=light_purple),
            Text("• Created by folding paper", font_size=28, color=light_purple),
            Text("• Each fold doubles the complexity", font_size=28, color=light_purple),
            Text("• Discovered by physicists in 1960s", font_size=28, color=pink_purple)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        properties.shift(UP * 1)
        
        self.play(LaggedStart(*[FadeIn(p, shift=RIGHT * 0.3) for p in properties], lag_ratio=0.3))
        self.wait(3)
        
        self.play(FadeOut(properties), FadeOut(props_title), run_time=0.5)
        
        # === FINAL SHOWCASE - Large Dragon ===
        showcase_label = Text("Final Form (12 iterations)", font_size=36, color=accent_cyan, weight=BOLD)
        showcase_label.shift(UP * 5.5)
        self.play(FadeIn(showcase_label), run_time=0.4)
        
        # Generate final dragon
        final_sequence = generate_dragon_sequence(12)
        final_step_size = 3.5 / (2 ** 6)
        final_points = draw_dragon_curve(final_sequence, np.array([0, 0, 0]), final_step_size)
        
        final_dragon = VMobject(stroke_width=2)
        final_dragon.set_points_as_corners(final_points)
        final_dragon.set_color_by_gradient(accent_cyan, primary_purple, pink_purple, light_purple)
        final_dragon.shift(UP * 0.3)
        
        self.play(Create(final_dragon), run_time=3, rate_func=linear)
        self.wait(2)
        
        # Rotate for dramatic effect
        self.play(
            Rotate(final_dragon, angle=2*PI, about_point=final_dragon.get_center()),
            run_time=3,
            rate_func=smooth
        )
        self.wait(1)
        
        # Fade out
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1)
        self.wait(0.5)