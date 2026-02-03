from manim import *
import numpy as np

config.pixel_height = 1920
config.pixel_width = 1080
config.frame_rate = 60
config.frame_height = 16.0
config.frame_width = 9.0

class StandingWaves(Scene):
    def construct(self):
        # Purple color scheme to match TechFlux branding
        primary_purple = "#9D4EDD"
        light_purple = "#C77DFF"
        pink_purple = "#E0AAFF"
        deep_purple = "#7B2CBF"
        accent_cyan = "#00D9FF"
        
        # Add TechFlux branding
        techflux = Text("TechFlux", font_size=44, weight=BOLD, color=primary_purple)
        techflux.to_corner(DR, buff=0.5)
        self.add(techflux)
        
        # Title
        title = Text("Standing Waves", font_size=56, weight=BOLD, color=light_purple)
        title.to_edge(UP, buff=1.2)
        self.add(title)
        
        # Subtitle
        subtitle = Text("The physics behind every musical note", font_size=30, color=accent_cyan)
        subtitle.next_to(title, DOWN, buff=0.3)
        self.play(FadeIn(subtitle))
        self.wait(1.5)
        self.play(FadeOut(subtitle))
        
        # Introduction
        intro = VGroup(
            Text("When waves reflect and interfere,", font_size=28, color=GRAY),
            Text("they create patterns that don't move", font_size=28, color=light_purple)
        ).arrange(DOWN, buff=0.3)
        intro.shift(UP * 5)
        self.play(FadeIn(intro))
        self.wait(2)
        self.play(FadeOut(intro))
        
        # String endpoints (fixed)
        string_length = 6
        left_end = LEFT * string_length/2 + UP * 1
        right_end = RIGHT * string_length/2 + UP * 1
        
        # Draw string endpoints (nodes that never move)
        left_anchor = Dot(left_end, color=deep_purple, radius=0.1)
        right_anchor = Dot(right_end, color=deep_purple, radius=0.1)
        
        # Base line (equilibrium)
        base_line = Line(left_end, right_end, color=deep_purple, stroke_width=2, stroke_opacity=0.3)
        
        self.play(FadeIn(left_anchor), FadeIn(right_anchor), Create(base_line))
        
        # Function to create standing wave
        def create_standing_wave(n, amplitude, phase, num_points=200):
            """Create standing wave for harmonic n"""
            points = []
            for i in range(num_points):
                x = i / (num_points - 1) * string_length - string_length/2
                # Standing wave: A * sin(n*pi*x/L) * cos(omega*t)
                y = amplitude * np.sin(n * np.pi * (x + string_length/2) / string_length) * np.cos(phase)
                points.append(left_end + RIGHT * (x + string_length/2) + UP * y)
            return points
        
        # Harmonics to show
        harmonics_data = [
            (1, "Fundamental (n=1)", "440 Hz - A note"),
            (2, "2nd Harmonic (n=2)", "880 Hz - A (octave higher)"),
            (3, "3rd Harmonic (n=3)", "1320 Hz"),
            (4, "4th Harmonic (n=4)", "1760 Hz"),
            (5, "5th Harmonic (n=5)", "2200 Hz")
        ]
        
        for n, harmonic_name, frequency in harmonics_data:
            # Harmonic label
            harmonic_label = VGroup(
                Text(harmonic_name, font_size=36, color=accent_cyan, weight=BOLD),
                Text(frequency, font_size=28, color=light_purple)
            ).arrange(DOWN, buff=0.2)
            harmonic_label.shift(UP * 4.5)
            
            self.play(FadeIn(harmonic_label))
            
            # Create the wave
            wave = VMobject(stroke_color=pink_purple, stroke_width=5)
            initial_points = create_standing_wave(n, 0.8, 0)
            wave.set_points_as_corners(initial_points)
            
            # Nodes and antinodes markers
            nodes = VGroup()
            antinodes = VGroup()
            
            # Nodes (points that don't move)
            for i in range(n + 1):
                node_x = i * string_length / n
                node_pos = left_end + RIGHT * node_x
                node_dot = Dot(node_pos, color=RED, radius=0.08)
                nodes.add(node_dot)
            
            # Antinodes (points of maximum displacement)
            for i in range(n):
                antinode_x = (i + 0.5) * string_length / n
                antinode_pos = left_end + RIGHT * antinode_x
                antinode_marker = Dot(antinode_pos, color=GREEN, radius=0.08)
                antinodes.add(antinode_marker)
            
            # Node/Antinode labels
            node_label = VGroup(
                Dot(color=RED, radius=0.08),
                Text("Nodes", font_size=24, color=RED)
            ).arrange(RIGHT, buff=0.3)
            node_label.to_edge(LEFT, buff=0.5).shift(DOWN * 3)
            
            antinode_label = VGroup(
                Dot(color=GREEN, radius=0.08),
                Text("Antinodes", font_size=24, color=GREEN)
            ).arrange(RIGHT, buff=0.3)
            antinode_label.next_to(node_label, DOWN, buff=0.3, aligned_edge=LEFT)
            
            # Show static wave first
            self.play(Create(wave))
            self.wait(0.5)
            
            # Show nodes and antinodes
            self.play(FadeIn(nodes), FadeIn(antinodes))
            if n == 1:
                self.play(FadeIn(node_label), FadeIn(antinode_label))
            self.wait(0.5)
            
            # Animate the standing wave oscillation
            def update_wave(mob, dt):
                if not hasattr(update_wave, 'time'):
                    update_wave.time = 0
                update_wave.time += dt
                
                omega = 4  # Angular frequency
                phase = omega * update_wave.time
                new_points = create_standing_wave(n, 0.8, phase)
                mob.set_points_as_corners(new_points)
            
            wave.add_updater(update_wave)
            
            # Oscillate for a few seconds
            self.wait(4)
            
            wave.remove_updater(update_wave)
            update_wave.time = 0  # Reset for next harmonic
            
            # Clean up for next harmonic
            self.play(
                FadeOut(wave),
                FadeOut(nodes),
                FadeOut(antinodes),
                FadeOut(harmonic_label)
            )
            
            if n == 1:
                self.play(FadeOut(node_label), FadeOut(antinode_label))
        
        # Clear the base setup
        self.play(FadeOut(left_anchor), FadeOut(right_anchor), FadeOut(base_line))
        
        # Show wavelength relationship
        wavelength_title = Text("Wavelength Relationship", font_size=40, color=accent_cyan, weight=BOLD)
        wavelength_title.shift(UP * 4)
        
        wavelength_formulas = VGroup(
            MathTex(r"L = \frac{n\lambda}{2}", font_size=48, color=light_purple),
            MathTex(r"\lambda_n = \frac{2L}{n}", font_size=40, color=pink_purple),
            Text("where L = string length, n = harmonic number", font_size=24, color=GRAY)
        ).arrange(DOWN, buff=0.5)
        wavelength_formulas.shift(UP * 1.5)
        
        self.play(FadeIn(wavelength_title))
        self.play(Write(wavelength_formulas))
        self.wait(2)
        
        self.play(FadeOut(wavelength_title), FadeOut(wavelength_formulas))
        
        # Frequency relationship
        freq_title = Text("Frequency Relationship", font_size=40, color=accent_cyan, weight=BOLD)
        freq_title.shift(UP * 4)
        
        freq_formulas = VGroup(
            MathTex(r"f_n = n \cdot f_1", font_size=48, color=light_purple),
            MathTex(r"f_n = \frac{nv}{2L}", font_size=40, color=pink_purple),
            Text("Higher harmonics = higher frequencies", font_size=28, color=GRAY)
        ).arrange(DOWN, buff=0.5)
        freq_formulas.shift(UP * 1)
        
        self.play(FadeIn(freq_title))
        self.play(Write(freq_formulas))
        self.wait(2)
        
        self.play(FadeOut(freq_title), FadeOut(freq_formulas))
        
        # Musical instruments examples
        instruments_title = Text("Real-World Applications", font_size=40, color=accent_cyan, weight=BOLD)
        instruments_title.shift(UP * 5)
        
        instruments = VGroup(
            Text("Guitar strings", font_size=34, color=light_purple),
            Text("Piano strings", font_size=34, color=light_purple),
            Text("Violin strings", font_size=34, color=light_purple),
            Text("Brass instruments (air columns)", font_size=34, color=light_purple),
            Text("Vocal cords", font_size=34, color=light_purple),
            Text("Radio antennas", font_size=34, color=light_purple)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        instruments.next_to(instruments_title, DOWN, buff=0.8)
        
        self.play(FadeIn(instruments_title))
        self.play(LaggedStart(*[FadeIn(inst, shift=RIGHT*0.5) for inst in instruments], lag_ratio=0.2))
        self.wait(3)
        
        self.play(FadeOut(instruments), FadeOut(instruments_title))
        
        # Superposition - combining harmonics
        superposition_title = Text("Timbre: Combining Harmonics", font_size=38, color=accent_cyan, weight=BOLD)
        superposition_title.shift(UP * 5)
        
        superposition_text = VGroup(
            Text("Every instrument plays the same note", font_size=28, color=GRAY),
            Text("but sounds different because of", font_size=28, color=GRAY),
            Text("the mix of harmonics present", font_size=32, color=light_purple, weight=BOLD)
        ).arrange(DOWN, buff=0.3)
        superposition_text.shift(UP * 2.5)
        
        self.play(FadeIn(superposition_title))
        self.play(FadeIn(superposition_text))
        self.wait(2)
        
        # Show superposition of multiple harmonics
        left_end_super = LEFT * string_length/2 + DOWN * 0.5
        right_end_super = RIGHT * string_length/2 + DOWN * 0.5
        
        left_anchor_super = Dot(left_end_super, color=deep_purple, radius=0.08)
        right_anchor_super = Dot(right_end_super, color=deep_purple, radius=0.08)
        base_line_super = Line(left_end_super, right_end_super, color=deep_purple, stroke_width=2, stroke_opacity=0.3)
        
        self.play(FadeIn(left_anchor_super), FadeIn(right_anchor_super), Create(base_line_super))
        
        # Create combined wave (fundamental + harmonics)
        def create_complex_wave(amplitudes, phase, num_points=200):
            """Combine multiple harmonics"""
            points = []
            for i in range(num_points):
                x = i / (num_points - 1) * string_length - string_length/2
                y = 0
                for n, amp in enumerate(amplitudes, 1):
                    y += amp * np.sin(n * np.pi * (x + string_length/2) / string_length) * np.cos(n * phase)
                points.append(left_end_super + RIGHT * (x + string_length/2) + UP * y)
            return points
        
        # Example: guitar-like timbre (strong fundamental, weaker harmonics)
        complex_wave = VMobject(stroke_color=accent_cyan, stroke_width=5)
        amplitudes = [0.6, 0.3, 0.2, 0.1, 0.05]  # Decreasing amplitude for higher harmonics
        
        initial_complex = create_complex_wave(amplitudes, 0)
        complex_wave.set_points_as_corners(initial_complex)
        
        complex_label = Text("Combined harmonics = unique sound", font_size=28, color=accent_cyan)
        complex_label.next_to(complex_wave, DOWN, buff=1)
        
        self.play(Create(complex_wave), FadeIn(complex_label))
        
        # Animate complex wave
        def update_complex_wave(mob, dt):
            if not hasattr(update_complex_wave, 'time'):
                update_complex_wave.time = 0
            update_complex_wave.time += dt
            
            omega = 3
            phase = omega * update_complex_wave.time
            new_points = create_complex_wave(amplitudes, phase)
            mob.set_points_as_corners(new_points)
        
        complex_wave.add_updater(update_complex_wave)
        self.wait(4)
        complex_wave.remove_updater(update_complex_wave)
        
        self.play(
            FadeOut(complex_wave),
            FadeOut(complex_label),
            FadeOut(left_anchor_super),
            FadeOut(right_anchor_super),
            FadeOut(base_line_super),
            FadeOut(superposition_title),
            FadeOut(superposition_text)
        )
        
        # Key insight
        insight = VGroup(
            Text("Standing waves are everywhere:", font_size=36, color=accent_cyan, weight=BOLD),
            Text("Music, acoustics, optics, quantum mechanics", font_size=28, color=light_purple)
        ).arrange(DOWN, buff=0.4)
        insight.shift(UP * 1.5)
        
        self.play(FadeIn(insight))
        self.wait(2)
        self.play(FadeOut(insight))
        
        # Follow for more
        follow_text = VGroup(
            Text("Follow TechFlux for more", font_size=48, color=accent_cyan, weight=BOLD),
            Text("physics visualizations", font_size=32, color=light_purple)
        ).arrange(DOWN, buff=0.4)
        follow_text.shift(UP * 1)
        
        arrow = Arrow(
            follow_text.get_bottom() + DOWN * 0.5,
            follow_text.get_bottom() + DOWN * 1.5,
            color=accent_cyan,
            stroke_width=8,
            max_tip_length_to_length_ratio=0.3
        )
        
        self.play(
            FadeIn(follow_text, scale=1.2),
            GrowArrow(arrow)
        )
        
        self.play(
            follow_text.animate.scale(1.1),
            arrow.animate.shift(DOWN * 0.2),
            rate_func=there_and_back,
            run_time=0.8
        )
        
        self.wait(2)
        
        # Fade out
        self.play(
            FadeOut(follow_text),
            FadeOut(arrow),
            FadeOut(title),
            FadeOut(techflux)
        )
        self.wait(0.5)