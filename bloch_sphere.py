from manim import *
import numpy as np

config.pixel_width  = 1080
config.pixel_height = 1920
config.frame_rate   = 60
config.frame_width  = 9
config.frame_height = 16

# ── TechFlux Palette ──────────────────────────────────────────────────────────
PRIMARY_PURPLE = "#9D4EDD"
LIGHT_PURPLE   = "#C77DFF"
PINK_PURPLE    = "#E0AAFF"
DEEP_PURPLE    = "#7B2CBF"
ACCENT_CYAN    = "#00D9FF"
ACCENT_CYAN2   = "#00C8FF"
BG_COLOR       = "#0a0a0a"

GRAD_PURPLE = [PRIMARY_PURPLE, LIGHT_PURPLE]
GRAD_CYAN   = [ACCENT_CYAN, ACCENT_CYAN2]
GRAD_MIX    = [PRIMARY_PURPLE, ACCENT_CYAN, LIGHT_PURPLE]

STATE_COL   = "#FF79C6"
ZERO_COL    = ACCENT_CYAN
ONE_COL     = LIGHT_PURPLE
EQUATOR_COL = PRIMARY_PURPLE


def bloch_point(theta, phi):
    return np.array([
        np.sin(theta) * np.cos(phi),
        np.sin(theta) * np.sin(phi),
        np.cos(theta),
    ])


def make_great_circle(normal, radius=2.0, col=PRIMARY_PURPLE, opacity=0.4, n=100):
    normal = np.array(normal, dtype=float)
    normal /= np.linalg.norm(normal)
    z_axis = np.array([0.0, 0.0, 1.0])
    pts = []
    for i in range(n + 1):
        ang = 2 * PI * i / n
        v = radius * np.array([np.cos(ang), np.sin(ang), 0.0])
        if np.allclose(normal, z_axis):
            pts.append(v)
        elif np.allclose(normal, -z_axis):
            pts.append(v * np.array([1, -1, 1]))
        else:
            axis  = np.cross(z_axis, normal)
            axis /= np.linalg.norm(axis)
            angle = np.arccos(np.clip(np.dot(z_axis, normal), -1, 1))
            c, s  = np.cos(angle), np.sin(angle)
            ax, ay, az = axis
            t = 1 - c
            R = np.array([
                [t*ax*ax + c,      t*ax*ay - s*az,  t*ax*az + s*ay],
                [t*ax*ay + s*az,   t*ay*ay + c,      t*ay*az - s*ax],
                [t*ax*az - s*ay,   t*ay*az + s*ax,   t*az*az + c   ],
            ])
            pts.append(R @ v)
    line = VMobject(stroke_color=col, stroke_width=1.8, stroke_opacity=opacity)
    line.set_points_as_corners(pts)
    return line


