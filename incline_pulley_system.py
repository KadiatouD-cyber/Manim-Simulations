from manim import *
import numpy as np

config.pixel_height = 1920
config.pixel_width = 1080
config.frame_rate = 60
config.frame_height = 16.0
config.frame_width = 9.0

class InclinePulleySystem(Scene):
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
        title = Text("Block on Frictional Incline with Pulley", font_size=50, weight=BOLD)
        title.set_color_by_gradient(primary_purple, accent_cyan)
        title.to_edge(UP, buff=0.3)
        self.play(Write(title), run_time=1)
        self.wait(0.5)
        
        subtitle = Text("Find a", font_size=40, color=light_purple)
        subtitle.next_to(title, DOWN, buff=0.2)
        self.play(FadeIn(subtitle), run_time=0.5)
        self.wait(0.5)
        
        # Setup the problem diagram
        # Incline angle
        theta = 30 * DEGREES
        incline_length = 4
        incline_height = incline_length * np.sin(theta)
        incline_base = incline_length * np.cos(theta)
        
        # Create incline
        incline_start = LEFT * 3.5 + DOWN * 1
        incline_end = incline_start + RIGHT * incline_base + UP * incline_height
        incline_base_end = incline_start + RIGHT * incline_base
        
        incline = Polygon(
            incline_start,
            incline_base_end,
            incline_end,
            color=WHITE,
            fill_opacity=0.2,
            stroke_width=3
        )
        
        # Angle arc
        angle_arc = Arc(
            radius=0.6,
            start_angle=0,
            angle=theta,
            color=accent_cyan,
            stroke_width=2
        ).shift(incline_start)
        
        theta_label = MathTex(r"\theta", color=accent_cyan, font_size=35)
        theta_label.next_to(angle_arc, RIGHT, buff=0.1).shift(UP * 0.1)
        
        # Block on incline (mass m)
        block_size = 0.5
        block_center = incline_start + RIGHT * incline_base * 0.4 + UP * incline_height * 0.4
        block_m = Square(side_length=block_size, color=primary_purple, fill_opacity=0.8, stroke_width=2)
        block_m.move_to(block_center)
        # Rotate to align with incline
        block_m.rotate(theta, about_point=block_m.get_center())
        
        # Label for block m
        m_label = MathTex("m", color=WHITE, font_size=40)
        m_label.move_to(block_m.get_center())
        
        # Pulley at top of incline
        pulley_center = incline_end + UP * 0.3
        pulley = Circle(radius=0.25, color=WHITE, stroke_width=3, fill_opacity=0.3)
        pulley.move_to(pulley_center)
        pulley_dot = Dot(pulley_center, color=WHITE, radius=0.05)
        
        # Hanging block (mass M)
        hanging_block_size = 0.6
        hanging_block_center = pulley_center + DOWN * 1.5
        block_M = Square(side_length=hanging_block_size, color=accent_cyan, fill_opacity=0.8, stroke_width=2)
        block_M.move_to(hanging_block_center)
        
        M_label = MathTex("M", color=WHITE, font_size=45)
        M_label.move_to(block_M.get_center())
        
        # Rope/String
        rope_to_pulley = Line(
            block_m.get_corner(UR) + UP * 0.05,
            pulley_center + LEFT * 0.25 * np.cos(theta) + DOWN * 0.25 * np.sin(theta),
            color=YELLOW,
            stroke_width=2
        )
        
        rope_vertical = Line(
            pulley_center + DOWN * 0.25,
            block_M.get_top(),
            color=YELLOW,
            stroke_width=2
        )
        
        # Draw the system
        self.play(
            Create(incline),
            Create(angle_arc),
            Write(theta_label),
            run_time=1.5
        )
        self.play(
            FadeIn(block_m),
            Write(m_label),
            run_time=1
        )
        self.play(
            Create(pulley),
            FadeIn(pulley_dot),
            run_time=0.8
        )
        self.play(
            Create(rope_to_pulley),
            Create(rope_vertical),
            run_time=1
        )
        self.play(
            FadeIn(block_M),
            Write(M_label),
            run_time=1
        )
        
        self.wait(1)
        
        # Now add force vectors for block m
        # Tension T
        T_vector_m = Arrow(
            block_m.get_center(),
            block_m.get_center() + RIGHT * np.cos(theta) * 1.2 + UP * np.sin(theta) * 1.2,
            buff=0,
            color=light_purple,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.15
        )
        T_label_m = MathTex("T", color=light_purple, font_size=40)
        T_label_m.next_to(T_vector_m.get_end(), UR, buff=0.1)
        
        # Weight mg
        mg_vector = Arrow(
            block_m.get_center(),
            block_m.get_center() + DOWN * 1.2,
            buff=0,
            color=pink_purple,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.15
        )
        mg_label = MathTex("mg", color=pink_purple, font_size=40)
        mg_label.next_to(mg_vector.get_end(), DOWN, buff=0.1)
        
        # Normal force N
        N_direction = np.array([-np.sin(theta), np.cos(theta), 0])
        N_vector = Arrow(
            block_m.get_center(),
            block_m.get_center() + N_direction * 1.0,
            buff=0,
            color=accent_cyan,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.15
        )
        N_label = MathTex("N", color=accent_cyan, font_size=40)
        N_label.next_to(N_vector.get_end(), UL, buff=0.1)
        
        # Friction force
        friction_direction = np.array([-np.cos(theta), -np.sin(theta), 0])
        friction_vector = Arrow(
            block_m.get_center(),
            block_m.get_center() + friction_direction * 0.8,
            buff=0,
            color=RED,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.15
        )
        friction_label = MathTex(r"\mu_k N", color=RED, font_size=35)
        friction_label.next_to(friction_vector.get_end(), DL, buff=0.1)
        
        # Show forces on block m
        force_text = Text("Forces on block m:", font_size=35, color=WHITE)
        force_text.to_corner(UL, buff=0.5).shift(DOWN * 1.5)
        
        self.play(Write(force_text), run_time=0.8)
        self.play(
            Create(T_vector_m),
            Write(T_label_m),
            run_time=0.8
        )
        self.play(
            Create(mg_vector),
            Write(mg_label),
            run_time=0.8
        )
        self.play(
            Create(N_vector),
            Write(N_label),
            run_time=0.8
        )
        self.play(
            Create(friction_vector),
            Write(friction_label),
            run_time=0.8
        )
        
        self.wait(1)
        
        # Now show forces on block M
        # Tension T upward
        T_vector_M = Arrow(
            block_M.get_center(),
            block_M.get_center() + UP * 1.2,
            buff=0,
            color=light_purple,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.15
        )
        T_label_M = MathTex("T", color=light_purple, font_size=40)
        T_label_M.next_to(T_vector_M.get_end(), UP, buff=0.1)
        
        # Weight Mg downward
        Mg_vector = Arrow(
            block_M.get_center(),
            block_M.get_center() + DOWN * 1.5,
            buff=0,
            color=pink_purple,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.15
        )
        Mg_label = MathTex("Mg", color=pink_purple, font_size=40)
        Mg_label.next_to(Mg_vector.get_end(), DOWN, buff=0.1)
        
        force_text_M = Text("Forces on block M:", font_size=35, color=WHITE)
        force_text_M.next_to(force_text, DOWN, buff=0.3, aligned_edge=LEFT)
        
        self.play(Write(force_text_M), run_time=0.8)
        self.play(
            Create(T_vector_M),
            Write(T_label_M),
            run_time=0.8
        )
        self.play(
            Create(Mg_vector),
            Write(Mg_label),
            run_time=0.8
        )
        
        self.wait(2)
        
        # Fade out diagram, keep title
        self.play(
            FadeOut(VGroup(
                incline, angle_arc, theta_label,
                block_m, m_label, block_M, M_label,
                pulley, pulley_dot, rope_to_pulley, rope_vertical,
                T_vector_m, T_label_m, mg_vector, mg_label,
                N_vector, N_label, friction_vector, friction_label,
                T_vector_M, T_label_M, Mg_vector, Mg_label,
                force_text, force_text_M
            )),
            run_time=1
        )
        
        # Show equations
        eq_title = Text("Newton's Second Law:", font_size=45, color=accent_cyan)
        eq_title.shift(UP * 2.5)
        self.play(Write(eq_title), run_time=0.8)
        
        # Equation for mass m
        eq_m_label = Text("For block m:", font_size=35, color=primary_purple)
        eq_m_label.shift(UP * 1.5 + LEFT * 3)
        
        eq_m = MathTex(
            r"T - mg\sin\theta - \mu_k N = ma",
            font_size=45,
            color=WHITE
        )
        eq_m.next_to(eq_m_label, DOWN, buff=0.3, aligned_edge=LEFT)
        
        self.play(Write(eq_m_label), run_time=0.6)
        self.play(Write(eq_m), run_time=1.5)
        self.wait(0.5)
        
        # Since N = mg cos(theta) for perpendicular equilibrium
        eq_m2 = MathTex(
            r"T - mg\sin\theta - \mu_k mg\cos\theta = ma",
            font_size=45,
            color=WHITE
        )
        eq_m2.move_to(eq_m.get_center())
        
        self.play(Transform(eq_m, eq_m2), run_time=1.5)
        self.wait(0.5)
        
        # Equation for mass M
        eq_M_label = Text("For block M:", font_size=35, color=accent_cyan)
        eq_M_label.shift(DOWN * 0.3 + LEFT * 3)
        
        eq_M = MathTex(
            r"Mg - T = Ma",
            font_size=45,
            color=WHITE
        )
        eq_M.next_to(eq_M_label, DOWN, buff=0.3, aligned_edge=LEFT)
        
        self.play(Write(eq_M_label), run_time=0.6)
        self.play(Write(eq_M), run_time=1.5)
        self.wait(1)
        
        # Add equations step
        add_text = Text("Add equations:", font_size=40, color=light_purple, weight=BOLD)
        add_text.shift(DOWN * 2.2)
        self.play(Write(add_text), run_time=0.8)
        self.wait(0.5)
        
        # Combined equation
        eq_combined = MathTex(
            r"(Mg - T) + (T - mg\sin\theta - \mu_k mg\cos\theta) = (M + m)a",
            font_size=40,
            color=WHITE
        )
        eq_combined.shift(DOWN * 3)
        self.play(Write(eq_combined), run_time=2)
        self.wait(1)
        
        # Simplify (T cancels)
        eq_simplified = MathTex(
            r"(M - m(\sin\theta + \mu_k\cos\theta))g = (M + m)a",
            font_size=42,
            color=WHITE
        )
        eq_simplified.shift(DOWN * 3.8)
        self.play(Write(eq_simplified), run_time=2)
        self.wait(1)
        
        # Final answer
        final_box = Rectangle(
            width=9,
            height=1.2,
            color=primary_purple,
            stroke_width=4,
            fill_opacity=0.1
        ).shift(DOWN * 5.2)
        
        final_answer = MathTex(
            r"a = \frac{(M - m(\sin\theta + \mu_k\cos\theta))g}{M + m}",
            font_size=50,
            color=accent_cyan
        )
        final_answer.move_to(final_box.get_center())
        
        self.play(Create(final_box), run_time=0.8)
        self.play(Write(final_answer), run_time=2)
        self.wait(2)
        
        # Highlight the answer
        self.play(
            final_box.animate.set_color(accent_cyan),
            final_answer.animate.scale(1.1),
            run_time=0.8
        )
        self.play(
            final_answer.animate.scale(1/1.1),
            run_time=0.5
        )
        
        self.wait(3)