from manim import *
import numpy as np

# Configure for vertical Instagram Reels format
config.pixel_height = 1920
config.pixel_width = 1080
config.frame_rate = 60
config.frame_height = 16.0
config.frame_width = 9.0

class PIDControl(Scene):
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
        title = Text("PID Control", font_size=56, weight=BOLD, color=light_purple)
        title.shift(UP * 6.8)
        self.add(title)
        
        # Subtitle
        subtitle = Text("Proportional-Integral-Derivative", font_size=28, color=accent_cyan)
        subtitle.next_to(title, DOWN, buff=0.25)
        self.play(FadeIn(subtitle))
        self.wait(1)
        self.play(FadeOut(subtitle))
        
        # Main PID equation - smaller
        equation = MathTex(
            r"u(t) = K_p e(t) + K_i \int_0^t e(\tau)d\tau + K_d \frac{de(t)}{dt}",
            font_size=32,
            color=light_purple
        ).shift(UP * 6)
        
        self.play(Write(equation))
        self.wait(1)
        
        # Visual representation setup - higher up
        track_y = UP * 4.5
        
        # Track line - shorter
        track = Line(LEFT * 3, RIGHT * 3, color=primary_purple, stroke_width=3)
        track.move_to(track_y)
        
        # Target (red hexagon) - smaller and AT the end of track
        target = RegularPolygon(n=6, color=RED, fill_opacity=0.3, stroke_width=3)
        target.scale(0.3)
        target_pos = RIGHT * 3  # At the end of the track
        target.move_to(track_y + target_pos)
        
        # Current position (blue circle) - smaller, starts at left
        current = Circle(radius=0.28, color=accent_cyan, fill_opacity=0.6, stroke_width=3)
        current_pos = LEFT * 3  # Start at left end
        current.move_to(track_y + current_pos)
        
        # Trail dots - smaller
        trail_dots = VGroup()
        for i in range(5):
            dot = Dot(radius=0.06, color=accent_cyan, fill_opacity=0.5 - i*0.08)
            dot.move_to(track_y + LEFT * 3 - RIGHT * i * 0.25)
            trail_dots.add(dot)
        
        # Error label - moved up and to the side
        error_label = Text("ERROR:", font_size=28, color=primary_purple, weight=BOLD)
        error_label.shift(UP * 3.8 + RIGHT * 1.8)
        
        error_value = DecimalNumber(
            6.0, num_decimal_places=2, font_size=32, color=RED
        )
        error_value.next_to(error_label, RIGHT, buff=0.2)
        
        self.play(
            Create(track),
            FadeIn(target),
            FadeIn(current),
            FadeIn(trail_dots)
        )
        self.play(FadeIn(error_label), FadeIn(error_value))
        self.wait(0.5)
        
        # Component displays - increased spacing to prevent overlaps
        
        # Proportional - at top
        p_label = Text("PROPORTIONAL", font_size=26, color=accent_cyan, weight=BOLD)
        p_label.shift(UP * 2.5 + LEFT * 1.8)
        p_formula = MathTex(r"K_p \cdot e(t)", font_size=28, color=light_purple)
        p_formula.next_to(p_label, DOWN, buff=0.15).align_to(p_label, LEFT)
        
        p_bar_bg = Rectangle(width=2, height=0.4, color=deep_purple, stroke_width=2, fill_opacity=0.2)
        p_bar_bg.next_to(p_formula, DOWN, buff=0.2).align_to(p_label, LEFT)
        
        # Start with tiny bar properly positioned
        p_bar = Rectangle(width=0.01, height=0.4, color=accent_cyan, fill_opacity=0.8, stroke_width=0)
        p_bar.align_to(p_bar_bg, LEFT).align_to(p_bar_bg, UP).align_to(p_bar_bg, DOWN)
        
        p_value = DecimalNumber(0, num_decimal_places=2, font_size=24, color="#FFD700")
        p_value.next_to(p_bar_bg, RIGHT, buff=0.3)
        
        # Integral - middle (more spacing from proportional)
        i_label = Text("INTEGRAL", font_size=26, color="#FFD700", weight=BOLD)
        i_label.shift(UP * 0.5 + LEFT * 1.8)
        i_formula = MathTex(r"K_i \int e(t)dt", font_size=28, color=light_purple)
        i_formula.next_to(i_label, DOWN, buff=0.15).align_to(i_label, LEFT)
        
        i_bar_bg = Rectangle(width=2, height=0.4, color=deep_purple, stroke_width=2, fill_opacity=0.2)
        i_bar_bg.next_to(i_formula, DOWN, buff=0.2).align_to(i_label, LEFT)
        
        # Start with tiny bar properly positioned
        i_bar = Rectangle(width=0.01, height=0.4, color="#FFD700", fill_opacity=0.8, stroke_width=0)
        i_bar.align_to(i_bar_bg, LEFT).align_to(i_bar_bg, UP).align_to(i_bar_bg, DOWN)
        
        i_value = DecimalNumber(0, num_decimal_places=2, font_size=24, color="#FFD700")
        i_value.next_to(i_bar_bg, RIGHT, buff=0.3)
        
        # Derivative - bottom (more spacing from integral)
        d_label = Text("DERIVATIVE", font_size=26, color="#90EE90", weight=BOLD)
        d_label.shift(DOWN * 1.5 + LEFT * 1.8)
        d_formula = MathTex(r"K_d \frac{de(t)}{dt}", font_size=28, color=light_purple)
        d_formula.next_to(d_label, DOWN, buff=0.15).align_to(d_label, LEFT)
        
        d_bar_bg = Rectangle(width=2, height=0.4, color=deep_purple, stroke_width=2, fill_opacity=0.2)
        d_bar_bg.next_to(d_formula, DOWN, buff=0.2).align_to(d_label, LEFT)
        
        # Start with tiny bar properly positioned
        d_bar = Rectangle(width=0.01, height=0.4, color="#90EE90", fill_opacity=0.8, stroke_width=0)
        d_bar.align_to(d_bar_bg, LEFT).align_to(d_bar_bg, UP).align_to(d_bar_bg, DOWN)
        
        d_value = DecimalNumber(0, num_decimal_places=2, font_size=24, color="#FFD700")
        d_value.next_to(d_bar_bg, RIGHT, buff=0.3)
        
        # Show components
        self.play(
            LaggedStart(
                FadeIn(VGroup(p_label, p_formula, p_bar_bg, p_bar, p_value)),
                FadeIn(VGroup(i_label, i_formula, i_bar_bg, i_bar, i_value)),
                FadeIn(VGroup(d_label, d_formula, d_bar_bg, d_bar, d_value)),
                lag_ratio=0.3
            )
        )
        self.wait(1)
        
        # Simulation parameters - OPTIMIZED for near-zero convergence
        Kp, Ki, Kd = 0.9, 0.08, 1.2  # Carefully tuned for smooth convergence
        setpoint = 3.0  # Position at the end of track (where hexagon is)
        position = -3.0  # Start at beginning
        velocity = 0
        integral = 0
        dt = 0.06
        prev_error = setpoint - position
        
        # Simulate PID control - better convergence
        for step in range(70):
            # Calculate error
            error = setpoint - position
            
            # PID terms
            p_term = Kp * error
            integral += error * dt
            # Anti-windup: clamp integral
            integral = max(-10, min(10, integral))
            i_term = Ki * integral
            derivative = (error - prev_error) / dt
            d_term = Kd * derivative
            
            # Control output
            control = p_term + i_term + d_term
            
            # Update position (better physics)
            velocity += control * dt
            velocity *= 0.95  # Damping
            position += velocity * dt
            
            # Clamp position
            position = max(-3, min(3, position))
            
            # Update visuals
            new_pos = track_y + RIGHT * position
            
            # Update bars - constrain to background width
            p_width = min(max(abs(p_term) * 0.12, 0.01), 2.0)
            i_width = min(max(abs(i_term) * 0.3, 0.01), 2.0)
            d_width = min(max(abs(d_term) * 0.15, 0.01), 2.0)
            
            # Create new bars aligned with backgrounds
            new_p_bar = Rectangle(width=p_width, height=0.4, color=accent_cyan, fill_opacity=0.8, stroke_width=0)
            new_p_bar.align_to(p_bar_bg, LEFT).align_to(p_bar_bg, UP).align_to(p_bar_bg, DOWN)
            
            new_i_bar = Rectangle(width=i_width, height=0.4, color="#FFD700", fill_opacity=0.8, stroke_width=0)
            new_i_bar.align_to(i_bar_bg, LEFT).align_to(i_bar_bg, UP).align_to(i_bar_bg, DOWN)
            
            new_d_bar = Rectangle(width=d_width, height=0.4, color="#90EE90", fill_opacity=0.8, stroke_width=0)
            new_d_bar.align_to(d_bar_bg, LEFT).align_to(d_bar_bg, UP).align_to(d_bar_bg, DOWN)
            
            # Update trail
            trail_dots.shift(LEFT * 0.035)
            
            if step % 3 == 0:
                self.play(
                    current.animate.move_to(new_pos),
                    Transform(p_bar, new_p_bar),
                    Transform(i_bar, new_i_bar),
                    Transform(d_bar, new_d_bar),
                    error_value.animate.set_value(abs(error)),
                    p_value.animate.set_value(p_term),
                    i_value.animate.set_value(i_term),
                    d_value.animate.set_value(d_term),
                    run_time=0.12
                )
            else:
                current.move_to(new_pos)
                p_bar.become(new_p_bar)
                i_bar.become(new_i_bar)
                d_bar.become(new_d_bar)
                error_value.set_value(abs(error))
                p_value.set_value(p_term)
                i_value.set_value(i_term)
                d_value.set_value(d_term)
            
            prev_error = error
            
            # Stop when error is very small (near zero)
            if abs(error) < 0.01 and abs(velocity) < 0.05:
                break
        
        # Success indicator
        current.generate_target()
        current.target.set_color(GREEN)
        self.play(MoveToTarget(current))
        
        checkmark = Text("✓", font_size=48, color=GREEN, weight=BOLD)
        checkmark.move_to(track_y)
        self.play(FadeIn(checkmark, scale=1.3))
        self.wait(0.5)
        self.play(FadeOut(checkmark))
        
        self.wait(1)
        
        # Clean up for explanations
        self.play(
            FadeOut(VGroup(track, target, current, trail_dots, error_label, error_value)),
            FadeOut(VGroup(p_label, p_formula, p_bar_bg, p_bar, p_value)),
            FadeOut(VGroup(i_label, i_formula, i_bar_bg, i_bar, i_value)),
            FadeOut(VGroup(d_label, d_formula, d_bar_bg, d_bar, d_value)),
            FadeOut(equation)
        )
        
        # Explain each component
        explanations = [
            ("Proportional (P)", "Responds to current error", "Larger error → Stronger correction", accent_cyan),
            ("Integral (I)", "Eliminates steady-state error", "Sums past errors over time", "#FFD700"),
            ("Derivative (D)", "Predicts future error", "Dampens oscillations", "#90EE90"),
        ]
        
        for comp_name, desc1, desc2, color in explanations:
            comp_title = Text(comp_name, font_size=44, color=color, weight=BOLD)
            comp_title.shift(UP * 2.5)
            
            desc1_text = Text(desc1, font_size=34, color=light_purple)
            desc1_text.next_to(comp_title, DOWN, buff=0.5)
            
            desc2_text = Text(desc2, font_size=30, color=WHITE)
            desc2_text.next_to(desc1_text, DOWN, buff=0.35)
            
            self.play(FadeIn(comp_title, scale=1.1))
            self.play(FadeIn(desc1_text))
            self.play(FadeIn(desc2_text))
            self.wait(2)
            self.play(FadeOut(VGroup(comp_title, desc1_text, desc2_text)))
            self.wait(0.3)
        
        # Applications
        app_title = Text("Real-World Applications", font_size=40, color=accent_cyan, weight=BOLD)
        app_title.shift(UP * 4.5)
        
        applications = VGroup(
            Text("• Cruise control systems", font_size=32, color=light_purple),
            Text("• Drone stabilization", font_size=32, color=light_purple),
            Text("• Temperature regulation", font_size=32, color=light_purple),
            Text("• Robot arm positioning", font_size=32, color=light_purple),
            Text("• Industrial automation", font_size=32, color=light_purple),
        ).arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        applications.shift(UP * 1)
        
        self.play(FadeIn(app_title))
        self.play(LaggedStart(*[FadeIn(app, shift=RIGHT*0.3) for app in applications], lag_ratio=0.15))
        self.wait(2.5)
        
        self.play(FadeOut(app_title), FadeOut(applications), FadeOut(title))
        
        # Follow for more
        follow_text = VGroup(
            Text("Follow for more", font_size=50, color=accent_cyan, weight=BOLD),
            Text("control systems explained", font_size=34, color=light_purple)
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