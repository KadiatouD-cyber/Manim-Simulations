from manim import *
import numpy as np

config.pixel_height = 1920
config.pixel_width = 1080
config.frame_rate = 60
config.frame_height = 16.0
config.frame_width = 9.0

class WorkEnergyTheorem(Scene):
    def construct(self):
        # Purple color scheme
        primary_purple = "#9D4EDD"
        light_purple = "#C77DFF"
        pink_purple = "#E0AAFF"
        deep_purple = "#7B2CBF"
        accent_cyan = "#00D9FF"
        
        # TechFlux branding
        techflux = Text("TechFlux", font_size=44, weight=BOLD, color=primary_purple)
        techflux.to_corner(DR, buff=0.5)
        self.add(techflux)
        
        # Title
        title = Text("Work-Energy Theorem", font_size=48, weight=BOLD, color=light_purple)
        title.to_edge(UP, buff=1.2)
        self.add(title)
        
        # Subtitle
        subtitle = Text("Why pushing things makes them faster", font_size=28, color=accent_cyan)
        subtitle.next_to(title, DOWN, buff=0.3)
        self.play(FadeIn(subtitle))
        self.wait(1.5)
        self.play(FadeOut(subtitle))
        
        # ===== PART 1: THE SETUP =====
        setup_text = Text("The Setup", font_size=36, color=pink_purple, weight=BOLD)
        setup_text.shift(UP * 4.8)
        self.play(FadeIn(setup_text))
        
        # Ground
        ground = Line(LEFT * 4.5, RIGHT * 4.5, color=deep_purple, stroke_width=4).shift(DOWN * 2)
        # Ground hatching
        hatches = VGroup()
        for i in range(18):
            x = -4.5 + i * 0.5
            hatch = Line(
                [x, -2, 0],
                [x - 0.3, -2.3, 0],
                color=deep_purple,
                stroke_width=2,
                stroke_opacity=0.5
            )
            hatches.add(hatch)
        
        self.play(Create(ground), Create(hatches))
        
        # Block
        block = Square(
            side_length=0.8,
            fill_color=pink_purple,
            fill_opacity=0.9,
            stroke_color=light_purple,
            stroke_width=4
        ).move_to([-2.5, -1.6, 0])
        
        block_label = Text("m", font_size=32, color=WHITE, weight=BOLD)
        block_label.move_to(block.get_center())
        
        self.play(FadeIn(block), FadeIn(block_label))
        
        # Force arrow
        force_arrow = Arrow(
            block.get_right(),
            block.get_right() + RIGHT * 1.5,
            color=accent_cyan,
            stroke_width=6,
            max_tip_length_to_length_ratio=0.2
        )
        force_label = MathTex("F", color=accent_cyan, font_size=40)
        force_label.next_to(force_arrow, UP, buff=0.2)
        
        self.play(GrowArrow(force_arrow), FadeIn(force_label))
        
        # Displacement arrow (below block)
        displacement_arrow = Arrow(
            block.get_center() + DOWN * 0.8,
            block.get_center() + DOWN * 0.8 + RIGHT * 2,
            color=YELLOW,
            stroke_width=4,
            max_tip_length_to_length_ratio=0.15
        )
        displacement_label = MathTex("d", color=YELLOW, font_size=36)
        displacement_label.next_to(displacement_arrow, DOWN, buff=0.2)
        
        self.play(Create(displacement_arrow), FadeIn(displacement_label))
        self.wait(1)
        
        # Given values box
        given = VGroup(
            Text("Given:", font_size=26, color=accent_cyan, weight=BOLD),
            Text("Mass m = 2 kg", font_size=24, color=GRAY),
            Text("Force F = 10 N", font_size=24, color=GRAY),
            Text("Distance d = 5 m", font_size=24, color=GRAY),
            Text("Initial velocity = 0", font_size=24, color=GRAY)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        
        given_box = SurroundingRectangle(given, color=deep_purple, buff=0.3, corner_radius=0.15)
        given_group = VGroup(given_box, given)
        given_group.to_corner(UR, buff=0.8)
        
        self.play(FadeIn(given_group))
        self.wait(1.5)
        self.play(FadeOut(setup_text))
        
        # ===== PART 2: THE THEOREM =====
        theorem_text = Text("The Theorem", font_size=36, color=pink_purple, weight=BOLD)
        theorem_text.shift(UP * 4.8)
        self.play(FadeIn(theorem_text))
        
        # Main equation
        main_eq = MathTex(
            r"W_{net} = \Delta KE",
            font_size=52,
            color=accent_cyan
        )
        main_eq.to_corner(UL, buff=1.2)
        main_eq.shift(DOWN * 2.5)
        
        eq_box = SurroundingRectangle(main_eq, color=accent_cyan, buff=0.3, corner_radius=0.2, stroke_width=4)
        
        self.play(Write(main_eq), Create(eq_box))
        self.wait(1)
        
        # Expanded equation
        expanded_eq = VGroup(
            MathTex(r"W = F \cdot d", font_size=40, color=light_purple),
            MathTex(r"\Delta KE = \frac{1}{2}mv_f^2 - \frac{1}{2}mv_i^2", font_size=36, color=pink_purple)
        ).arrange(DOWN, buff=0.4)
        expanded_eq.next_to(main_eq, DOWN, buff=0.6)
        
        self.play(Write(expanded_eq))
        self.wait(1.5)
        self.play(FadeOut(theorem_text))
        
        # ===== PART 3: SOLVE =====
        solve_text = Text("Let's Solve It", font_size=36, color=pink_purple, weight=BOLD)
        solve_text.shift(UP * 4.8)
        self.play(FadeIn(solve_text))
        
        # Step 1: Calculate Work
        step1_title = Text("Step 1: Calculate Work", font_size=28, color=GREEN, weight=BOLD)
        step1_title.next_to(expanded_eq, DOWN, buff=0.8)
        
        step1_eqs = VGroup(
            MathTex(r"W = F \cdot d", font_size=34, color=GREEN),
            MathTex(r"W = 10 \times 5", font_size=34, color=GREEN),
            MathTex(r"W = 50 \text{ J}", font_size=38, color=GREEN, )
        ).arrange(DOWN, buff=0.3)
        step1_eqs.next_to(step1_title, DOWN, buff=0.4)
        
        self.play(FadeIn(step1_title))
        for eq in step1_eqs:
            self.play(Write(eq), run_time=0.6)
            self.wait(0.3)
        self.wait(0.8)
        
        # Step 2: Use theorem to find velocity
        step2_title = Text("Step 2: Find Final Velocity", font_size=28, color=BLUE, weight=BOLD)
        step2_title.next_to(step1_eqs, DOWN, buff=0.6)
        
        step2_eqs = VGroup(
            MathTex(r"W = \frac{1}{2}mv_f^2 - \frac{1}{2}mv_i^2", font_size=30, color=BLUE),
            MathTex(r"50 = \frac{1}{2}(2)v_f^2 - 0", font_size=30, color=BLUE),
            MathTex(r"50 = v_f^2", font_size=30, color=BLUE),
            MathTex(r"v_f = \sqrt{50} \approx 7.07 \text{ m/s}", font_size=34, color=BLUE)
        ).arrange(DOWN, buff=0.25)
        step2_eqs.next_to(step2_title, DOWN, buff=0.4)
        
        self.play(FadeIn(step2_title))
        for eq in step2_eqs:
            self.play(Write(eq), run_time=0.6)
            self.wait(0.3)
        
        self.wait(1)
        self.play(FadeOut(solve_text))
        
        # ===== PART 4: ANSWER =====
        answer_text = Text("The Answer", font_size=36, color=pink_purple, weight=BOLD)
        answer_text.shift(UP * 4.8)
        self.play(FadeIn(answer_text))
        
        # Clear solve equations
        self.play(
            FadeOut(main_eq),
            FadeOut(eq_box),
            FadeOut(expanded_eq),
            FadeOut(step1_title),
            FadeOut(step1_eqs),
            FadeOut(step2_title),
            FadeOut(step2_eqs),
            FadeOut(given_group)
        )
        
        # Answer boxes
        work_box = VGroup(
            Text("Work Done", font_size=28, color=GREEN, weight=BOLD),
            MathTex(r"W = 50 \text{ J}", font_size=44, color=GREEN)
        ).arrange(DOWN, buff=0.3)
        work_box_rect = SurroundingRectangle(work_box, color=GREEN, buff=0.3, corner_radius=0.2, stroke_width=3)
        work_group = VGroup(work_box_rect, work_box)
        work_group.shift(LEFT * 2 + UP * 1.5)
        
        velocity_box = VGroup(
            Text("Final Velocity", font_size=28, color=BLUE, weight=BOLD),
            MathTex(r"v_f = 7.07 \text{ m/s}", font_size=44, color=BLUE)
        ).arrange(DOWN, buff=0.3)
        velocity_box_rect = SurroundingRectangle(velocity_box, color=BLUE, buff=0.3, corner_radius=0.2, stroke_width=3)
        velocity_group = VGroup(velocity_box_rect, velocity_box)
        velocity_group.shift(RIGHT * 2 + UP * 1.5)
        
        self.play(FadeIn(work_group), FadeIn(velocity_group))
        self.wait(1)
        
        # Energy bar comparison
        energy_title = Text("Energy Visualization", font_size=28, color=accent_cyan, weight=BOLD)
        energy_title.shift(DOWN * 0.5)
        self.play(FadeIn(energy_title))
        
        # Work energy bar
        work_bar_outline = Rectangle(
            width=5,
            height=0.6,
            stroke_color=GREEN,
            stroke_width=3,
            fill_opacity=0
        ).shift(DOWN * 1.5)
        
        work_bar_fill = Rectangle(
            width=5,
            height=0.6,
            fill_color=GREEN,
            fill_opacity=0.7,
            stroke_width=0
        ).shift(DOWN * 1.5)
        
        work_bar_label = MathTex(r"W = 50 \text{ J}", font_size=28, color=GREEN)
        work_bar_label.next_to(work_bar_outline, RIGHT, buff=0.3)
        
        # KE bar
        ke_bar_outline = Rectangle(
            width=5,
            height=0.6,
            stroke_color=BLUE,
            stroke_width=3,
            fill_opacity=0
        ).shift(DOWN * 2.5)
        
        ke_bar_fill = Rectangle(
            width=5,
            height=0.6,
            fill_color=BLUE,
            fill_opacity=0.7,
            stroke_width=0
        ).shift(DOWN * 2.5)
        
        ke_bar_label = MathTex(r"KE = 50 \text{ J}", font_size=28, color=BLUE)
        ke_bar_label.next_to(ke_bar_outline, RIGHT, buff=0.3)
        
        # Labels
        work_bar_title = Text("Work", font_size=24, color=GREEN)
        work_bar_title.next_to(work_bar_outline, LEFT, buff=0.3)
        ke_bar_title = Text("KE", font_size=24, color=BLUE)
        ke_bar_title.next_to(ke_bar_outline, LEFT, buff=0.3)
        
        # Animate bars filling
        self.play(Create(work_bar_outline), Create(ke_bar_outline))
        
        work_bar_fill_anim = work_bar_fill.copy().scale([0, 1, 1])
        work_bar_fill_anim.align_to(work_bar_outline, LEFT)
        self.add(work_bar_fill_anim)
        
        ke_bar_fill_anim = ke_bar_fill.copy().scale([0, 1, 1])
        ke_bar_fill_anim.align_to(ke_bar_outline, LEFT)
        self.add(ke_bar_fill_anim)
        
        self.play(
            work_bar_fill_anim.animate.become(work_bar_fill),
            run_time=1.5
        )
        self.play(
            ke_bar_fill_anim.animate.become(ke_bar_fill),
            run_time=1.5
        )
        
        self.play(
            FadeIn(work_bar_label),
            FadeIn(ke_bar_label),
            FadeIn(work_bar_title),
            FadeIn(ke_bar_title)
        )
        self.wait(1.5)
        
        # Equal sign between bars
        equal_sign = Text("=", font_size=48, color=accent_cyan, weight=BOLD)
        equal_sign.shift(DOWN * 2 + RIGHT * 3.8)
        self.play(FadeIn(equal_sign))
        self.wait(1)
        
        # ===== PART 5: MOTION SIMULATION =====
        # Clean up
        self.play(
            FadeOut(work_group),
            FadeOut(velocity_group),
            FadeOut(energy_title),
            FadeOut(work_bar_outline),
            FadeOut(work_bar_fill_anim),
            FadeOut(work_bar_label),
            FadeOut(work_bar_title),
            FadeOut(ke_bar_outline),
            FadeOut(ke_bar_fill_anim),
            FadeOut(ke_bar_label),
            FadeOut(ke_bar_title),
            FadeOut(equal_sign),
            FadeOut(answer_text)
        )
        
        # Show it in action
        action_text = Text("See it in action!", font_size=36, color=accent_cyan, weight=BOLD)
        action_text.shift(UP * 4.8)
        self.play(FadeIn(action_text))
        
        # Reset block position
        block.move_to([-3, -1.6, 0])
        block_label.move_to(block.get_center())
        
        # Force arrow on block
        force_arrow_sim = Arrow(
            block.get_right(),
            block.get_right() + RIGHT * 1.2,
            color=accent_cyan,
            stroke_width=5,
            max_tip_length_to_length_ratio=0.2
        )
        
        # Velocity label
        vel_label = Text("v = 0 m/s", font_size=28, color=YELLOW)
        vel_label.next_to(block, UP, buff=0.5)
        
        # KE label
        ke_label = Text("KE = 0 J", font_size=28, color=BLUE)
        ke_label.next_to(vel_label, UP, buff=0.3)
        
        # Work label
        work_label_sim = Text("W = 0 J", font_size=28, color=GREEN)
        work_label_sim.next_to(ke_label, UP, buff=0.3)
        
        self.play(
            FadeIn(force_arrow_sim),
            FadeIn(vel_label),
            FadeIn(ke_label),
            FadeIn(work_label_sim)
        )
        
        # Simulate motion
        F = 10  # Force
        m = 2   # Mass
        d_total = 5  # Total distance
        a = F / m   # Acceleration
        
        n_steps = 30
        
        for step in range(1, n_steps + 1):
            t_frac = step / n_steps
            
            # Calculate distance traveled
            d = d_total * t_frac
            
            # Calculate velocity at this point
            v = np.sqrt(2 * a * d)
            
            # Calculate KE
            KE = 0.5 * m * v ** 2
            
            # Calculate Work
            W = F * d
            
            # New position
            new_x = -3 + d * 1.2  # Scale for screen
            
            # Update block position
            new_block_pos = [new_x, -1.6, 0]
            
            # Update labels
            new_vel_label = Text(f"v = {v:.2f} m/s", font_size=28, color=YELLOW)
            new_vel_label.next_to([new_x, -1.6, 0], UP * 2.5, buff=0)
            
            new_ke_label = Text(f"KE = {KE:.1f} J", font_size=28, color=BLUE)
            new_ke_label.next_to(new_vel_label, UP, buff=0.3)
            
            new_work_label = Text(f"W = {W:.1f} J", font_size=28, color=GREEN)
            new_work_label.next_to(new_ke_label, UP, buff=0.3)
            
            # Update force arrow
            new_force_arrow = Arrow(
                [new_x + 0.4, -1.6, 0],
                [new_x + 1.6, -1.6, 0],
                color=accent_cyan,
                stroke_width=5,
                max_tip_length_to_length_ratio=0.2
            )
            
            run_time = 0.15 if step < n_steps else 0.3
            
            self.play(
                block.animate.move_to(new_block_pos),
                block_label.animate.move_to(new_block_pos),
                Transform(vel_label, new_vel_label),
                Transform(ke_label, new_ke_label),
                Transform(work_label_sim, new_work_label),
                Transform(force_arrow_sim, new_force_arrow),
                run_time=run_time,
                rate_func=linear
            )
        
        self.wait(1.5)
        
        # Final message
        self.play(
            FadeOut(block),
            FadeOut(block_label),
            FadeOut(force_arrow),
            FadeOut(force_label),
            FadeOut(displacement_arrow),
            FadeOut(displacement_label),
            FadeOut(force_arrow_sim),
            FadeOut(vel_label),
            FadeOut(ke_label),
            FadeOut(work_label_sim),
            FadeOut(ground),
            FadeOut(hatches),
            FadeOut(action_text)
        )
        
        # Key insight
        insight = VGroup(
            Text("Work = Change in KE", font_size=42, color=accent_cyan, weight=BOLD),
            Text("Force over distance", font_size=30, color=light_purple),
            Text("= Speed gained", font_size=30, color=pink_purple)
        ).arrange(DOWN, buff=0.5)
        insight.shift(UP * 1.5)
        
        self.play(FadeIn(insight))
        self.wait(2)
        self.play(FadeOut(insight))
        
        # Follow for more
        follow_text = VGroup(
            Text("Follow for more", font_size=48, color=accent_cyan, weight=BOLD),
            Text("physics explained", font_size=32, color=light_purple)
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
        
        self.wait(1.5)
        
        # Fade out
        self.play(
            FadeOut(follow_text),
            FadeOut(arrow),
            FadeOut(title),
            FadeOut(techflux)
        )
        self.wait(0.5)