from manim import *
import numpy as np

class HeartEquationAnimation(Scene):
    def construct(self):
        # Define your color scheme
        primary_purple = "#9D4EDD"
        light_purple = "#C77DFF"
        pink_purple = "#E0AAFF"
        deep_purple = "#7B2CBF"
        accent_cyan = "#00D9FF"
        
        # Set dark background
        self.camera.background_color = "#0a0a0a"
        
        # Title at the top
        title = Text(
            "Heart Equation",
            font_size=48,
            weight=BOLD,
            gradient=(primary_purple, light_purple)
        ).to_edge(UP, buff=0.6)
        
        # Equation below title
        equation = MathTex(
            r"y = x^{\frac{2}{3}} + 0.9\sin(kx)\sqrt{3-x^2}",
            color=light_purple,
            font_size=38
        ).next_to(title, DOWN, buff=0.35)
        
        # Parameter k value
        k_text = MathTex(
            r"k = 100.00",
            color=pink_purple,
            font_size=34
        ).next_to(equation, DOWN, buff=0.3)
        
        # Create coordinate system - adjusted to fit properly
        axes = Axes(
            x_range=[-2, 2, 0.5],
            y_range=[-1.8, 2, 0.5],
            x_length=5.5,
            y_length=5,
            axis_config={
                "color": primary_purple,
                "stroke_width": 2.5,
                "include_tip": True,
                "tip_width": 0.2,
                "tip_height": 0.2,
            },
        ).shift(DOWN * 0.6)
        
        # Add subtle grid
        grid = NumberPlane(
            x_range=[-2, 2, 0.5],
            y_range=[-1.8, 2, 0.5],
            x_length=5.5,
            y_length=5,
            background_line_style={
                "stroke_color": deep_purple,
                "stroke_width": 0.8,
                "stroke_opacity": 0.25,
            },
            axis_config={"stroke_opacity": 0},
        ).shift(DOWN * 0.6)
        
        # Heart equation function
        def heart_func(x, k=100):
            if abs(x) > np.sqrt(3):
                return None
            try:
                term1 = np.power(abs(x), 2/3)
                term2 = 0.9 * np.sin(k * x) * np.sqrt(3 - x**2)
                return term1 + term2
            except:
                return None
        
        # Create the heart curve with vertical lines effect
        k_value = 100
        x_samples = np.linspace(-np.sqrt(3), np.sqrt(3), 600)
        
        # Create vertical lines to form the heart (like in your image)
        lines = VGroup()
        for x in x_samples[::2]:  # Every other point for better performance
            y_val = heart_func(x, k_value)
            if y_val is not None:
                point = axes.c2p(x, y_val)
                start = axes.c2p(x, 0)
                
                # Color gradient from pink to light purple
                line = Line(
                    start, point,
                    stroke_width=2.5,
                    color=pink_purple
                )
                lines.add(line)
        
        # Create smooth heart outline
        heart_points = []
        for x in x_samples:
            y_val = heart_func(x, k_value)
            if y_val is not None:
                heart_points.append(axes.c2p(x, y_val))
        
        heart_outline = VMobject()
        heart_outline.set_points_smoothly(heart_points)
        heart_outline.set_stroke(color=primary_purple, width=3.5)
        heart_outline.set_fill(color=deep_purple, opacity=0.2)
        
        # TechFlux branding in bottom right
        branding = Text(
            "TechFlux",
            font_size=28,
            weight=BOLD,
            color=primary_purple
        ).to_corner(DR, buff=0.5)
        
        # ============ ANIMATIONS ============
        
        # 1. Fade in title
        self.play(
            FadeIn(title, scale=0.9),
            run_time=1
        )
        self.wait(0.4)
        
        # 2. Write equation
        self.play(
            Write(equation),
            run_time=1.8
        )
        self.wait(0.3)
        
        # 3. Show k parameter
        self.play(
            FadeIn(k_text, shift=UP*0.2),
            run_time=0.8
        )
        self.wait(0.5)
        
        # 4. Create coordinate system
        self.play(
            Create(grid),
            Create(axes),
            run_time=2
        )
        self.wait(0.4)
        
        # 5. Animate vertical lines appearing (like drawing the heart)
        self.play(
            LaggedStart(
                *[Create(line) for line in lines],
                lag_ratio=0.008,
                run_time=3.5
            )
        )
        self.wait(0.6)
        
        # 6. Draw the heart outline
        self.play(
            Create(heart_outline),
            run_time=2.5
        )
        self.wait(0.5)
        
        # 7. Add TechFlux branding
        self.play(
            FadeIn(branding, shift=UP*0.3),
            run_time=0.9
        )
        
        # 8. Hold the final frame
        self.wait(2.5)
        
        # 9. Fade everything out
        self.play(
            *[FadeOut(mob) for mob in self.mobjects],
            run_time=1.5
        )
        self.wait(0.5)