class BlochSphere(ThreeDScene):
    def construct(self):

        # ═════════════════════════════════════════════════════════════════
        #  PHASE 0 — 2D title intro (matches trig / wave style)
        # ═════════════════════════════════════════════════════════════════

        # Branding — added once, persists whole video
        brand = VGroup(
            Text("TechFlux",           font_size=38, weight=BOLD, color=PRIMARY_PURPLE),
            Text("Quantum Explained",  font_size=22, color=ACCENT_CYAN),
        ).arrange(DOWN, buff=0.08, aligned_edge=RIGHT).to_corner(DR, buff=0.45)
        self.add_fixed_in_frame_mobjects(brand)

        # Title at screen center
        title = MathTex(r"\mathbb{B}\text{loch }\mathbb{S}\text{phere}") \
            .scale(1.55).set_stroke(width=2.5).set_color_by_gradient(*GRAD_MIX)
        title.move_to(ORIGIN)
        self.add_fixed_in_frame_mobjects(title)
        self.play(Write(title), run_time=1.2)
        self.wait(0.4)

        # Subtitle below, then fades out
        subtitle = Text("Visualising a qubit's quantum state",
                        font_size=28, color=PINK_PURPLE).set_stroke(width=1)
        subtitle.next_to(title, DOWN, buff=0.4)
        self.add_fixed_in_frame_mobjects(subtitle)
        self.play(FadeIn(subtitle, shift=DOWN * 0.2), run_time=0.55)
        self.wait(0.9)
        self.play(FadeOut(subtitle), run_time=0.35)

        # Title slides to top — same as trig/wave
        self.play(title.animate.scale(0.68).move_to(UP * 6.5), run_time=0.65)
        self.wait(0.2)

        # ═════════════════════════════════════════════════════════════════
        #  PHASE 1 — Build 3D scene
        # ═════════════════════════════════════════════════════════════════
        self.set_camera_orientation(phi=70 * DEGREES, theta=45 * DEGREES)

        sphere = Sphere(radius=2.0, resolution=(28, 28))
        sphere.set_color(DEEP_PURPLE)
        sphere.set_opacity(0.13)
        sphere.set_stroke(width=0)

        equator   = make_great_circle([0, 0, 1], col=EQUATOR_COL, opacity=0.55)
        meridian1 = make_great_circle([0, 1, 0], col=LIGHT_PURPLE, opacity=0.28)
        meridian2 = make_great_circle([1, 0, 0], col=ACCENT_CYAN,  opacity=0.28)

        ax_len = 2.6
        x_ax  = Arrow3D(ORIGIN, ax_len * RIGHT, color=LIGHT_PURPLE, thickness=0.018)
        y_ax  = Arrow3D(ORIGIN, ax_len * UP,    color=LIGHT_PURPLE, thickness=0.018)
        z_ax  = Arrow3D(ORIGIN, ax_len * OUT,   color=LIGHT_PURPLE, thickness=0.018)
        neg_z = DashedLine(ORIGIN, 2.6 * IN, dash_length=0.12,
                           stroke_color=LIGHT_PURPLE, stroke_width=1.5,
                           stroke_opacity=0.35)

        self.play(
            FadeIn(sphere),
            Create(equator), Create(meridian1), Create(meridian2),
            Create(x_ax), Create(y_ax), Create(z_ax), Create(neg_z),
            run_time=1.3,
        )

        # Pole labels — use add_fixed_orientation_mobjects so they face the
        # camera but live in 3D space (avoids the broken-LaTeX glitch)
        lbl_north = Text("|0>", font_size=36, color=ZERO_COL) \
            .set_stroke(width=1.2).move_to(OUT * 2.75 + UP * 0.1)
        lbl_south = Text("|1>", font_size=36, color=ONE_COL) \
            .set_stroke(width=1.2).move_to(IN  * 2.75 + UP * 0.1)
        self.add_fixed_orientation_mobjects(lbl_north, lbl_south)
        self.play(FadeIn(lbl_north), FadeIn(lbl_south), run_time=0.6)

        # ── State vector ──────────────────────────────────────────────────
        theta_tr = ValueTracker(0.0)
        phi_tr   = ValueTracker(0.0)

        def get_state_vec():
            tip = bloch_point(theta_tr.get_value(), phi_tr.get_value()) * 2.0
            return Arrow3D(ORIGIN, tip, color=STATE_COL,
                           thickness=0.045, base_radius=0.045)

        def get_tip_dot():
            tip = bloch_point(theta_tr.get_value(), phi_tr.get_value()) * 2.0
            return Dot3D(tip, color=STATE_COL, radius=0.12)

        def get_proj_line():
            tip  = bloch_point(theta_tr.get_value(), phi_tr.get_value()) * 2.0
            proj = np.array([tip[0], tip[1], 0.0])
            return DashedLine(proj, tip, dash_length=0.1,
                              stroke_color=STATE_COL, stroke_width=2.5,
                              stroke_opacity=0.5)

        state_vec = always_redraw(get_state_vec)
        tip_dot   = always_redraw(get_tip_dot)
        proj_line = always_redraw(get_proj_line)
        self.add(state_vec, tip_dot, proj_line)

        # State equation — fixed 2D, bottom
        state_eq = MathTex(
            r"|\psi\rangle = \cos\tfrac{\theta}{2}|0\rangle"
            r"+ e^{i\phi}\sin\tfrac{\theta}{2}|1\rangle",
            font_size=33,
        ).set_stroke(width=1.4).set_color_by_gradient(*GRAD_MIX).move_to(DOWN * 5.1)
        self.add_fixed_in_frame_mobjects(state_eq)
        self.play(Write(state_eq), run_time=1.0)
        self.wait(0.3)

        # ── Section label helper ──────────────────────────────────────────
        _sec = [None]
        SEC_POS = UP * 5.5

        def set_section(text, color=ACCENT_CYAN):
            new = Text(text, font_size=29, weight=BOLD, color=color).move_to(SEC_POS)
            self.add_fixed_in_frame_mobjects(new)
            anims = [FadeIn(new, shift=DOWN * 0.1)]
            if _sec[0] is not None:
                anims.append(FadeOut(_sec[0]))
            self.play(*anims, run_time=0.4)
            _sec[0] = new

        def clear_section():
            if _sec[0] is not None:
                self.play(FadeOut(_sec[0]), run_time=0.3)
                _sec[0] = None

        # ═════════════════════════════════════════════════════════════════
        #  ACTS
        # ═════════════════════════════════════════════════════════════════
        self.begin_ambient_camera_rotation(rate=0.18)

        set_section("|0>  —  North Pole", ZERO_COL)
        self.wait(1.6)

        set_section("|1>  —  South Pole", ONE_COL)
        self.play(theta_tr.animate.set_value(PI), run_time=1.8, rate_func=smooth)
        self.wait(1.2)

        set_section("|+>  =  (|0> + |1>) / sqrt(2)", ACCENT_CYAN)
        self.play(theta_tr.animate.set_value(PI / 2),
                  phi_tr.animate.set_value(0),
                  run_time=1.4, rate_func=smooth)
        self.wait(1.1)

        set_section("Sweeping phase  phi  around equator", LIGHT_PURPLE)
        self.play(phi_tr.animate.set_value(2 * PI),
                  run_time=3.5, rate_func=linear)
        self.wait(0.4)

        # X gate
        set_section("X Gate  —  pi rotation about X axis", PINK_PURPLE)
        self.play(theta_tr.animate.set_value(0),
                  phi_tr.animate.set_value(0), run_time=0.8)
        self.wait(0.3)
        x_note = MathTex(r"X|0\rangle = |1\rangle", font_size=36, color=PINK_PURPLE) \
            .set_stroke(width=1.4).move_to(DOWN * 6.1)
        self.add_fixed_in_frame_mobjects(x_note)
        self.play(FadeIn(x_note, shift=UP * 0.1), run_time=0.35)
        self.play(theta_tr.animate.set_value(PI),
                  phi_tr.animate.set_value(PI / 2),
                  run_time=1.8, rate_func=smooth)
        self.wait(0.7)
        self.play(FadeOut(x_note), run_time=0.3)

        # Hadamard
        set_section("H Gate  —  Hadamard", ACCENT_CYAN)
        self.play(theta_tr.animate.set_value(0),
                  phi_tr.animate.set_value(0), run_time=0.8)
        self.wait(0.3)
        h_note = MathTex(r"H|0\rangle = |{+}\rangle", font_size=36, color=ACCENT_CYAN) \
            .set_stroke(width=1.4).move_to(DOWN * 6.1)
        self.add_fixed_in_frame_mobjects(h_note)
        self.play(FadeIn(h_note, shift=UP * 0.1), run_time=0.35)
        self.play(theta_tr.animate.set_value(PI / 2),
                  run_time=1.4, rate_func=smooth)
        self.wait(0.8)
        self.play(FadeOut(h_note), run_time=0.3)

        # Precession
        set_section("Qubit precessing...", LIGHT_PURPLE)
        self.play(theta_tr.animate.set_value(PI * 0.3),
                  phi_tr.animate.set_value(4 * PI),
                  run_time=4.0, rate_func=linear)
        self.wait(0.3)
        clear_section()

        # ═════════════════════════════════════════════════════════════════
        #  SUMMARY CARDS — one at a time, no overlap
        # ═════════════════════════════════════════════════════════════════
        self.stop_ambient_camera_rotation()
        self.move_camera(phi=65 * DEGREES, theta=30 * DEGREES,
                         run_time=0.9, rate_func=smooth)

        self.play(
            FadeOut(sphere, equator, meridian1, meridian2,
                    x_ax, y_ax, z_ax, neg_z,
                    state_vec, tip_dot, proj_line,
                    lbl_north, lbl_south, state_eq),
            run_time=0.8,
        )

        sum_title = Text("The Bloch Sphere",
                         font_size=46, weight=BOLD, color=ACCENT_CYAN).move_to(UP * 5.5)
        self.add_fixed_in_frame_mobjects(sum_title)
        self.play(FadeIn(sum_title, shift=DOWN * 0.2), run_time=0.5)

        def make_card(top_tex, note, top_col, note_col, grad, pos, is_math=True):
            top = (MathTex(top_tex, font_size=31, color=top_col).set_stroke(width=1.3)
                   if is_math else
                   Text(top_tex, font_size=27, weight=BOLD, color=top_col))
            bot = Text(note, font_size=22, color=note_col)
            grp = VGroup(top, bot).arrange(DOWN, buff=0.18).move_to(pos)
            bg  = RoundedRectangle(
                width=7.8, height=1.65, corner_radius=0.28,
                fill_color=DEEP_PURPLE, fill_opacity=0.45, stroke_width=3,
            ).set_color_by_gradient(*grad).move_to(pos)
            return VGroup(bg, grp)

        positions = [UP * 3.3, UP * 1.25, DOWN * 0.8, DOWN * 2.85]
        cards_info = [
            (r"|\psi\rangle = \alpha|0\rangle + \beta|1\rangle",
             "Qubit: superposition of |0> and |1>",
             ACCENT_CYAN, PINK_PURPLE, GRAD_CYAN, True),
            (r"\theta \in [0,\pi],\;\; \phi \in [0, 2\pi]",
             "Every pure state lives on the sphere",
             LIGHT_PURPLE, PINK_PURPLE, GRAD_PURPLE, True),
            ("X, Y, Z gates = rotations",
             "Quantum gates rotate the state vector",
             PRIMARY_PURPLE, PINK_PURPLE, GRAD_MIX, False),
            (r"|\langle\psi|\phi\rangle|^2 = \cos^2\!\tfrac{\delta}{2}",
             "Antipodal points = orthogonal states",
             ACCENT_CYAN, PINK_PURPLE, [ACCENT_CYAN, PRIMARY_PURPLE], True),
        ]

        all_cards = []
        for (top_tex, note, tc, nc, grad, is_math), pos in zip(cards_info, positions):
            card = make_card(top_tex, note, tc, nc, grad, pos, is_math)
            # Add to fixed frame individually, right before animating in
            self.add_fixed_in_frame_mobjects(card)
            self.play(FadeIn(card, shift=RIGHT * 0.2, scale=0.95), run_time=0.5)
            self.wait(0.25)
            all_cards.append(card)

        self.wait(1.0)

        # ═════════════════════════════════════════════════════════════════
        #  FOLLOW FOR MORE
        # ═════════════════════════════════════════════════════════════════
        self.play(FadeOut(sum_title, *all_cards), run_time=0.7)

        cta = VGroup(
            Text("Follow for more",             font_size=54, weight=BOLD, color=ACCENT_CYAN),
            Text("Quantum & Physics Explained", font_size=31, color=LIGHT_PURPLE),
        ).arrange(DOWN, buff=0.5).move_to(UP * 2.5)

        cta_glow = RoundedRectangle(
            width=8.4, height=3.6, corner_radius=0.55,
            fill_color=DEEP_PURPLE, fill_opacity=0.38, stroke_width=4,
        ).set_color_by_gradient(*GRAD_MIX).move_to(cta)

        arrow = Arrow(
            cta.get_bottom() + DOWN * 0.35,
            cta.get_bottom() + DOWN * 1.55,
            color=ACCENT_CYAN, stroke_width=14,
            max_tip_length_to_length_ratio=0.26,
        )

        self.add_fixed_in_frame_mobjects(cta_glow, cta, arrow)
        self.play(
            FadeIn(cta_glow, scale=0.92),
            FadeIn(cta, shift=DOWN * 0.35, scale=1.04),
            GrowArrow(arrow),
            run_time=0.85,
        )
        self.play(
            cta.animate.scale(1.07),
            arrow.animate.shift(DOWN * 0.18),
            rate_func=there_and_back,
            run_time=0.85,
        )
        self.wait(2.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1)
        self.wait(0.4)