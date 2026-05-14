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

CART_A_COL  = ACCENT_CYAN
CART_B_COL  = LIGHT_PURPLE
MOM_A_COL   = ACCENT_CYAN
MOM_B_COL   = "#FF79C6"
TOTAL_COL   = "#FFD700"


class ConservationOfMomentum(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        # Branding
        brand = VGroup(
            Text("TechFlux",          font_size=38, weight=BOLD, color=PRIMARY_PURPLE),
            Text("Physics Explained", font_size=20, color=ACCENT_CYAN),
        ).arrange(DOWN, buff=0.08, aligned_edge=RIGHT).to_corner(DR, buff=0.4)
        self.add(brand)

      
        #  hook title
        
        TITLE_Y = UP * 6.75

        hook = VGroup(
            MathTex(r"\mathbb{C}\text{onservation of}", font_size=48)
                .set_color_by_gradient(*GRAD_CYAN),
            MathTex(r"\mathbb{M}\text{omentum}", font_size=56)
                .set_color_by_gradient(*GRAD_PURPLE),
        ).arrange(DOWN, buff=0.1).set_stroke(width=2.5).move_to(ORIGIN)

        self.play(Write(hook), run_time=1.1)
        self.wait(0.3)

        sub = Text("What happens when objects collide?",
                   font_size=27, color=PINK_PURPLE).set_stroke(width=1)
        sub.next_to(hook, DOWN, buff=0.3)
        self.play(FadeIn(sub, shift=DOWN * 0.2), run_time=0.55)
        self.wait(1.1)
        self.play(FadeOut(sub, shift=UP * 0.2), run_time=0.3)
        self.play(hook.animate.scale(0.62).move_to(TITLE_Y), run_time=0.65)

        # Section label helper
        SEC_Y = UP * 5.4
        _sec  = [None]
        def set_sec(txt, col=ACCENT_CYAN):
            new = Text(txt, font_size=31, weight=BOLD, color=col).move_to(SEC_Y)
            anims = [FadeIn(new, shift=DOWN * 0.1)]
            if _sec[0]: anims.append(FadeOut(_sec[0], shift=UP * 0.1))
            self.play(*anims, run_time=0.4)
            _sec[0] = new

        def clear_sec():
            if _sec[0]:
                self.play(FadeOut(_sec[0], shift=UP * 0.1), run_time=0.3)
                _sec[0] = None

        #  MOMENTUM DEFINITION
    
        set_sec("What is momentum?", ACCENT_CYAN)

        p_def = MathTex(r"\vec{p}", r"=", r"m", r"\vec{v}",
                        font_size=88).set_stroke(width=2).move_to(UP * 2.5)
        p_def[0].set_color(TOTAL_COL)
        p_def[2].set_color(CART_A_COL)
        p_def[3].set_color(CART_B_COL)

        p_fill = SurroundingRectangle(p_def, corner_radius=0.3, buff=0.3,
            stroke_width=0, fill_color=DEEP_PURPLE, fill_opacity=0.42)
        p_box  = SurroundingRectangle(p_def, corner_radius=0.3, buff=0.3,
            stroke_width=5).set_color_by_gradient(*GRAD_MIX)

        desc1 = Text("mass  ×  velocity", font_size=34, color=PINK_PURPLE)\
            .next_to(p_def, DOWN, buff=0.55)
        desc2 = Text("a vector quantity", font_size=28, color=LIGHT_PURPLE)\
            .next_to(desc1, DOWN, buff=0.25)

        self.play(Write(p_def), run_time=0.9)
        self.play(FadeIn(p_fill), Create(p_box), run_time=0.4)
        self.play(FadeIn(desc1, shift=DOWN * 0.15),
                  FadeIn(desc2, shift=DOWN * 0.15), run_time=0.5)
        self.wait(1.2)
        self.play(FadeOut(p_def, p_fill, p_box, desc1, desc2), run_time=0.5)

    
        #  The law
      
        set_sec("The Law", ACCENT_CYAN)

        law_eq = MathTex(
            r"\vec{p}_{\text{total}}",
            r"=",
            r"m_1\vec{v}_1 + m_2\vec{v}_2",
            r"= \text{const}",
            font_size=46,
        ).set_stroke(width=1.8).move_to(UP * 2.8)
        law_eq[0].set_color(TOTAL_COL)
        law_eq[2].set_color_by_gradient(CART_A_COL, CART_B_COL)
        law_eq[3].set_color(PINK_PURPLE)

        law_fill = SurroundingRectangle(law_eq, corner_radius=0.25, buff=0.25,
            stroke_width=0, fill_color=DEEP_PURPLE, fill_opacity=0.42)
        law_box  = SurroundingRectangle(law_eq, corner_radius=0.25, buff=0.25,
            stroke_width=4).set_color_by_gradient(*GRAD_MIX)

        self.play(Write(law_eq), run_time=1.0)
        self.play(FadeIn(law_fill), Create(law_box), run_time=0.4)

        newton = Text("← Newton's 3rd Law guarantees this",
                      font_size=24, color=PINK_PURPLE)\
            .next_to(law_eq, DOWN, buff=0.5)
        self.play(FadeIn(newton, shift=DOWN * 0.1), run_time=0.5)
        self.wait(1.2)
        self.play(FadeOut(law_eq, law_fill, law_box, newton), run_time=0.5)

        #  shared scene elements (track + carts)
        
        TRACK_Y = UP * 1.2      # vertical centre of track
        TRACK_W = 8.0

        def make_track():
            rail   = Line(LEFT * TRACK_W/2, RIGHT * TRACK_W/2,
                          color=LIGHT_PURPLE, stroke_width=4,
                          stroke_opacity=0.6).move_to(TRACK_Y + DOWN * 0.55)
            shadow = Line(LEFT * TRACK_W/2, RIGHT * TRACK_W/2,
                          color=DEEP_PURPLE, stroke_width=8,
                          stroke_opacity=0.25).move_to(TRACK_Y + DOWN * 0.60)
            return VGroup(shadow, rail)

        def make_cart(label_tex, mass_str, body_col, x_pos):
            body  = RoundedRectangle(width=1.5, height=1.0, corner_radius=0.15,
                fill_color=body_col, fill_opacity=1,
                stroke_color=WHITE, stroke_width=2)
            shine = RoundedRectangle(width=1.2, height=0.25, corner_radius=0.08,
                fill_color=WHITE, fill_opacity=0.15, stroke_width=0)\
                .move_to(body.get_top() + DOWN * 0.2)

            mass_lbl = MathTex(mass_str, font_size=30, color=WHITE)\
                .set_stroke(width=1.2).move_to(body)

            w1 = Circle(radius=0.18, fill_color="#222", fill_opacity=1,
                        stroke_color=LIGHT_PURPLE, stroke_width=3)\
                .move_to(body.get_bottom() + LEFT * 0.42 + DOWN * 0.05)
            w2 = w1.copy().move_to(body.get_bottom() + RIGHT * 0.42 + DOWN * 0.05)
            hub1 = Dot(w1.get_center(), radius=0.06, color=LIGHT_PURPLE)
            hub2 = Dot(w2.get_center(), radius=0.06, color=LIGHT_PURPLE)

            cart = VGroup(body, shine, mass_lbl, w1, w2, hub1, hub2)
            cart.move_to(TRACK_Y + RIGHT * x_pos)
            return cart

        def make_velocity_arrow(cart, v, col, label_tex):
            if abs(v) < 0.001:
                return VGroup()
            direction = RIGHT if v > 0 else LEFT
            length    = min(abs(v) * 0.55, 2.2)
            start     = cart.get_right() if v > 0 else cart.get_left()
            end       = start + direction * length
            arr = Arrow(start, end, color=col, stroke_width=7,
                        buff=0, max_tip_length_to_length_ratio=0.22)
            lbl = MathTex(label_tex, font_size=30, color=col)\
                .set_stroke(width=1.2).next_to(arr, UP, buff=0.1)
            return VGroup(arr, lbl)

        def momentum_bar(value, max_val, col, label_tex, center):
            """Horizontal momentum bar."""
            bar_w = min(abs(value) / max_val * 3.2, 3.2)
            bar   = Rectangle(width=bar_w, height=0.38,
                fill_color=col, fill_opacity=0.9, stroke_width=0)\
                .move_to(center)
            outline = Rectangle(width=3.4, height=0.38,
                fill_opacity=0, stroke_color=col,
                stroke_width=2, stroke_opacity=0.5).move_to(center)
            lbl = MathTex(label_tex, font_size=26, color=col)\
                .set_stroke(width=1.2).next_to(outline, LEFT, buff=0.15)
            val_lbl = MathTex(rf"{value:+.1f}", font_size=24, color=WHITE)\
                .next_to(outline, RIGHT, buff=0.15)
            return VGroup(outline, bar, lbl, val_lbl)

       
        #  act 1 — ELASTIC COLLISION
        #  m1=2 kg, v1=+3 m/s   m2=2 kg, v2=0
        #  After: v1'=0, v2'=+3  (equal masses → complete transfer)
    
        set_sec("Elastic Collision", ACCENT_CYAN)

        track = make_track()
        self.play(Create(track), run_time=0.5)

        m1, v1i = 2.0,  3.0
        m2, v2i = 2.0,  0.0
        v1f =  0.0
        v2f =  3.0
        p_total = m1*v1i + m2*v2i   # = 6

        # Initial positions
        cart_a = make_cart(r"A", r"m_1{=}2\text{kg}", CART_A_COL, -2.8)
        cart_b = make_cart(r"B", r"m_2{=}2\text{kg}", CART_B_COL,  2.5)

        arr_a = make_velocity_arrow(cart_a,  v1i, MOM_A_COL, r"v_1=3\,\frac{m}{s}")
        arr_b = make_velocity_arrow(cart_b,  v2i, MOM_B_COL, r"v_2=0")

        self.play(FadeIn(cart_a, shift=LEFT*0.3),
                  FadeIn(cart_b, shift=RIGHT*0.3), run_time=0.6)
        self.play(FadeIn(arr_a), FadeIn(arr_b), run_time=0.5)

        # Momentum bars — before
        BAR1_Y = DOWN * 2.05
        BAR2_Y = DOWN * 2.65
        BAR3_Y = DOWN * 3.35

        bar_p1_before = momentum_bar(m1*v1i, p_total, MOM_A_COL,
                                     r"p_1", BAR1_Y + LEFT*0.5)
        bar_p2_before = momentum_bar(m2*v2i, p_total, MOM_B_COL,
                                     r"p_2", BAR2_Y + LEFT*0.5)

        # total bar
        sep_line = Line(LEFT*4, RIGHT*4, stroke_width=1,
                        color=LIGHT_PURPLE, stroke_opacity=0.4).move_to(BAR3_Y + UP*0.25)
        bar_total = momentum_bar(p_total, p_total, TOTAL_COL,
                                 r"p_{\text{tot}}", BAR3_Y + LEFT*0.5)

        before_lbl = Text("BEFORE", font_size=24, weight=BOLD, color=PINK_PURPLE)\
            .move_to(DOWN * 1.55)

        self.play(
            FadeIn(before_lbl),
            FadeIn(bar_p1_before), FadeIn(bar_p2_before),
            FadeIn(sep_line), FadeIn(bar_total),
            run_time=0.7,
        )
        self.wait(0.7)

        # Collision animation 
        self.play(FadeOut(arr_a, arr_b), run_time=0.2)

        # Cart A slides right
        self.play(
            cart_a.animate.move_to(TRACK_Y + RIGHT * 0.85),
            run_time=1.0, rate_func=linear,
        )

        # Impact flash
        impact_flash = Circle(radius=0.5, color=TOTAL_COL,
                              fill_color=TOTAL_COL, fill_opacity=0.6,
                              stroke_width=0)\
            .move_to(TRACK_Y + RIGHT * 0.85)
        self.play(FadeIn(impact_flash, scale=0.3), run_time=0.1)
        self.play(FadeOut(impact_flash, scale=2.5), run_time=0.25)

        # Post-collision: A stops, B moves right
        arr_a_after = make_velocity_arrow(cart_a,  v1f, MOM_A_COL, r"v_1'=0")
        arr_b_after = make_velocity_arrow(
            cart_b.copy().move_to(TRACK_Y + RIGHT * 0.85 + RIGHT * 1.15),
            v2f, MOM_B_COL, r"v_2'=3\,\frac{m}{s}")

        self.play(
            cart_b.animate.move_to(TRACK_Y + RIGHT * 3.2),
            run_time=1.1, rate_func=linear,
        )

        after_lbl = Text("AFTER", font_size=24, weight=BOLD, color=PINK_PURPLE)\
            .move_to(DOWN * 1.55)

        bar_p1_after = momentum_bar(m1*v1f, p_total, MOM_A_COL,
                                    r"p_1'", BAR1_Y + LEFT*0.5)
        bar_p2_after = momentum_bar(m2*v2f, p_total, MOM_B_COL,
                                    r"p_2'", BAR2_Y + LEFT*0.5)
        bar_total_after = momentum_bar(p_total, p_total, TOTAL_COL,
                                       r"p_{\text{tot}}'", BAR3_Y + LEFT*0.5)

        self.play(
            ReplacementTransform(before_lbl, after_lbl),
            ReplacementTransform(bar_p1_before, bar_p1_after),
            ReplacementTransform(bar_p2_before, bar_p2_after),
            ReplacementTransform(bar_total, bar_total_after),
            FadeIn(arr_b_after),
            run_time=0.7,
        )

        # Highlight total unchanged
        conserved_note = Text("Total momentum unchanged! ✓",
                              font_size=28, weight=BOLD, color=TOTAL_COL)\
            .move_to(DOWN * 4.35)
        self.play(FadeIn(conserved_note, shift=DOWN*0.1), run_time=0.4)

        # Flash total bar
        self.play(bar_total_after[1].animate.set_fill(opacity=1.0),
                  run_time=0.2, rate_func=there_and_back)
        self.wait(1.2)

        # Clear elastic scene
        self.play(
            FadeOut(track, cart_a, cart_b, arr_b_after,
                    after_lbl, bar_p1_after, bar_p2_after,
                    sep_line, bar_total_after, conserved_note),
            run_time=0.6,
        )

        
        #  Act 2 — PERFECTLY INELASTIC COLLISION
        #  m1=3 kg, v1=+4 m/s   m2=1 kg, v2=−1 m/s
        #  They stick together → v_f = (m1v1+m2v2)/(m1+m2) = (12−1)/4 = 2.75

        set_sec("Perfectly Inelastic", LIGHT_PURPLE)

        m1, v1i = 3.0,  4.0
        m2, v2i = 1.0, -1.0
        p_tot2  = m1*v1i + m2*v2i   # = 11
        vf      = p_tot2 / (m1 + m2) # = 2.75

        track2 = make_track()
        self.play(Create(track2), run_time=0.4)

        cart2_a = make_cart(r"A", r"m_1{=}3", CART_A_COL, -2.5)
        cart2_b = make_cart(r"B", r"m_2{=}1", CART_B_COL,  2.2)

        arr2_a = make_velocity_arrow(cart2_a, v1i, MOM_A_COL,
                                     r"v_1=+4\,\frac{m}{s}")
        arr2_b = make_velocity_arrow(cart2_b, v2i, MOM_B_COL,
                                     r"v_2=-1\,\frac{m}{s}")

        self.play(FadeIn(cart2_a, shift=LEFT*0.3),
                  FadeIn(cart2_b, shift=RIGHT*0.3), run_time=0.55)
        self.play(FadeIn(arr2_a), FadeIn(arr2_b), run_time=0.5)

        bar2_p1 = momentum_bar(m1*v1i, p_tot2, MOM_A_COL, r"p_1", BAR1_Y + LEFT*0.5)
        bar2_p2 = momentum_bar(m2*v2i, p_tot2, MOM_B_COL, r"p_2", BAR2_Y + LEFT*0.5)
        sep2    = Line(LEFT*4, RIGHT*4, stroke_width=1,
                       color=LIGHT_PURPLE, stroke_opacity=0.4).move_to(BAR3_Y + UP*0.25)
        bar2_tot= momentum_bar(p_tot2, p_tot2, TOTAL_COL,
                               r"p_{\text{tot}}", BAR3_Y + LEFT*0.5)
        bef2_lbl= Text("BEFORE", font_size=24, weight=BOLD,
                        color=PINK_PURPLE).move_to(DOWN * 1.55)

        self.play(FadeIn(bef2_lbl), FadeIn(bar2_p1), FadeIn(bar2_p2),
                  FadeIn(sep2), FadeIn(bar2_tot), run_time=0.65)
        self.wait(0.6)

        # Both carts approach each other
        self.play(FadeOut(arr2_a, arr2_b), run_time=0.2)
        self.play(
            cart2_a.animate.move_to(TRACK_Y + RIGHT * 0.2),
            cart2_b.animate.move_to(TRACK_Y + RIGHT * 0.2 + RIGHT * 1.52),
            run_time=0.9, rate_func=linear,
        )

        # Stick together — merge flash
        merge_flash = Circle(radius=0.6, color=TOTAL_COL,
                             fill_color=TOTAL_COL, fill_opacity=0.55,
                             stroke_width=0).move_to(TRACK_Y + RIGHT * 0.95)
        self.play(FadeIn(merge_flash, scale=0.2), run_time=0.12)
        self.play(FadeOut(merge_flash, scale=2.8), run_time=0.28)

        # Merged cart (wider body)
        merged = VGroup(
            RoundedRectangle(width=3.1, height=1.0, corner_radius=0.15,
                fill_color=DEEP_PURPLE, fill_opacity=1,
                stroke_color=WHITE, stroke_width=2),
            MathTex(r"m_1{+}m_2=4\text{kg}", font_size=28, color=WHITE)\
                .set_stroke(width=1.1),
        )
        merged[1].move_to(merged[0])
        # wheels
        for dx in [-0.95, 0, 0.95]:
            w = Circle(radius=0.18, fill_color="#222", fill_opacity=1,
                       stroke_color=LIGHT_PURPLE, stroke_width=3)\
                .move_to(merged[0].get_bottom() + RIGHT*dx + DOWN*0.05)
            hub = Dot(w.get_center(), radius=0.06, color=LIGHT_PURPLE)
            merged.add(w, hub)
        merged.move_to(TRACK_Y + RIGHT * 0.75)

        self.play(FadeOut(cart2_a, cart2_b), FadeIn(merged), run_time=0.3)

        arr_merged = make_velocity_arrow(merged, vf, TOTAL_COL,
                                         rf"v'={vf:.2f}\,\frac{{m}}{{s}}")
        self.play(FadeIn(arr_merged), run_time=0.4)
        self.play(merged.animate.shift(RIGHT * 1.3),
                  arr_merged.animate.shift(RIGHT * 1.3),
                  run_time=1.0, rate_func=linear)

        aft2_lbl = Text("AFTER", font_size=24, weight=BOLD,
                         color=PINK_PURPLE).move_to(DOWN * 1.55)
        bar2_pf  = momentum_bar(p_tot2, p_tot2, TOTAL_COL,
                                r"p_{\text{tot}}'", BAR3_Y + LEFT*0.5)
        # individual bars collapse into total
        bar2_pA  = momentum_bar(p_tot2, p_tot2, DEEP_PURPLE,
                                r"p_A'", BAR1_Y + LEFT*0.5)
        bar2_pB  = momentum_bar(0.0, p_tot2, MOM_B_COL,
                                r"p_B'", BAR2_Y + LEFT*0.5)

        self.play(
            ReplacementTransform(bef2_lbl, aft2_lbl),
            ReplacementTransform(bar2_p1, bar2_pA),
            ReplacementTransform(bar2_p2, bar2_pB),
            ReplacementTransform(bar2_tot, bar2_pf),
            run_time=0.65,
        )

        conserved2 = Text("Still conserved! (KE is lost, p is not)",
                          font_size=25, weight=BOLD, color=TOTAL_COL)\
            .move_to(DOWN * 4.35)
        self.play(FadeIn(conserved2, shift=DOWN*0.1), run_time=0.4)
        self.wait(1.3)

        # Clear inelastic scene
        self.play(
            FadeOut(track2, merged, arr_merged, aft2_lbl,
                    bar2_pA, bar2_pB, sep2, bar2_pf, conserved2),
            run_time=0.6,
        )
        clear_sec()

        
        #  Derivation — where does the law come from?
      
        set_sec("Why is it conserved?", ACCENT_CYAN)

        steps = [
            (r"\vec{F}_{12} = -\vec{F}_{21}",
             "Newton's 3rd Law"),
            (r"\frac{d\vec{p}_1}{dt} = -\frac{d\vec{p}_2}{dt}",
             "Force = rate of change of momentum"),
            (r"\frac{d}{dt}(\vec{p}_1 + \vec{p}_2) = 0",
             "Sum of rates is zero"),
            (r"\therefore\; \vec{p}_{\text{total}} = \text{const}",
             "Total momentum is constant!"),
        ]

        step_grp = VGroup()
        for i, (tex, note) in enumerate(steps):
            eq  = MathTex(tex, font_size=42).set_stroke(width=1.6)\
                .set_color_by_gradient(*GRAD_MIX)
            nt  = Text(note, font_size=24, color=PINK_PURPLE)
            row = VGroup(eq, nt).arrange(DOWN, buff=0.14)
            bg  = RoundedRectangle(width=7.8, height=1.55, corner_radius=0.25,
                fill_color=DEEP_PURPLE, fill_opacity=0.42, stroke_width=3)\
                .set_color_by_gradient(*GRAD_MIX).move_to(row)
            step_grp.add(VGroup(bg, row))

        step_grp.arrange(DOWN, buff=0.28).move_to(UP * 1.5)

        for card in step_grp:
            self.play(FadeIn(card, shift=RIGHT * 0.2, scale=0.96), run_time=0.5)
            self.wait(0.35)

        self.wait(1.0)

        
        #  Summary card
       
        self.play(FadeOut(step_grp), run_time=0.6)
        clear_sec()

        sum_title = Text("Key Equations",
                         font_size=42, weight=BOLD, color=ACCENT_CYAN)\
            .move_to(UP * 5.0)
        self.play(FadeIn(sum_title, shift=DOWN * 0.2), run_time=0.5)

        main_eq = MathTex(
            r"m_1\vec{v}_1 + m_2\vec{v}_2 = m_1\vec{v}_1' + m_2\vec{v}_2'",
            font_size=40,
        ).set_stroke(width=1.8).move_to(UP * 3.3)
        main_eq.set_color_by_gradient(*GRAD_MIX)

        mfill = SurroundingRectangle(main_eq, corner_radius=0.25, buff=0.25,
            stroke_width=0, fill_color=DEEP_PURPLE, fill_opacity=0.42)
        mbox  = SurroundingRectangle(main_eq, corner_radius=0.25, buff=0.25,
            stroke_width=4).set_color_by_gradient(*GRAD_MIX)

        self.play(Write(main_eq), run_time=0.9)
        self.play(FadeIn(mfill), Create(mbox), run_time=0.4)

        def sum_card(tex, note, top_col, note_col, grad, pos):
            top = MathTex(tex, font_size=34, color=top_col).set_stroke(width=1.4)
            bot = Text(note, font_size=23, color=note_col)
            grp = VGroup(top, bot).arrange(DOWN, buff=0.15)
            bg  = RoundedRectangle(width=7.8, height=1.6, corner_radius=0.28,
                fill_color=DEEP_PURPLE, fill_opacity=0.45, stroke_width=3)\
                .set_color_by_gradient(*grad).move_to(grp)
            return VGroup(bg, grp).move_to(pos)

        c1 = sum_card(
            r"v_1' = \frac{m_1-m_2}{m_1+m_2}v_1",
            "Elastic  ·  kinetic energy conserved",
            CART_A_COL, PINK_PURPLE, GRAD_CYAN, UP * 1.35)

        c2 = sum_card(
            r"v' = \frac{m_1 v_1 + m_2 v_2}{m_1 + m_2}",
            "Inelastic  ·  KE lost, p conserved",
            CART_B_COL, PINK_PURPLE, GRAD_PURPLE, DOWN * 0.4)

        c3 = sum_card(
            r"\Delta \vec{p} = \vec{F}_{\text{net}}\,\Delta t = 0",
            "No external force → momentum conserved",
            TOTAL_COL, PINK_PURPLE, [TOTAL_COL, PRIMARY_PURPLE], DOWN * 2.15)

        for c in [c1, c2, c3]:
            self.play(FadeIn(c, shift=RIGHT * 0.18, scale=0.96), run_time=0.5)
            self.wait(0.2)

        self.wait(1.1)

     
        #  follow for more
       
        self.play(
            FadeOut(sum_title, main_eq, mfill, mbox, c1, c2, c3),
            run_time=0.65,
        )

        cta = VGroup(
            Text("Follow for more",          font_size=56, weight=BOLD, color=ACCENT_CYAN),
            Text("Physics & Math Explained", font_size=34, color=LIGHT_PURPLE),
        ).arrange(DOWN, buff=0.48).move_to(UP * 2.5)

        cta_glow = RoundedRectangle(
            width=8.4, height=3.5, corner_radius=0.5,
            fill_color=DEEP_PURPLE, fill_opacity=0.38, stroke_width=4,
        ).set_color_by_gradient(*GRAD_MIX).move_to(cta)

        arrow = Arrow(
            cta.get_bottom() + DOWN * 0.32,
            cta.get_bottom() + DOWN * 1.5,
            color=ACCENT_CYAN, stroke_width=13,
            max_tip_length_to_length_ratio=0.26,
        )

        self.play(
            FadeIn(cta_glow, scale=0.92),
            FadeIn(cta, shift=DOWN * 0.32, scale=1.04),
            GrowArrow(arrow),
            run_time=0.85,
        )
        self.play(
            cta.animate.scale(1.07),
            arrow.animate.shift(DOWN * 0.17),
            rate_func=there_and_back, run_time=0.85,
        )
        self.wait(2.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1)
        self.wait(0.4)