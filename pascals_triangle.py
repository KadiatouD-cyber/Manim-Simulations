from manim import *
import numpy as np

config.pixel_width  = 1080
config.pixel_height = 1920
config.frame_rate   = 60
config.frame_width  = 9
config.frame_height = 16

# TechFlux Palette 
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
GRAD_MIX2   = [ACCENT_CYAN, PRIMARY_PURPLE]


def pascal_row(n):
    row = [1]
    for k in range(1, n + 1):
        row.append(row[-1] * (n - k + 1) // k)
    return row


def get_cell_color(value, row_idx, num_rows):
    """Color by divisibility for the Sierpinski reveal."""
    if value % 2 == 0:
        return DEEP_PURPLE
    # Odd numbers get a gradient based on row position
    t = row_idx / max(num_rows - 1, 1)
    r1 = np.array([0x9D, 0x4E, 0xDD]) / 255
    r2 = np.array([0x00, 0xD9, 0xFF]) / 255
    c = (1 - t) * r1 + t * r2
    return rgb_to_color(c)


class PascalsTriangle(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        NUM_ROWS = 12   # rows shown in main triangle
        CELL_W   = 0.58
        CELL_H   = 0.58
        ROW_GAP  = 0.62

        # branding
        brand = VGroup(
            Text("TechFlux",          font_size=38, weight=BOLD, color=PRIMARY_PURPLE),
            Text("Math Explained",    font_size=22, color=ACCENT_CYAN),
        ).arrange(DOWN, buff=0.08, aligned_edge=RIGHT).to_corner(DR, buff=0.45)
        self.add(brand)

        # Hook title
        title = MathTex(
            r"\mathbb{P}\text{ascal's }\mathbb{T}\text{riangle}"
        ).scale(1.55).set_stroke(width=2.5).set_color_by_gradient(*GRAD_MIX)
        title.move_to(UP * 1)

        self.play(Write(title), run_time=1.1)
        self.wait(0.3)
        self.play(title.animate.move_to(UP * 6.8).scale(0.72), run_time=0.65)

        # Build all Pascal rows
        all_rows_data = [pascal_row(n) for n in range(NUM_ROWS)]

        # Pre-compute positions: triangle centered, shifted up a bit
        TRIANGLE_TOP = UP * 5.5

        def cell_pos(row_i, col_i):
            total_width = row_i * CELL_W
            x = (col_i - row_i / 2) * CELL_W
            y = -row_i * ROW_GAP
            return TRIANGLE_TOP + np.array([x, y, 0])

        # Animate rows appearing one by one
        all_cells   = []   # list of lists of VGroups (bg + text)
        all_add_anims = []

        for row_i, row_data in enumerate(all_rows_data):
            row_cells = []
            row_anims = []
            for col_i, val in enumerate(row_data):
                pos = cell_pos(row_i, col_i)

                # Hexagon cell background
                hex_bg = RegularPolygon(
                    n=6, radius=CELL_W * 0.46,
                    stroke_width=2.5, fill_opacity=0.18,
                ).move_to(pos)
                hex_bg.set_color_by_gradient(*GRAD_MIX)
                hex_bg.set_fill(DEEP_PURPLE, opacity=0.18)

                # Number label — scale down font for large numbers
                font = 22 if val > 999 else (26 if val > 99 else 30)
                num_tex = Text(str(val), font_size=font,
                               color=PINK_PURPLE, weight=BOLD).move_to(pos)

                cell = VGroup(hex_bg, num_tex)
                row_cells.append(cell)
                row_anims.append(FadeIn(cell, scale=0.7))

            all_cells.append(row_cells)
            all_add_anims.append(row_anims)

        # Play row-by-row with connection lines 
        connection_lines = VGroup()

        for row_i in range(NUM_ROWS):
            self.play(
                AnimationGroup(*all_add_anims[row_i], lag_ratio=0.06),
                run_time=max(0.25, 0.55 - row_i * 0.025),
            )

            # Draw lines connecting to next row's cells (after row 0)
            if row_i > 0:
                for col_i in range(len(all_rows_data[row_i])):
                    child_pos = cell_pos(row_i, col_i)
                    # parent left
                    if col_i > 0:
                        parent_pos = cell_pos(row_i - 1, col_i - 1)
                        line = Line(
                            parent_pos + DOWN * 0.23,
                            child_pos  + UP   * 0.23,
                            stroke_width=1.2, stroke_opacity=0.28,
                        ).set_color_by_gradient(ACCENT_CYAN, PRIMARY_PURPLE)
                        connection_lines.add(line)
                    # parent right
                    if col_i < len(all_rows_data[row_i]) - 1:
                        parent_pos = cell_pos(row_i - 1, col_i)
                        line = Line(
                            parent_pos + DOWN * 0.23,
                            child_pos  + UP   * 0.23,
                            stroke_width=1.2, stroke_opacity=0.28,
                        ).set_color_by_gradient(PRIMARY_PURPLE, ACCENT_CYAN)
                        connection_lines.add(line)

        # Add all connection lines subtly after triangle is built
        self.play(FadeIn(connection_lines, lag_ratio=0.002), run_time=0.9)
        self.wait(0.5)

        # ACT 1: Highlight row sums = powers of 2 
        sec_label = Text("Row sums = Powers of 2",
                         font_size=33, weight=BOLD, color=ACCENT_CYAN).move_to(DOWN * 6.3)
        self.play(FadeIn(sec_label, shift=UP * 0.15), run_time=0.45)

        sum_labels = VGroup()
        for row_i, row_data in enumerate(all_rows_data):
            total = sum(row_data)
            pos   = cell_pos(row_i, len(row_data) - 1) + RIGHT * 0.85
            exp   = row_i
            lbl   = MathTex(f"= 2^{{{exp}}}", font_size=22, color=ACCENT_CYAN)\
                        .move_to(pos).set_stroke(width=1.2)
            sum_labels.add(lbl)

            # Flash the whole row
            flash_anims = [
                cell[0].animate.set_fill(ACCENT_CYAN, opacity=0.45)
                for cell in all_cells[row_i]
            ]
            self.play(
                *flash_anims,
                FadeIn(lbl, shift=RIGHT * 0.1),
                run_time=0.18,
            )

        self.wait(0.6)

        # Fade row highlights back
        unfade = []
        for row_i in range(NUM_ROWS):
            for cell in all_cells[row_i]:
                unfade.append(cell[0].animate.set_fill(DEEP_PURPLE, opacity=0.18))
        self.play(*unfade, FadeOut(sum_labels), FadeOut(sec_label), run_time=0.55)

        #  ACT 2: Highlight diagonals
        sec2 = Text("Hidden diagonals",
                    font_size=33, weight=BOLD, color=LIGHT_PURPLE).move_to(DOWN * 6.3)
        self.play(FadeIn(sec2, shift=UP * 0.15), run_time=0.4)

        # Natural numbers diagonal (col index 1)
        nat_cells  = [all_cells[r][1] for r in range(1, NUM_ROWS)]
        nat_label  = Text("Natural numbers", font_size=26, color=LIGHT_PURPLE)\
                         .move_to(DOWN * 5.7)
        self.play(
            *[c[0].animate.set_fill(LIGHT_PURPLE, opacity=0.55) for c in nat_cells],
            *[c[1].animate.set_color(WHITE) for c in nat_cells],
            FadeIn(nat_label, shift=UP * 0.1),
            run_time=0.5,
        )
        self.wait(0.7)
        self.play(
            *[c[0].animate.set_fill(DEEP_PURPLE, opacity=0.18) for c in nat_cells],
            *[c[1].animate.set_color(PINK_PURPLE) for c in nat_cells],
            FadeOut(nat_label),
            run_time=0.4,
        )

        # Triangular numbers diagonal (col index 2)
        tri_cells = [all_cells[r][2] for r in range(2, NUM_ROWS)]
        tri_label = Text("Triangular numbers", font_size=26, color=PRIMARY_PURPLE)\
                        .move_to(DOWN * 5.7)
        self.play(
            *[c[0].animate.set_fill(PRIMARY_PURPLE, opacity=0.6) for c in tri_cells],
            *[c[1].animate.set_color(WHITE) for c in tri_cells],
            FadeIn(tri_label, shift=UP * 0.1),
            run_time=0.5,
        )
        self.wait(0.7)
        self.play(
            *[c[0].animate.set_fill(DEEP_PURPLE, opacity=0.18) for c in tri_cells],
            *[c[1].animate.set_color(PINK_PURPLE) for c in tri_cells],
            FadeOut(tri_label),
            FadeOut(sec2),
            run_time=0.4,
        )

        # ACT 3: Sierpinski — color odd vs even
        sec3 = Text("Mod 2  →  Sierpiński Triangle",
                    font_size=31, weight=BOLD, color=ACCENT_CYAN).move_to(DOWN * 6.3)
        self.play(FadeIn(sec3, shift=UP * 0.15), run_time=0.45)

        sierpinski_anims = []
        for row_i, row_data in enumerate(all_rows_data):
            for col_i, val in enumerate(row_data):
                cell = all_cells[row_i][col_i]
                if val % 2 == 0:
                    # Even — nearly invisible (Sierpinski hole)
                    sierpinski_anims.append(
                        cell[0].animate.set_fill(BG_COLOR, opacity=0.0)
                    )
                    sierpinski_anims.append(
                        cell[0].animate.set_stroke(opacity=0.08)
                    )
                    sierpinski_anims.append(
                        cell[1].animate.set_opacity(0.05)
                    )
                else:
                    # Odd — bright, gradient by row
                    t   = row_i / (NUM_ROWS - 1)
                    r1  = np.array([0x9D, 0x4E, 0xDD]) / 255
                    r2  = np.array([0x00, 0xD9, 0xFF]) / 255
                    col = rgb_to_color((1 - t) * r1 + t * r2)
                    sierpinski_anims.append(
                        cell[0].animate.set_fill(col, opacity=0.75)
                    )
                    sierpinski_anims.append(
                        cell[0].animate.set_stroke(color=col, opacity=1.0)
                    )
                    sierpinski_anims.append(
                        cell[1].animate.set_color(WHITE).set_opacity(1.0)
                    )

        self.play(
            AnimationGroup(*sierpinski_anims, lag_ratio=0.008),
            run_time=2.2,
        )
        self.wait(0.6)

        sier_note = Text(
            "Odd entries form a fractal!",
            font_size=28, weight=BOLD, color=PINK_PURPLE
        ).move_to(DOWN * 5.7)
        self.play(FadeIn(sier_note, shift=UP * 0.1), run_time=0.4)
        self.wait(1.2)

        # Fade everything for summary cards
        everything = VGroup(
            *[c for row in all_cells for c in row],
            connection_lines, sec3, sier_note,
        )
        self.play(FadeOut(everything), run_time=0.8)

        # Summary cards 
        sum_title = Text("Pascal's Secrets",
                         font_size=48, weight=BOLD, color=ACCENT_CYAN).move_to(UP * 5.2)
        self.play(FadeIn(sum_title, shift=DOWN * 0.2), run_time=0.5)

        def info_card(top_tex, note, top_col, note_col, grad, pos, is_math=True):
            top = MathTex(top_tex, font_size=34, color=top_col).set_stroke(width=1.4)\
                if is_math else \
                Text(top_tex, font_size=30, weight=BOLD, color=top_col)
            bot = Text(note, font_size=24, color=note_col)
            grp = VGroup(top, bot).arrange(DOWN, buff=0.18)
            bg  = RoundedRectangle(
                width=7.8, height=1.65, corner_radius=0.28,
                fill_color=DEEP_PURPLE, fill_opacity=0.45, stroke_width=3,
            ).set_color_by_gradient(*grad).move_to(grp)
            return VGroup(bg, grp).move_to(pos)

        cards = [
            info_card(
                r"\binom{n}{k} = \binom{n-1}{k-1} + \binom{n-1}{k}",
                "Each cell = sum of two above",
                ACCENT_CYAN, PINK_PURPLE, GRAD_CYAN, UP * 3.2,
            ),
            info_card(
                r"\text{Row } n \text{ sum} = 2^n",
                "Row sums are powers of 2",
                LIGHT_PURPLE, PINK_PURPLE, GRAD_PURPLE, UP * 1.2,
            ),
            info_card(
                r"(a+b)^n = \sum_{k=0}^{n}\binom{n}{k}a^k b^{n-k}",
                "Binomial theorem coefficients",
                PRIMARY_PURPLE, PINK_PURPLE, GRAD_MIX, DOWN * 0.8,
            ),
            info_card(
                "Mod 2  →  Sierpiński fractal", "",
                ACCENT_CYAN, PINK_PURPLE,
                [ACCENT_CYAN, PRIMARY_PURPLE], DOWN * 2.55, is_math=False,
            ),
        ]

        for card in cards:
            self.play(FadeIn(card, shift=RIGHT * 0.2, scale=0.95), run_time=0.5)
            self.wait(0.25)

        self.wait(1.0)

        # Follow for more 
        self.play(
            FadeOut(sum_title, *cards),
            run_time=0.7,
        )

        cta = VGroup(
            Text("Follow for more",          font_size=56, weight=BOLD, color=ACCENT_CYAN),
            Text("Math & Physics Explained", font_size=34, color=LIGHT_PURPLE),
        ).arrange(DOWN, buff=0.5).move_to(UP * 2.5)

        cta_glow = RoundedRectangle(
            width=8.4, height=3.6, corner_radius=0.55,
            fill_color=DEEP_PURPLE, fill_opacity=0.38,
            stroke_width=4,
        ).set_color_by_gradient(*GRAD_MIX).move_to(cta)

        arrow = Arrow(
            cta.get_bottom() + DOWN * 0.35,
            cta.get_bottom() + DOWN * 1.55,
            color=ACCENT_CYAN, stroke_width=14,
            max_tip_length_to_length_ratio=0.26,
        )

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