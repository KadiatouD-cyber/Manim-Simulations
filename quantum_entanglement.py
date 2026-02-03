from manim import *
import numpy as np

config.pixel_height = 1920
config.pixel_width = 1080
config.frame_rate = 60
config.frame_height = 16.0
config.frame_width = 9.0

class QuantumEntanglement(Scene):
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
        title = Text("Quantum Entanglement", font_size=52, weight=BOLD, color=light_purple)
        title.to_edge(UP, buff=1.2)
        self.add(title)
        
        # Subtitle with Einstein quote
        subtitle = Text('"Spooky action at a distance"', font_size=30, color=accent_cyan, slant=ITALIC)
        subtitle.next_to(title, DOWN, buff=0.3)
        einstein = Text("- Albert Einstein", font_size=24, color=GRAY, slant=ITALIC)
        einstein.next_to(subtitle, DOWN, buff=0.2)
        
        self.play(FadeIn(subtitle), FadeIn(einstein))
        self.wait(2)
        self.play(FadeOut(subtitle), FadeOut(einstein))
        
        # Introduction
        intro = VGroup(
            Text("Two particles become connected", font_size=28, color=GRAY),
            Text("Measure one → instantly affects the other", font_size=28, color=light_purple),
            Text("No matter how far apart they are", font_size=28, color=accent_cyan, weight=BOLD)
        ).arrange(DOWN, buff=0.3)
        intro.shift(UP * 4.5)
        self.play(FadeIn(intro))
        self.wait(3)
        self.play(FadeOut(intro))
        
        # Create particle source in the center
        source = Circle(radius=0.3, color=YELLOW, fill_opacity=0.8, stroke_width=4)
        source.shift(UP * 1)
        
        source_label = Text("Entangled\nPair Source", font_size=24, color=YELLOW)
        source_label.next_to(source, DOWN, buff=0.3)
        
        self.play(FadeIn(source), FadeIn(source_label))
        self.wait(0.5)
        
        # Create two particles (initially together)
        particle_radius = 0.15
        
        particle_A = Circle(
            radius=particle_radius,
            color=RED,
            fill_opacity=1,
            stroke_width=3
        ).move_to(source.get_center())
        
        particle_B = Circle(
            radius=particle_radius,
            color=BLUE,
            fill_opacity=1,
            stroke_width=3
        ).move_to(source.get_center())
        
        # Particle labels
        label_A = Text("A", font_size=24, color=RED, weight=BOLD).move_to(particle_A.get_center())
        label_B = Text("B", font_size=24, color=BLUE, weight=BOLD).move_to(particle_B.get_center())
        
        # Glow effect for particles
        glow_A = Circle(radius=particle_radius * 1.5, color=RED, stroke_opacity=0.5, stroke_width=2)
        glow_A.move_to(particle_A.get_center())
        glow_B = Circle(radius=particle_radius * 1.5, color=BLUE, stroke_opacity=0.5, stroke_width=2)
        glow_B.move_to(particle_B.get_center())
        
        # Create particles with animation
        self.play(
            FadeIn(particle_A),
            FadeIn(particle_B),
            FadeIn(glow_A),
            FadeIn(glow_B),
            FadeIn(label_A),
            FadeIn(label_B)
        )
        self.wait(0.5)
        
        # Entanglement link (wavy line between particles)
        def create_entanglement_link(p1, p2, color=accent_cyan):
            start = p1.get_center()
            end = p2.get_center()
            
            # Create wavy line
            path = VMobject(stroke_color=color, stroke_width=3)
            points = []
            n_points = 30
            for i in range(n_points):
                t = i / (n_points - 1)
                base_point = start + (end - start) * t
                # Add wave perpendicular to line
                direction = end - start
                perp = np.array([-direction[1], direction[0], 0])
                if np.linalg.norm(perp) > 0:
                    perp = perp / np.linalg.norm(perp)
                wave_offset = perp * 0.15 * np.sin(t * 4 * PI)
                points.append(base_point + wave_offset)
            
            path.set_points_as_corners(points)
            return path
        
        entanglement_link = always_redraw(
            lambda: create_entanglement_link(particle_A, particle_B)
        )
        
        self.add(entanglement_link)
        self.wait(0.5)
        
        # Separate the particles
        final_pos_A = LEFT * 3 + UP * 1
        final_pos_B = RIGHT * 3 + UP * 1
        
        separation_text = Text("Particles separate", font_size=28, color=light_purple)
        separation_text.shift(UP * 4)
        self.play(FadeIn(separation_text))
        
        self.play(
            particle_A.animate.move_to(final_pos_A),
            particle_B.animate.move_to(final_pos_B),
            glow_A.animate.move_to(final_pos_A),
            glow_B.animate.move_to(final_pos_B),
            label_A.animate.move_to(final_pos_A),
            label_B.animate.move_to(final_pos_B),
            FadeOut(source),
            FadeOut(source_label),
            run_time=2
        )
        
        # Add "still connected" text
        still_connected = Text("But still connected!", font_size=28, color=accent_cyan, weight=BOLD)
        still_connected.next_to(separation_text, DOWN, buff=0.3)
        self.play(FadeIn(still_connected))
        self.wait(1.5)
        self.play(FadeOut(separation_text), FadeOut(still_connected))
        
        # Show quantum states (superposition)
        # Particle A superposition
        superposition_A = VGroup(
            Text("?", font_size=48, color=RED, weight=BOLD),
            MathTex(r"\frac{1}{\sqrt{2}}(\uparrow + \downarrow)", font_size=24, color=RED)
        ).arrange(DOWN, buff=0.2)
        superposition_A.next_to(particle_A, UP, buff=0.5)
        
        # Particle B superposition
        superposition_B = VGroup(
            Text("?", font_size=48, color=BLUE, weight=BOLD),
            MathTex(r"\frac{1}{\sqrt{2}}(\uparrow + \downarrow)", font_size=24, color=BLUE)
        ).arrange(DOWN, buff=0.2)
        superposition_B.next_to(particle_B, UP, buff=0.5)
        
        superposition_label = Text("Both in superposition (↑ and ↓)", font_size=28, color=light_purple)
        superposition_label.shift(UP * 4)
        
        self.play(FadeIn(superposition_label))
        self.play(FadeIn(superposition_A), FadeIn(superposition_B))
        self.wait(2)
        self.play(FadeOut(superposition_label))
        
        # Create measurement apparatus for particle A
        detector_A = VGroup(
            Rectangle(width=1.2, height=1.5, color=RED, stroke_width=4, fill_opacity=0.2),
            Text("Detector", font_size=20, color=RED)
        ).arrange(DOWN, buff=0.1)
        detector_A.next_to(particle_A, DOWN, buff=0.8)  # Changed to DOWN instead of LEFT
        
        measure_text = Text("Measure particle A", font_size=32, color=accent_cyan, weight=BOLD)
        measure_text.shift(UP * 4)
        
        self.play(FadeIn(measure_text))
        self.play(FadeIn(detector_A))
        
        # Move particle A into detector
        self.play(
            particle_A.animate.move_to(detector_A[0].get_center()),
            glow_A.animate.move_to(detector_A[0].get_center()),
            label_A.animate.move_to(detector_A[0].get_center()),
            run_time=1.5
        )
        
        # Measurement flash
        flash = Circle(radius=0.5, color=YELLOW, fill_opacity=0.5).move_to(detector_A[0].get_center())
        self.play(
            FadeIn(flash, scale=0.5),
            FadeOut(flash, scale=2),
            run_time=0.5
        )
        
        # Collapse to definite state (let's say spin up)
        result_A = VGroup(
            MathTex(r"\uparrow", font_size=72, color=RED),
            Text("Spin UP", font_size=24, color=RED)
        ).arrange(DOWN, buff=0.2)
        result_A.move_to(superposition_A.get_center())
        
        self.play(
            FadeOut(superposition_A),
            FadeIn(result_A)
        )
        self.wait(1)
        
        # Instant effect on particle B
        instant_text = Text("Particle B instantly becomes:", font_size=28, color=accent_cyan, weight=BOLD)
        instant_text.shift(UP * 4)
        
        self.play(Transform(measure_text, instant_text))
        
        # Highlight the entanglement link
        self.play(
            entanglement_link.animate.set_stroke(width=6, color=YELLOW),
            rate_func=there_and_back,
            run_time=1
        )
        
        # Particle B collapses to opposite state (spin down)
        result_B = VGroup(
            MathTex(r"\downarrow", font_size=72, color=BLUE),
            Text("Spin DOWN", font_size=24, color=BLUE)
        ).arrange(DOWN, buff=0.2)
        result_B.move_to(superposition_B.get_center())
        
        self.play(
            FadeOut(superposition_B),
            FadeIn(result_B),
            particle_B.animate.set_fill(BLUE, opacity=1),
            glow_B.animate.set_stroke(BLUE, opacity=1),
            run_time=0.3  # Instantaneous!
        )
        self.wait(1.5)
        
        # Correlation explanation
        correlation_text = Text("Always opposite! 100% correlated", font_size=32, color=accent_cyan, weight=BOLD)
        correlation_text.shift(UP * 4)
        self.play(Transform(measure_text, correlation_text))
        self.wait(2)
        
        # Clean up for explanation
        self.play(
            FadeOut(particle_A),
            FadeOut(particle_B),
            FadeOut(glow_A),
            FadeOut(glow_B),
            FadeOut(label_A),
            FadeOut(label_B),
            FadeOut(detector_A),
            FadeOut(result_A),
            FadeOut(result_B),
            FadeOut(entanglement_link),
            FadeOut(measure_text)
        )
        
        # Key points
        key_points_title = Text("Why It's Bizarre:", font_size=40, color=accent_cyan, weight=BOLD)
        key_points_title.shift(UP * 5)
        
        key_points = VGroup(
            Text("1. Faster than light?", font_size=32, color=light_purple),
            Text("   Information appears to travel instantly", font_size=26, color=GRAY),
            Text("2. No hidden variables", font_size=32, color=light_purple),
            Text("   States truly don't exist until measured", font_size=26, color=GRAY),
            Text("3. Non-local correlation", font_size=32, color=light_purple),
            Text("   Connection transcends space", font_size=26, color=GRAY)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.3)
        key_points.shift(UP * 1)
        
        self.play(FadeIn(key_points_title))
        self.play(LaggedStart(*[FadeIn(point, shift=RIGHT*0.5) for point in key_points], lag_ratio=0.3))
        self.wait(4)
        
        self.play(FadeOut(key_points), FadeOut(key_points_title))
        
        # Einstein's objection
        einstein_section = VGroup(
            Text("Einstein hated this idea", font_size=36, color=accent_cyan, weight=BOLD),
            Text('Called it "spooky action at a distance"', font_size=28, color=GRAY, slant=ITALIC),
            Text("Thought quantum mechanics was incomplete", font_size=28, color=GRAY)
        ).arrange(DOWN, buff=0.4)
        einstein_section.shift(UP * 2)
        
        self.play(FadeIn(einstein_section))
        self.wait(3)
        self.play(FadeOut(einstein_section))
        
        # But experiments proved it
        experiments = VGroup(
            Text("But experiments proved it real:", font_size=36, color=accent_cyan, weight=BOLD),
            Text("• Bell's Theorem (1964)", font_size=28, color=light_purple),
            Text("• Aspect Experiments (1982)", font_size=28, color=light_purple),
            Text("• Nobel Prize 2022", font_size=28, color=light_purple),
            Text("• Now used in quantum computing", font_size=28, color=pink_purple)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.4)
        experiments.shift(UP * 1.5)
        
        self.play(FadeIn(experiments[0]))
        self.play(LaggedStart(*[FadeIn(exp, shift=RIGHT*0.5) for exp in experiments[1:]], lag_ratio=0.4))
        self.wait(3)
        
        self.play(FadeOut(experiments))
        
        # Real applications
        applications_title = Text("Real Applications:", font_size=40, color=accent_cyan, weight=BOLD)
        applications_title.shift(UP * 5)
        
        applications = VGroup(
            Text("🔐 Quantum Cryptography", font_size=34, color=light_purple),
            Text("   Unhackable communication", font_size=26, color=GRAY),
            Text("💻 Quantum Computing", font_size=34, color=light_purple),
            Text("   Entangled qubits for computation", font_size=26, color=GRAY),
            Text("📡 Quantum Teleportation", font_size=34, color=light_purple),
            Text("   Transfer quantum states instantly", font_size=26, color=GRAY)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.35)
        applications.shift(UP * 0.5)
        
        self.play(FadeIn(applications_title))
        self.play(LaggedStart(*[FadeIn(app, shift=RIGHT*0.5) for app in applications], lag_ratio=0.3))
        self.wait(4)
        
        self.play(FadeOut(applications), FadeOut(applications_title))
        
        # Mind-blowing fact
        mind_blow = VGroup(
            Text("The Universe is Non-Local", font_size=42, color=accent_cyan, weight=BOLD),
            Text("Distant parts can be instantly connected", font_size=30, color=light_purple),
            Text("Space doesn't separate everything", font_size=30, color=pink_purple)
        ).arrange(DOWN, buff=0.5)
        mind_blow.shift(UP * 1.5)
        
        self.play(FadeIn(mind_blow, scale=1.2))
        self.wait(3)
        self.play(FadeOut(mind_blow))
        
        # Follow for more
        follow_text = VGroup(
            Text("Follow for more", font_size=48, color=accent_cyan, weight=BOLD),
            Text("quantum physics explained", font_size=32, color=light_purple)
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