from manim import *
import numpy as np
from scipy.integrate import solve_ivp

config.pixel_height = 1920
config.pixel_width = 1080
config.frame_rate = 60
config.frame_height = 16.0
config.frame_width = 9.0

# Define the Lorenz system of differential equations
# This is the mathematical heart of the animation so like three coupled equations that
# describe chaotic fluid convection, famous for their "butterfly effect"
def lorenz_system(t, state, sigma=10, rho=28, beta=8/3):
    x, y, z = state
    dxdt = sigma * (y - x)
    dydt = x * (rho - z) - y
    dzdt = x * y - beta * z
    return [dxdt, dydt, dzdt]

# Numerical ODE solver wrapper
# This function uses SciPy's solve_ivp to compute the trajectory points
# It converts continuous differential equations into discrete points for animation
def ode_solution_points(function, state0, time, dt=0.01):
    solution = solve_ivp(
        function,
        t_span=(0, time),
        y0=state0,
        t_eval=np.arange(0, time, dt)
    )
    return solution.y.T

class LorenzAttractor(ThreeDScene):
    def construct(self):
        # Color scheme for visual differentiation of trajectories
        # Each color represents a slightly different initial condition
        color1, color2, color3 = "#29F889", "#D463F7", "#00C8FF"
        gradient = [color1, color3, color2]
        
        # Create 3D coordinate axes
        # The axes provide spatial reference for the chaotic motion
        axes = ThreeDAxes(
            x_range=(-30, 30, 10),
            y_range=(-30, 30, 10),
            z_range=(0, 40, 10),
            x_length=8,
            y_length=8,
            z_length=5,
        ).shift(OUT * -1.8)
        self.add(axes)
        
        # Create a fixed title that won't move with 3D camera
        # Using add_fixed_in_frame_mobjects keeps 2D elements readable during 3D rotation
        title = MathTex(r"\mathbb{L}\text{orenz } \mathbb{A}\text{ttractor}").scale(1.5).set_stroke(width=2.5).shift(UP*5.5).set_color_by_gradient(color1, color3, color2)
        self.add_fixed_in_frame_mobjects(title)
        
        # Add TechFlux branding at bottom right in purple???
        techflux = Text("TechFlux", font_size=44, weight=BOLD, color="#9D4EDD")
        techflux.to_corner(DR, buff=0.5)
        self.add_fixed_in_frame_mobjects(techflux)
        
        #Set initial camera position and start automatic rotation
        # Phi controls vertical angle, theta controls horizontal angle
        # Ambient rotation creates a cinematic exploration of the 3D structure
        self.set_camera_orientation(phi=70 * DEGREES, theta=100 * DEGREES)
        self.begin_ambient_camera_rotation(rate=0.3)
        
        # Display the Lorenz equations as fixed 2D text
        # stays there throughout
        eqs = MathTex(
            r"\begin{aligned}"
            r"\dot{x} &= \sigma(y - x) \\"
            r"\dot{y} &= x(\rho - z) - y \\"
            r"\dot{z} &= xy - \beta z"
            r"\end{aligned}", font_size=60
        ).scale(1)
        eqs.shift(DOWN*4.8).set_stroke(width=2)
        eqs.set_color_by_gradient(*gradient)
        self.add_fixed_in_frame_mobjects(eqs)
        
        # Set up multiple initial conditions with tiny differences
      
        epsilon = 0.00001
        evolution_time = 20
        n_points = 4
        states = [[10, 10, 10 + n * epsilon] for n in range(n_points)]
        
        # Generate colors for each trajectory
        # Different colors help track how tiny differences lead to divergent paths
        colors = color_gradient([color1, color2, color1, color3], n_points)
        
        # Solve  differential equations for all starting points
        # This basically pre-computes all trajectory points before animation begins
        solution_sets = [
            ode_solution_points(lorenz_system, s, evolution_time)
            for s in states
        ]
        max_steps = min(len(sol) for sol in solution_sets)
        
        # Create visual elements for each trajectory
        # Each gets a colored dot (current position) and a tail (path history)
        dots = VGroup()
        tails = VGroup()
        for sol, color in zip(solution_sets, colors):
            # Convert first point from mathematical to visual coordinates
            start = axes.c2p(*sol[0])
            
            # Create a 3D sphere to represent current position
            dot = Dot3D(start, color=color, radius=0.1)
            
            # Create  empty VMobject for the growing tail
            # VMobject allows smooth, continuous line updates 
            tail = VMobject(stroke_color=color, stroke_width=5)
            tail.set_points_as_corners([start])  # Start with just the initial point
            
            dots.add(dot)
            tails.add(tail)
            self.add(tail)
        self.add(dots)
        
        # Group dots and tails for simultaneous updating
        animation_group = VGroup(dots, tails)
        
        # Custom update function for real-time trajectory drawing
        # This function is called continuously during animation to update positions
        def update_motion(mob, alpha):
            """Update both dots and tails simultaneously"""
            for i, (dot, tail) in enumerate(zip(dots, tails)):
                sol = solution_sets[i]
                # Calculate current frame index based on animation progress
                idx = min(int(alpha * len(sol)), len(sol) - 1)
                
                # Update dot to current position
                new_point = axes.c2p(*sol[idx])
                dot.move_to(new_point)
                
                # Build the tail by adding all points up to current position
                # basically creates the "drawing" effect as the dot moves
                points = [axes.c2p(*sol[j]) for j in range(idx + 1)]
                tail.set_points_as_corners(points)
        
        # Main animation: trace all trajectories simultaneously
        # UpdateFromAlphaFunc makes ir more smooth
        self.play(
            UpdateFromAlphaFunc(animation_group, update_motion),
            run_time=20,
            rate_func=linear  # Constant speed for natural motion
        )
        self.wait(2)
        
        # Stop automatic camera rotation for controlled final view
        self.stop_ambient_camera_rotation()
        
        # TReposition camera for a dramatic top-down view
        
        self.move_camera(
            phi=0 * DEGREES,     # Directly overhead
            theta=270 * DEGREES, # Specific orientation
            gamma=0 * DEGREES,   # No tilt??
            zoom=1,
            rate_func=linear
        )
        self.wait(1)