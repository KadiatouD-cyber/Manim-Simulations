from manim import *
import numpy as np
from scipy.stats import norm

config.pixel_height = 1920
config.pixel_width = 1080
config.frame_rate = 60
config.frame_height = 16.0
config.frame_width = 9.0

class NormalDistribution(Scene):
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
        title = Text("Normal Distribution", font_size=52, weight=BOLD, color=light_purple)
        title.to_edge(UP, buff=1.2)
        self.add(title)
        
        # Subtitle
        subtitle = Text("The Bell Curve That Rules Everything", font_size=28, color=accent_cyan)
        subtitle.next_to(title, DOWN, buff=0.3)
        self.play(FadeIn(subtitle))
        self.wait(1.5)
        self.play(FadeOut(subtitle))
        
        # Create axes
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[0, 0.5, 0.1],
            x_length=7,
            y_length=4.5,
            axis_config={"color": deep_purple, "stroke_width": 3},
            tips=False
        ).shift(UP * 0.5)
        
        # Labels
        x_label = MathTex(r"x", font_size=40, color=light_purple).next_to(axes.x_axis.get_end(), RIGHT, buff=0.3)
        
        self.play(Create(axes), FadeIn(x_label))
        self.wait(0.5)
        
        # Parameters
        mu = 0
        sigma = 1
        
        # Create the normal distribution curve
        curve = axes.plot(
            lambda x: norm.pdf(x, mu, sigma),
            x_range=[-4, 4],
            color=accent_cyan,
            stroke_width=6
        )
        
        # Draw curve with smooth animation
        self.play(Create(curve), run_time=2)
        self.wait(0.5)
        
        # Fill under curve with beautiful gradient
        area_full = axes.get_area(
            curve,
            x_range=[-4, 4],
            color=[deep_purple, accent_cyan, light_purple],
            opacity=0.4
        )
        self.play(FadeIn(area_full))
        self.wait(0.5)
        
        # Mean line
        mean_line = DashedLine(
            axes.c2p(mu, 0),
            axes.c2p(mu, norm.pdf(mu, mu, sigma)),
            color=YELLOW,
            stroke_width=4,
            dash_length=0.15
        )
        mean_label = MathTex(r"\mu", color=YELLOW, font_size=44).next_to(mean_line.get_top(), UP, buff=0.2)
        
        self.play(Create(mean_line), FadeIn(mean_label))
        self.wait(0.5)
        
        # 68-95-99.7 Rule Animation
        rule_title = Text("68-95-99.7 Rule", font_size=38, color=accent_cyan, weight=BOLD)
        rule_title.shift(UP * 5)
        self.play(FadeIn(rule_title))
        
        # 68% (1 sigma)
        area_1sigma = axes.get_area(
            curve,
            x_range=[-1, 1],
            color=GREEN,
            opacity=0.8
        )
        
        # Lines for 1 sigma
        sigma_line_left_1 = DashedLine(
            axes.c2p(-1, 0),
            axes.c2p(-1, norm.pdf(-1, mu, sigma)),
            color=GREEN,
            stroke_width=3,
            dash_length=0.1
        )
        sigma_line_right_1 = DashedLine(
            axes.c2p(1, 0),
            axes.c2p(1, norm.pdf(1, mu, sigma)),
            color=GREEN,
            stroke_width=3,
            dash_length=0.1
        )
        
        text_68 = VGroup(
            Text("68%", font_size=52, color=GREEN, weight=BOLD),
            Text("within ±1σ", font_size=28, color=GREEN)
        ).arrange(DOWN, buff=0.2)
        text_68.to_edge(DOWN, buff=2.5)
        
        self.play(
            FadeIn(area_1sigma),
            Create(sigma_line_left_1),
            Create(sigma_line_right_1),
            FadeIn(text_68),
            run_time=1
        )
        self.wait(1.5)
        self.play(
            FadeOut(area_1sigma),
            FadeOut(sigma_line_left_1),
            FadeOut(sigma_line_right_1),
            FadeOut(text_68)
        )
        
        # 95% (2 sigma)
        area_2sigma = axes.get_area(
            curve,
            x_range=[-2, 2],
            color=BLUE,
            opacity=0.8
        )
        
        sigma_line_left_2 = DashedLine(
            axes.c2p(-2, 0),
            axes.c2p(-2, norm.pdf(-2, mu, sigma)),
            color=BLUE,
            stroke_width=3,
            dash_length=0.1
        )
        sigma_line_right_2 = DashedLine(
            axes.c2p(2, 0),
            axes.c2p(2, norm.pdf(2, mu, sigma)),
            color=BLUE,
            stroke_width=3,
            dash_length=0.1
        )
        
        text_95 = VGroup(
            Text("95%", font_size=52, color=BLUE, weight=BOLD),
            Text("within ±2σ", font_size=28, color=BLUE)
        ).arrange(DOWN, buff=0.2)
        text_95.to_edge(DOWN, buff=2.5)
        
        self.play(
            FadeIn(area_2sigma),
            Create(sigma_line_left_2),
            Create(sigma_line_right_2),
            FadeIn(text_95),
            run_time=1
        )
        self.wait(1.5)
        self.play(
            FadeOut(area_2sigma),
            FadeOut(sigma_line_left_2),
            FadeOut(sigma_line_right_2),
            FadeOut(text_95)
        )
        
        # 99.7% (3 sigma)
        area_3sigma = axes.get_area(
            curve,
            x_range=[-3, 3],
            color=RED,
            opacity=0.8
        )
        
        sigma_line_left_3 = DashedLine(
            axes.c2p(-3, 0),
            axes.c2p(-3, norm.pdf(-3, mu, sigma)),
            color=RED,
            stroke_width=3,
            dash_length=0.1
        )
        sigma_line_right_3 = DashedLine(
            axes.c2p(3, 0),
            axes.c2p(3, norm.pdf(3, mu, sigma)),
            color=RED,
            stroke_width=3,
            dash_length=0.1
        )
        
        text_997 = VGroup(
            Text("99.7%", font_size=52, color=RED, weight=BOLD),
            Text("within ±3σ", font_size=28, color=RED)
        ).arrange(DOWN, buff=0.2)
        text_997.to_edge(DOWN, buff=2.5)
        
        self.play(
            FadeIn(area_3sigma),
            Create(sigma_line_left_3),
            Create(sigma_line_right_3),
            FadeIn(text_997),
            run_time=1
        )
        self.wait(1.5)
        self.play(
            FadeOut(area_3sigma),
            FadeOut(sigma_line_left_3),
            FadeOut(sigma_line_right_3),
            FadeOut(text_997),
            FadeOut(rule_title)
        )
        
        # Formula
        formula = MathTex(
            r"f(x) = \frac{1}{\sigma\sqrt{2\pi}} e^{-\frac{(x-\mu)^2}{2\sigma^2}}",
            font_size=40,
            color=light_purple
        )
        formula.to_edge(DOWN, buff=2)
        
        formula_box = SurroundingRectangle(formula, color=accent_cyan, buff=0.3, corner_radius=0.2, stroke_width=3)
        
        self.play(Write(formula), Create(formula_box))
        self.wait(2)
        self.play(FadeOut(formula), FadeOut(formula_box))
        
        # Clean up for examples
        self.play(
            FadeOut(axes),
            FadeOut(curve),
            FadeOut(area_full),
            FadeOut(mean_line),
            FadeOut(mean_label),
            FadeOut(x_label)
        )
        
        # Real-world examples
        examples_title = Text("Found Everywhere:", font_size=40, color=accent_cyan, weight=BOLD)
        examples_title.shift(UP * 5)
        
        examples = VGroup(
            Text(" Human heights", font_size=34, color=light_purple),
            Text("IQ scores", font_size=34, color=light_purple),
            Text("Test scores", font_size=34, color=light_purple),
            Text( "Measurement errors", font_size=34, color=light_purple),
            Text("Random processes", font_size=34, color=light_purple),
            Text(" Financial returns", font_size=34, color=light_purple)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.45)
        examples.shift(UP * 0.5)
        
        self.play(FadeIn(examples_title))
        self.play(LaggedStart(*[FadeIn(ex, shift=RIGHT*0.5) for ex in examples], lag_ratio=0.2))
        self.wait(2.5)
        
        self.play(FadeOut(examples), FadeOut(examples_title))
        
        # Central Limit Theorem
        clt_title = Text("Why is it Common?", font_size=40, color=accent_cyan, weight=BOLD)
        clt_title.shift(UP * 4)
        
        clt_text = VGroup(
            Text("Central Limit Theorem:", font_size=32, color=light_purple, weight=BOLD),
            Text("Sum many random variables", font_size=28, color=GRAY),
            Text("→ Normal Distribution", font_size=32, color=accent_cyan)
        ).arrange(DOWN, buff=0.4)
        clt_text.shift(UP * 1)
        
        self.play(FadeIn(clt_title))
        self.play(FadeIn(clt_text))
        self.wait(2.5)
        
        self.play(FadeOut(clt_title), FadeOut(clt_text))
        
        # Key insight
        insight = VGroup(
            Text("Nature loves symmetry", font_size=38, color=accent_cyan, weight=BOLD),
            Text("Random + Random + Random", font_size=30, color=light_purple),
            Text("= Predictable Pattern", font_size=30, color=pink_purple)
        ).arrange(DOWN, buff=0.5)
        insight.shift(UP * 1.5)
        
        self.play(FadeIn(insight, scale=1.1))
        self.wait(2)
        self.play(FadeOut(insight))
        
        # Follow for more
        follow_text = VGroup(
            Text("Follow for more", font_size=48, color=accent_cyan, weight=BOLD),
            Text("stats & math explained", font_size=32, color=light_purple)
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