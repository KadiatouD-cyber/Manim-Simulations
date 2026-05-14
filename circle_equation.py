from manim import *
import numpy as np

config.pixel_width = 1080
config.pixel_height = 1920
config.frame_rate = 60
config.frame_width = 9
config.frame_height = 16

# ─────────────────────────────────────────────
#  TechFlux Color Palette
# ─────────────────────────────────────────────
PRIMARY_PURPLE  = "#9D4EDD"
LIGHT_PURPLE    = "#C77DFF"
PINK_PURPLE     = "#E0AAFF"
DEEP_PURPLE     = "#7B2CBF"
ACCENT_CYAN     = "#00D9FF"
ACCENT_CYAN2    = "#00C8FF"
BG_COLOR        = "#0a0a0a"

GRAD_PURPLE     = [PRIMARY_PURPLE, LIGHT_PURPLE]
GRAD_CYAN       = [ACCENT_CYAN, ACCENT_CYAN2]
GRAD_MIX        = [PRIMARY_PURPLE, ACCENT_CYAN, LIGHT_PURPLE]
GRAD_MIX2       = [ACCENT_CYAN, PRIMARY_PURPLE]


class CircleEquationTechFlux(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        # Branding (persistent) 
        techflux = Text("TechFlux", font_size=44, weight=BOLD, color=PRIMARY_PURPLE)
        brand_sub = Text("Physics Explained", font_size=24, color=ACCENT_CYAN)
        brand = VGroup(techflux, brand_sub).arrange(DOWN, buff=0.1, aligned_edge=RIGHT)
        brand.to_corner(DR, buff=0.5)
        self.add(brand)

        # Hook title 
        hook = MathTex(
            r"\mathbb{C}\text{ircle }\mathbb{E}\text{quation}"
        ).scale(1.7).set_stroke(width=2.5).set_color_by_gradient(*GRAD_MIX)
        hook.move_to(UP * 1)

        self.play(Write(hook), run_time=1.2)
        self.wait(0.3)

        # Build coordinate axes 
        axes = Axes(
            x_range=[-2, 6],
            y_range=[-2, 6],
            x_length=6,
            y_length=6,
            axis_config={
                "stroke_width": 3,
                "include_numbers": False,
                "include_tip": True,
                "stroke_color": LIGHT_PURPLE,
            },
        ).shift(LEFT * 0.3)
        axes.x_axis.tip.scale(0.7)
        axes.y_axis.tip.scale(0.7)

        x_label = MathTex("x", font_size=40, color=LIGHT_PURPLE).next_to(axes.x_axis.tip, UP, buff=0.3)
        y_label = MathTex("y", font_size=40, color=LIGHT_PURPLE).next_to(axes.y_axis.tip, RIGHT, buff=0.3)
        labels  = VGroup(x_label, y_label)

        self.play(
            hook.animate.shift(UP * 4),
            GrowFromCenter(axes),
            FadeIn(labels),
            run_time=0.9,
        )

        # Circle geometry 
        a, b, r = 3, 3, 2

        center_dot = Dot(axes.c2p(a, b), color=ACCENT_CYAN, radius=0.1).set_z_index(2)
        center_label = MathTex("(a,\, b)", font_size=30, color=ACCENT_CYAN) \
            .next_to(center_dot, UL, buff=0.1).set_stroke(width=2)

        circle = Circle(
            radius=axes.x_axis.unit_size * r, stroke_width=7
        ).set_color_by_gradient(*GRAD_MIX).move_to(axes.c2p(a, b))

        # Point on circle
        angle = 48 * DEGREES
        px = a + r * np.cos(angle)
        py = b + r * np.sin(angle)
        point_dot   = Dot(axes.c2p(px, py), color=PINK_PURPLE, radius=0.1).set_z_index(2)
        point_label = MathTex("(x,\, y)", font_size=30, color=PINK_PURPLE) \
            .next_to(point_dot, UR, buff=0.1).set_stroke(width=2)

        self.play(FadeIn(center_dot), Write(center_label), Create(circle), run_time=0.9)

        # Dashed projection lines 
        dash_kw = dict(stroke_width=4, dashed_ratio=0.45, dash_length=0.07)
        x_proj = DashedLine(axes.c2p(px, py), axes.c2p(px, 0), **dash_kw).set_color_by_gradient(*GRAD_PURPLE)
        a_proj = DashedLine(axes.c2p(a,  b ), axes.c2p(a,  0), **dash_kw).set_color_by_gradient(*GRAD_PURPLE)
        y_proj = DashedLine(axes.c2p(px, py), axes.c2p(0, py), **dash_kw).set_color_by_gradient(*GRAD_CYAN)
        b_proj = DashedLine(axes.c2p(a,  b ), axes.c2p(0,  b), **dash_kw).set_color_by_gradient(*GRAD_CYAN)

        x_diff = MathTex(r"(x-a)", font_size=30, color=LIGHT_PURPLE) \
            .next_to(axes.c2p((a + px) / 2, 0), DOWN, buff=0.25).set_stroke(width=2)
        y_diff = MathTex(r"(y-b)", font_size=30, color=ACCENT_CYAN) \
            .next_to(axes.c2p(0, (b + py) / 2), LEFT, buff=0.25).set_stroke(width=2)

        #  Triangle sides 
        A = axes.c2p(a,  b )
        B = axes.c2p(px, b )
        C = axes.c2p(px, py)

        radius_line = Line(A, C, stroke_width=8) \
            .set_color_by_gradient(*GRAD_MIX).set_sheen_direction(UR)
        r_label = MathTex(r"r", font_size=42, color=WHITE) \
            .move_to(radius_line.get_center() + 0.18 * UP + 0.18 * LEFT).set_stroke(width=2)

        h_line = Line(A, B, stroke_width=7).set_color_by_gradient(*GRAD_PURPLE)
        v_line = Line(B, C, stroke_width=7).set_color_by_gradient(*GRAD_CYAN).set_z_index(1)

        self.play(FadeIn(point_dot), FadeIn(point_label), Create(radius_line), FadeIn(r_label))
        self.play(Create(a_proj), Create(x_proj), FadeIn(x_diff, shift=DOWN * 0.5))
        self.wait(0.3)
        self.play(Create(b_proj), Create(y_proj), FadeIn(y_diff, shift=LEFT * 0.5))
        self.play(FadeOut(center_label))
        self.play(Create(h_line), x_diff.animate.next_to(h_line, DOWN))
        self.play(Create(v_line), y_diff.animate.next_to(v_line, RIGHT))

        #  Pythagoras label & equation 
        pyt_text = Text("by Pythagoras' Theorem", font_size=30) \
            .set_color_by_gradient(*GRAD_MIX).move_to(DOWN * 3.5).set_stroke(width=1.5)
        self.play(Write(pyt_text), run_time=0.7)

        final_eq = MathTex(
            r"(x-a)^2", r"+", r"(y-b)^2", r"=", r"r^2",
            font_size=48
        ).set_stroke(width=2).move_to(DOWN * 4.3)
        final_eq[0].set_color(LIGHT_PURPLE)
        final_eq[2].set_color(ACCENT_CYAN)
        final_eq[4].set_color(PINK_PURPLE)

        box = SurroundingRectangle(
            final_eq, corner_radius=0.25, buff=0.22, stroke_width=5
        ).set_color_by_gradient(*GRAD_MIX)

        # Glowy fill on the box
        box_fill = SurroundingRectangle(
            final_eq, corner_radius=0.25, buff=0.22, stroke_width=0,
            fill_color=DEEP_PURPLE, fill_opacity=0.35
        )

        self.play(TransformMatchingShapes(x_diff.copy(), final_eq[0]))
        self.play(Write(final_eq[1]))
        self.play(TransformMatchingShapes(y_diff.copy(), final_eq[2]))
        self.play(Write(final_eq[3]))
        self.play(TransformMatchingShapes(r_label.copy(), final_eq[4]))
        self.play(FadeIn(box_fill), Create(box))

        self.wait(0.5)

        # Clean up diagram for interactive demo 
        self.play(
            FadeOut(
                pyt_text, point_dot, point_label, radius_line, r_label,
                x_proj, a_proj, y_proj, b_proj, h_line, v_line, labels,
                x_diff, y_diff,
            ),
            run_time=0.7,
        )

        # ValueTracker interactive demo 
        a_tr = ValueTracker(0)
        b_tr = ValueTracker(0)
        r_tr = ValueTracker(2)

        axes2 = Axes(
            x_range=[-4, 4],
            y_range=[-4, 4],
            x_length=6,
            y_length=6,
            axis_config={
                "stroke_width": 3,
                "include_numbers": False,
                "include_tip": True,
                "stroke_color": LIGHT_PURPLE,
            },
        ).shift(UP * 1.2)
        axes2.x_axis.tip.scale(0.6)
        axes2.y_axis.tip.scale(0.6)

        center_dot2 = always_redraw(
            lambda: Dot(
                axes2.c2p(a_tr.get_value(), b_tr.get_value()),
                color=ACCENT_CYAN, radius=0.1,
            ).set_z_index(2)
        )

        circle2 = always_redraw(
            lambda: Circle(
                radius=axes2.x_axis.unit_size * r_tr.get_value(),
                stroke_width=8,
            ).set_color_by_gradient(*GRAD_MIX)
            .move_to(axes2.c2p(a_tr.get_value(), b_tr.get_value()))
        )

        # Parameter display positions
        base_y = axes2.get_center() + DOWN * 3.9
        pos_a = base_y + LEFT * 2.5
        pos_b = base_y
        pos_r = base_y + RIGHT * 2.5

        def _param_tex(label, tracker, color):
            return always_redraw(
                lambda: MathTex(
                    f"{label} = {tracker.get_value():.1f}",
                    font_size=40, color=color,
                ).set_stroke(width=1.8).move_to(
                    pos_a if label == "a" else (pos_b if label == "b" else pos_r)
                )
            )

        txt_a = _param_tex("a", a_tr, LIGHT_PURPLE)
        txt_b = _param_tex("b", b_tr, ACCENT_CYAN)
        txt_r = _param_tex("r", r_tr, PINK_PURPLE)

        def _param_box(txt, grad):
            return always_redraw(
                lambda: SurroundingRectangle(
                    txt, corner_radius=0.2, buff=0.2, stroke_width=4
                ).set_color_by_gradient(*grad)
            )

        bx_a = _param_box(txt_a, GRAD_PURPLE)
        bx_b = _param_box(txt_b, GRAD_CYAN)
        bx_r = _param_box(txt_r, [PINK_PURPLE, LIGHT_PURPLE])

        # Transition from first axes to second
        self.play(
            ReplacementTransform(VGroup(circle, axes), VGroup(circle2, axes2)),
            ReplacementTransform(center_dot, center_dot2),
            FadeOut(box, box_fill),
            run_time=0.9,
        )
        self.add(txt_a, txt_b, txt_r, bx_a, bx_b, bx_r, center_dot2)

        # Slide in the equation and param boxes
        final_eq.generate_target()
        final_eq.target.move_to(DOWN * 5.3).scale(0.9)
        self.play(
            MoveToTarget(final_eq),
            Create(bx_a), Create(bx_b), Create(bx_r),
            run_time=0.7,
        )

        # Animated parameter sequence 
        self.play(r_tr.animate.set_value(3.2), run_time=0.9)
        self.play(r_tr.animate.set_value(1.0), run_time=0.9)
        self.play(
            a_tr.animate.set_value(-2), b_tr.animate.set_value(-1.5),
            r_tr.animate.set_value(2), run_time=1,
        )
        self.play(
            a_tr.animate.set_value(-2), b_tr.animate.set_value(2.5),
            r_tr.animate.set_value(1.5), run_time=1,
        )
        self.play(
            a_tr.animate.set_value(0), b_tr.animate.set_value(0),
            r_tr.animate.set_value(2), run_time=1,
        )
        self.play(
            a_tr.animate.set_value(2), b_tr.animate.set_value(2),
            r_tr.animate.set_value(2.5), run_time=1,
        )
        self.play(
            a_tr.animate.set_value(1.5), b_tr.animate.set_value(-2),
            r_tr.animate.set_value(1.2), run_time=1,
        )
        self.play(
            a_tr.animate.set_value(0), b_tr.animate.set_value(0),
            r_tr.animate.set_value(2), run_time=1,
        )
        self.wait(0.5)

        # Fade everything out for CTA 
        self.play(
            *[FadeOut(m) for m in [
                hook, axes2, circle2, center_dot2,
                txt_a, txt_b, txt_r, bx_a, bx_b, bx_r, final_eq,
            ]],
            run_time=0.8,
        )

        # Follow for more
        cta_top = Text(
            "Follow for more", font_size=56, weight=BOLD, color=ACCENT_CYAN
        )
        cta_bot = Text(
            "Physics & Math Explained", font_size=34, color=LIGHT_PURPLE
        )
        cta_group = VGroup(cta_top, cta_bot).arrange(DOWN, buff=0.55)
        cta_group.shift(UP * 2.5)

        # Glow rectangle behind CTA
        cta_glow = RoundedRectangle(
            width=8, height=3.5, corner_radius=0.5,
            fill_color=DEEP_PURPLE, fill_opacity=0.4,
            stroke_color=PRIMARY_PURPLE, stroke_width=4,
        ).move_to(cta_group.get_center())
        cta_glow.set_color_by_gradient(*GRAD_MIX)

        arrow = Arrow(
            cta_group.get_bottom() + DOWN * 0.4,
            cta_group.get_bottom() + DOWN * 1.5,
            color=ACCENT_CYAN,
            stroke_width=14,
            max_tip_length_to_length_ratio=0.28,
        )

        self.play(
            FadeIn(cta_glow, scale=0.9),
            FadeIn(cta_group, shift=DOWN * 0.4, scale=1.05),
            GrowArrow(arrow),
            run_time=0.9,
        )

        # Pulse the CTA once
        self.play(
            cta_group.animate.scale(1.08),
            arrow.animate.shift(DOWN * 0.2),
            rate_func=there_and_back,
            run_time=0.9,
        )

        self.wait(2.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1)
        self.wait(0.5)