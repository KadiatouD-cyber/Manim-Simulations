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
BG_COLOR       = "#0a0a0a"

GRAD_PURPLE = [PRIMARY_PURPLE, LIGHT_PURPLE]
GRAD_CYAN   = [ACCENT_CYAN, "#00C8FF"]
GRAD_MIX    = [PRIMARY_PURPLE, ACCENT_CYAN, LIGHT_PURPLE]

W1_COL  = ACCENT_CYAN
W2_COL  = LIGHT_PURPLE
SUM_COL = "#FF79C6"
ENV_COL = "#FFD700"


class BeatsPhenomenon(Scene):
    def construct(self):
        self.camera.background_color = BG_COLOR

        # Branding
        brand = VGroup(
            Text("TechFlux",          font_size=38, weight=BOLD, color=PRIMARY_PURPLE),
            Text("Physics Explained", font_size=20, color=ACCENT_CYAN),
        ).arrange(DOWN, buff=0.08, aligned_edge=RIGHT).to_corner(DR, buff=0.4)
        self.add(brand)

        TITLE_Y = UP * 6.75
        SEC_Y   = UP * 5.38
        _sec    = [None]

        def set_sec(txt, col=ACCENT_CYAN):
            new = Text(txt, font_size=30, weight=BOLD, color=col).move_to(SEC_Y)
            anims = [FadeIn(new, shift=DOWN * 0.1)]
            if _sec[0]: anims.append(FadeOut(_sec[0], shift=UP * 0.1))
            self.play(*anims, run_time=0.38)
            _sec[0] = new

        def clear_sec():
            if _sec[0]:
                self.play(FadeOut(_sec[0], shift=UP * 0.1), run_time=0.28)
                _sec[0] = None

        #  HOOK
      
        hook = VGroup(
            MathTex(r"\mathbb{B}\text{eats}", font_size=72)
                .set_color_by_gradient(*GRAD_CYAN),
            MathTex(r"\mathbb{P}\text{henomenon}", font_size=56)
                .set_color_by_gradient(*GRAD_PURPLE),
        ).arrange(DOWN, buff=0.08).set_stroke(width=2.5).move_to(UP * 0.5)

        self.play(Write(hook), run_time=1.1)
        self.wait(0.25)

        sub = Text('The "wah-wah" effect in music',
                   font_size=27, color=PINK_PURPLE).set_stroke(width=1)
        sub.next_to(hook, DOWN, buff=0.32)
        self.play(FadeIn(sub, shift=DOWN * 0.2), run_time=0.5)
        self.wait(1.0)
        self.play(FadeOut(sub, shift=UP * 0.2), run_time=0.28)
        self.play(hook.animate.scale(0.62).move_to(TITLE_Y), run_time=0.6)

        #  LAYOUT
  
        ROW1_Y = UP  * 3.55
        ROW2_Y = UP  * 0.45
        ROW3_Y = DOWN * 2.60

        f1     = 5.0
        f2     = 5.8
        A      = 0.70
        x_show = 4.0
        x_range = [0.0, x_show]

        t_tr = ValueTracker(0.0)

        # Axes factory 
        def make_ax(center, y_range=(-1.15, 1.15), y_len=2.1):
            return Axes(
                x_range=[0, x_show, 1],
                y_range=[y_range[0], y_range[1], 0.5],
                x_length=7.5, y_length=y_len,
                axis_config={"stroke_width": 1.8, "color": LIGHT_PURPLE,
                             "stroke_opacity": 0.55, "include_tip": False,
                             "include_numbers": False},
            ).move_to(center)

        ax1 = make_ax(ROW1_Y)
        ax2 = make_ax(ROW2_Y)
        ax3 = make_ax(ROW3_Y, y_range=(-1.55, 1.55), y_len=2.75)

        # Row labels 
        lbl1 = MathTex(rf"y_1 = A\sin(2\pi \cdot {f1:.0f}\, t)",
                       font_size=30, color=W1_COL)\
            .set_stroke(width=1.3).next_to(ax1, UP, buff=0.08)
        lbl2 = MathTex(rf"y_2 = A\sin(2\pi \cdot {f2:.1f}\, t)",
                       font_size=30, color=W2_COL)\
            .set_stroke(width=1.3).next_to(ax2, UP, buff=0.08)
        lbl3 = MathTex(r"y_{\Sigma} = y_1 + y_2",
                       font_size=30, color=SUM_COL)\
            .set_stroke(width=1.3).next_to(ax3, UP, buff=0.08)

        sep1 = Line(LEFT*4.1, RIGHT*4.1, stroke_width=0.9,
                    color=PRIMARY_PURPLE, stroke_opacity=0.38).move_to(UP * 2.05)
        sep2 = Line(LEFT*4.1, RIGHT*4.1, stroke_width=0.9,
                    color=PRIMARY_PURPLE, stroke_opacity=0.38).move_to(DOWN * 1.05)

        # Static background curves
        def make_static(ax, fn, col, y_clip, stroke_op=0.22):
            xs = np.linspace(0, x_show, 1200)
            ys = np.clip(fn(xs), y_clip[0], y_clip[1])
            coords = [ax.c2p(x, y) for x, y in zip(xs, ys)]
            mob = VMobject(stroke_width=2.5, stroke_opacity=stroke_op)
            mob.set_points_smoothly(coords)
            mob.set_color(col)
            return mob

        bg1   = make_static(ax1, lambda xs: A*np.sin(2*PI*f1*xs),   W1_COL,  (-1.15,1.15))
        bg2   = make_static(ax2, lambda xs: A*np.sin(2*PI*f2*xs),   W2_COL,  (-1.15,1.15))
        bg_sum= make_static(ax3,
            lambda xs: A*np.sin(2*PI*f1*xs)+A*np.sin(2*PI*f2*xs),
            SUM_COL, (-1.55,1.55))

        # Live curves
        def live_wave(ax, freq, col, y_clip, grad=None, sw=5.0):
            def builder():
                t = t_tr.get_value()
                if t < 0.02: return VMobject()
                xs = np.linspace(0, min(t, x_show), max(3, int(t/x_show*900)))
                ys = np.clip(A*np.sin(2*PI*freq*xs), y_clip[0], y_clip[1])
                coords = [ax.c2p(x, y) for x, y in zip(xs, ys)]
                mob = VMobject(stroke_width=sw)
                mob.set_points_smoothly(coords)
                if grad: mob.set_color_by_gradient(*grad)
                else:    mob.set_color(col)
                return mob
            return always_redraw(builder)

        def live_sum(ax, fa, fb):
            def builder():
                t = t_tr.get_value()
                if t < 0.02: return VMobject()
                xs = np.linspace(0, min(t,x_show), max(3,int(t/x_show*900)))
                ys = np.clip(A*np.sin(2*PI*fa*xs)+A*np.sin(2*PI*fb*xs),-1.55,1.55)
                coords = [ax.c2p(x,y) for x,y in zip(xs,ys)]
                mob = VMobject(stroke_width=6.0)
                mob.set_points_smoothly(coords)
                mob.set_color_by_gradient(SUM_COL, "#FFD6F5", SUM_COL)
                return mob
            return always_redraw(builder)

        def live_env(ax, fa, fb, sign=1):
            def builder():
                t  = t_tr.get_value()
                if t < 0.02: return VMobject()
                df = abs(fb - fa)
                xs = np.linspace(0, min(t,x_show), max(3,int(t/x_show*600)))
                ys = np.clip(sign*2*A*np.abs(np.cos(PI*df*xs)), -1.55, 1.55)
                coords = [ax3.c2p(x,y) for x,y in zip(xs,ys)]
                mob = VMobject(stroke_width=3.5, stroke_opacity=0.9)
                mob.set_points_smoothly(coords)
                mob.set_color(ENV_COL)
                return mob
            return always_redraw(builder)

        def make_playhead(ax, freq, col, y_clip):
            return always_redraw(lambda:
                Dot(ax.c2p(
                    min(t_tr.get_value(), x_show),
                    float(np.clip(A*np.sin(2*PI*freq*min(t_tr.get_value(),x_show)),
                                  y_clip[0], y_clip[1]))),
                    color=col, radius=0.12).set_z_index(4))

        def make_playhead_sum(ax, fa, fb):
            return always_redraw(lambda:
                Dot(ax.c2p(
                    min(t_tr.get_value(), x_show),
                    float(np.clip(
                        A*np.sin(2*PI*fa*min(t_tr.get_value(),x_show))
                        + A*np.sin(2*PI*fb*min(t_tr.get_value(),x_show)),
                        -1.55, 1.55))),
                    color=SUM_COL, radius=0.13).set_z_index(4))

        g1      = live_wave(ax1, f1, W1_COL, (-1.15,1.15), grad=[W1_COL,"#9DF9EB",W1_COL])
        g2      = live_wave(ax2, f2, W2_COL, (-1.15,1.15), grad=[W2_COL,PINK_PURPLE,W2_COL])
        g_sum   = live_sum(ax3, f1, f2)
        env_top = live_env(ax3, f1, f2,  1)
        env_bot = live_env(ax3, f1, f2, -1)
        ph1     = make_playhead(ax1, f1, W1_COL, (-1.15,1.15))
        ph2     = make_playhead(ax2, f2, W2_COL, (-1.15,1.15))
        ph_s    = make_playhead_sum(ax3, f1, f2)

        # Reveal 
        set_sec("Two close frequencies…", ACCENT_CYAN)

        self.play(
            *[GrowFromCenter(a) for a in [ax1, ax2, ax3]],
            *[FadeIn(l, shift=DOWN*0.12) for l in [lbl1, lbl2, lbl3]],
            FadeIn(sep1), FadeIn(sep2),
            FadeIn(bg1), FadeIn(bg2), FadeIn(bg_sum),
            run_time=0.85,
        )
        self.add(g1, g2, g_sum, env_top, env_bot, ph1, ph2, ph_s)

        #  act 1 — draw waves live
   
        self.play(t_tr.animate.set_value(x_show), run_time=4.5, rate_func=linear)
        self.wait(0.3)

        set_sec("The envelope appears!", ENV_COL)

        env_lbl = MathTex(
            r"\text{envelope} = 2A\left|\cos(\pi \Delta f\, t)\right|",
            font_size=31, color=ENV_COL,
        ).set_stroke(width=1.4).next_to(ax3, DOWN, buff=0.12)
        self.play(FadeIn(env_lbl, shift=DOWN*0.1), run_time=0.5)
        self.play(env_top.animate.set_stroke(width=7),
                  env_bot.animate.set_stroke(width=7),
                  run_time=0.2, rate_func=there_and_back)
        self.wait(1.0)
        self.play(FadeOut(env_lbl), run_time=0.3)

     
        #  act 2 — slower Δf  (f2=5.3)
      
        set_sec("Closer frequencies → slower beats", LIGHT_PURPLE)
        f2b = 5.3

        self.remove(g1, g2, g_sum, env_top, env_bot, ph1, ph2, ph_s,
                    bg1, bg2, bg_sum)

        lbl2_new = MathTex(rf"y_2 = A\sin(2\pi \cdot {f2b:.1f}\, t)",
                           font_size=30, color=W2_COL)\
            .set_stroke(width=1.3).next_to(ax2, UP, buff=0.08)
        self.play(Transform(lbl2, lbl2_new), run_time=0.4)

        bg1b    = make_static(ax1, lambda xs: A*np.sin(2*PI*f1*xs),  W1_COL, (-1.15,1.15))
        bg2b    = make_static(ax2, lambda xs: A*np.sin(2*PI*f2b*xs), W2_COL, (-1.15,1.15))
        bg_sb   = make_static(ax3,
            lambda xs: A*np.sin(2*PI*f1*xs)+A*np.sin(2*PI*f2b*xs),
            SUM_COL, (-1.55,1.55))
        self.add(bg1b, bg2b, bg_sb)

        g1b      = live_wave(ax1, f1,  W1_COL, (-1.15,1.15), grad=[W1_COL,"#9DF9EB",W1_COL])
        g2b      = live_wave(ax2, f2b, W2_COL, (-1.15,1.15), grad=[W2_COL,PINK_PURPLE,W2_COL])
        g_sb     = live_sum(ax3, f1, f2b)
        env_tb   = live_env(ax3, f1, f2b,  1)
        env_bb   = live_env(ax3, f1, f2b, -1)
        ph1b     = make_playhead(ax1, f1,  W1_COL, (-1.15,1.15))
        ph2b     = make_playhead(ax2, f2b, W2_COL, (-1.15,1.15))
        ph_sb    = make_playhead_sum(ax3, f1, f2b)

        self.add(g1b, g2b, g_sb, env_tb, env_bb, ph1b, ph2b, ph_sb)
        t_tr.set_value(0)
        self.play(t_tr.animate.set_value(x_show), run_time=4.5, rate_func=linear)
        self.wait(0.3)
        self.remove(g1b, g2b, g_sb, env_tb, env_bb, ph1b, ph2b, ph_sb,
                    bg1b, bg2b, bg_sb)
        clear_sec()

      
        #  act 3 — DERIVATION
       
        self.play(FadeOut(ax1, ax2, ax3, lbl1, lbl2, lbl3, sep1, sep2), run_time=0.65)
        set_sec("Where does the formula come from?", ACCENT_CYAN)

        derive_steps = [
            (r"y_1+y_2 = A\sin(\omega_1 t)+A\sin(\omega_2 t)",
             "Start with superposition"),
            (r"= 2A\cos\!\left(\tfrac{\omega_1-\omega_2}{2}t\right)"
             r"\sin\!\left(\tfrac{\omega_1+\omega_2}{2}t\right)",
             "Sum-to-product identity"),
            (r"\underbrace{2A\cos(\pi\Delta f\,t)}_{\text{slow envelope}}"
             r"\cdot\underbrace{\sin(2\pi\bar{f}\,t)}_{\text{fast carrier}}",
             "Envelope  ×  Carrier"),
        ]

        cards = VGroup()
        for tex, note in derive_steps:
            eq  = MathTex(tex, font_size=33).set_stroke(width=1.4)\
                .set_color_by_gradient(*GRAD_MIX)
            nt  = Text(note, font_size=22, color=PINK_PURPLE)
            grp = VGroup(eq, nt).arrange(DOWN, buff=0.13)
            bg  = RoundedRectangle(width=7.8, height=1.65, corner_radius=0.25,
                fill_color=DEEP_PURPLE, fill_opacity=0.42, stroke_width=3)\
                .set_color_by_gradient(*GRAD_MIX).move_to(grp)
            cards.add(VGroup(bg, grp))

        cards.arrange(DOWN, buff=0.28).move_to(UP * 1.85)
        for card in cards:
            self.play(FadeIn(card, shift=RIGHT*0.2, scale=0.96), run_time=0.52)
            self.wait(0.38)
        self.wait(0.8)

        
        #  act 4 — beat frequency formula
   
        self.play(FadeOut(cards), run_time=0.5)
        clear_sec()
        set_sec("Beat Frequency Formula", ENV_COL)

        beat_eq = MathTex(r"f_{\text{beat}}", r"=", r"|f_1 - f_2|",
                          font_size=82).set_stroke(width=2.2).move_to(UP * 3.2)
        beat_eq[0].set_color(ENV_COL)
        beat_eq[2].set_color_by_gradient(W1_COL, W2_COL)

        bfill = SurroundingRectangle(beat_eq, corner_radius=0.3, buff=0.32,
            stroke_width=0, fill_color=DEEP_PURPLE, fill_opacity=0.45)
        bbox  = SurroundingRectangle(beat_eq, corner_radius=0.3, buff=0.32,
            stroke_width=5).set_color_by_gradient(*GRAD_MIX)

        self.play(Write(beat_eq), run_time=1.0)
        self.play(FadeIn(bfill), Create(bbox), run_time=0.45)
        self.wait(0.4)

        examples = [(5.0, 5.8, 0.8), (440, 444, 4), (220, 223, 3)]
        ex_cards = VGroup()
        for fa, fb, fb_beat in examples:
            if fa >= 100:
                tex  = rf"|{fa:.0f} - {fb:.0f}| = {fb_beat:.0f}\,\text{{Hz}}"
                note = f"A4 vs slightly sharp  →  {fb_beat:.0f} beats/sec"
            else:
                tex  = rf"|{fa:.1f} - {fb:.1f}| = {fb_beat:.1f}\,\text{{Hz}}"
                note = f"{fb_beat:.1f} amplitude pulsation per second"
            eq  = MathTex(tex, font_size=35, color=ENV_COL).set_stroke(width=1.3)
            nt  = Text(note, font_size=21, color=PINK_PURPLE)
            grp = VGroup(eq, nt).arrange(DOWN, buff=0.12)
            bg  = RoundedRectangle(width=7.8, height=1.4, corner_radius=0.24,
                fill_color=DEEP_PURPLE, fill_opacity=0.42, stroke_width=2.5)\
                .set_color_by_gradient(ENV_COL, PRIMARY_PURPLE).move_to(grp)
            ex_cards.add(VGroup(bg, grp))

        ex_cards.arrange(DOWN, buff=0.26).move_to(DOWN * 0.5)
        for ec in ex_cards:
            self.play(FadeIn(ec, shift=RIGHT*0.18, scale=0.95), run_time=0.45)
            self.wait(0.25)
        self.wait(1.0)
        
        #  act 5 — live Δf demo
        
        self.play(FadeOut(beat_eq, bfill, bbox, ex_cards), run_time=0.6)
        clear_sec()
        set_sec("Watch Δf change the beat rate", ACCENT_CYAN)

        ax_demo = Axes(
            x_range=[0, x_show, 1],
            y_range=[-1.55, 1.55, 0.5],
            x_length=7.5, y_length=3.5,
            axis_config={"stroke_width": 1.8, "color": LIGHT_PURPLE,
                         "stroke_opacity": 0.55, "include_tip": False,
                         "include_numbers": False},
        ).move_to(UP * 1.8)

        demo_lbl = MathTex(r"y_\Sigma", font_size=36, color=SUM_COL)\
            .set_stroke(width=1.3).next_to(ax_demo, UP, buff=0.1)
        self.play(GrowFromCenter(ax_demo), FadeIn(demo_lbl), run_time=0.55)

        df_tr = ValueTracker(0.8)

        beat_readout = always_redraw(lambda:
            MathTex(
                rf"f_{{\text{{beat}}}} = |f_1 - f_2| = {df_tr.get_value():.1f}\,\text{{Hz}}",
                font_size=34, color=ENV_COL,
            ).set_stroke(width=1.3).move_to(DOWN * 4.5))

        def demo_sum_curve():
            df  = df_tr.get_value()
            f2d = f1 + df
            xs  = np.linspace(0, x_show, 1200)
            ys  = np.clip(A*np.sin(2*PI*f1*xs)+A*np.sin(2*PI*f2d*xs), -1.55, 1.55)
            coords = [ax_demo.c2p(x, y) for x, y in zip(xs, ys)]
            mob = VMobject(stroke_width=5.5)
            mob.set_points_smoothly(coords)
            mob.set_color_by_gradient(SUM_COL, "#FFD6F5", SUM_COL)
            return mob

        def demo_env_curve(sign=1):
            def builder():
                df  = df_tr.get_value()
                xs  = np.linspace(0, x_show, 600)
                ys  = np.clip(sign*2*A*np.abs(np.cos(PI*df*xs)), -1.55, 1.55)
                coords = [ax_demo.c2p(x, y) for x, y in zip(xs, ys)]
                mob = VMobject(stroke_width=4.5, stroke_opacity=0.92)
                mob.set_points_smoothly(coords)
                mob.set_color(ENV_COL)
                return mob
            return always_redraw(builder)

        d_sum   = always_redraw(demo_sum_curve)
        d_env_t = demo_env_curve( 1)
        d_env_b = demo_env_curve(-1)

        self.add(d_sum, d_env_t, d_env_b, beat_readout)

        self.play(df_tr.animate.set_value(2.0), run_time=2.0, rate_func=smooth)
        self.wait(0.3)
        self.play(df_tr.animate.set_value(0.3), run_time=2.0, rate_func=smooth)
        self.wait(0.3)
        self.play(df_tr.animate.set_value(1.5), run_time=1.5, rate_func=smooth)
        self.wait(0.5)

        self.play(FadeOut(ax_demo, demo_lbl, d_sum, d_env_t, d_env_b,
                          beat_readout), run_time=0.6)
        clear_sec()

        #  SUMMARY

        sum_title = Text("Beats — Key Takeaways",
                         font_size=40, weight=BOLD, color=ACCENT_CYAN)\
            .move_to(UP * 5.05)
        self.play(FadeIn(sum_title, shift=DOWN*0.2), run_time=0.5)

        main_eq2 = MathTex(r"f_{\text{beat}} = |f_1 - f_2|",
                           font_size=68).set_stroke(width=2).move_to(UP * 3.3)
        main_eq2.set_color_by_gradient(ENV_COL, W1_COL, W2_COL)

        mfill2 = SurroundingRectangle(main_eq2, corner_radius=0.28, buff=0.28,
            stroke_width=0, fill_color=DEEP_PURPLE, fill_opacity=0.44)
        mbox2  = SurroundingRectangle(main_eq2, corner_radius=0.28, buff=0.28,
            stroke_width=5).set_color_by_gradient(*GRAD_MIX)

        self.play(Write(main_eq2), run_time=0.85)
        self.play(FadeIn(mfill2), Create(mbox2), run_time=0.4)
        self.wait(0.2)

        def key_card(tex, note, top_col, note_col, grad, pos):
            top = MathTex(tex, font_size=32, color=top_col).set_stroke(width=1.3)
            bot = Text(note, font_size=22, color=note_col)
            grp = VGroup(top, bot).arrange(DOWN, buff=0.13)
            bg  = RoundedRectangle(width=7.8, height=1.52, corner_radius=0.26,
                fill_color=DEEP_PURPLE, fill_opacity=0.45, stroke_width=3)\
                .set_color_by_gradient(*grad).move_to(grp)
            return VGroup(bg, grp).move_to(pos)

        kc1 = key_card(r"\Delta f \uparrow \;\Rightarrow\; \text{faster beats}",
                       "Larger gap = quicker pulsing",
                       ENV_COL, PINK_PURPLE, [ENV_COL, PRIMARY_PURPLE], UP * 1.45)

        kc2 = key_card(r"\Delta f \to 0 \;\Rightarrow\; \text{no beats}",
                       "Perfect unison — envelope vanishes",
                       W1_COL, PINK_PURPLE, GRAD_CYAN, DOWN * 0.22)

        kc3 = key_card(
            r"y_\Sigma = 2A\cos(\pi\Delta f\,t)\cdot\sin(2\pi\bar{f}\,t)",
            "Envelope × Carrier — sum-to-product",
            LIGHT_PURPLE, PINK_PURPLE, GRAD_PURPLE, DOWN * 1.88)

        for kc in [kc1, kc2, kc3]:
            self.play(FadeIn(kc, shift=RIGHT*0.18, scale=0.96), run_time=0.48)
            self.wait(0.22)
        self.wait(1.1)

        #  FOLLOW FOR MORE
  
        self.play(FadeOut(sum_title, main_eq2, mfill2, mbox2, kc1, kc2, kc3),
                  run_time=0.65)

        cta = VGroup(
            Text("Follow for more",          font_size=56, weight=BOLD, color=ACCENT_CYAN),
            Text("Physics Explained", font_size=34, color=LIGHT_PURPLE),
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

        self.play(FadeIn(cta_glow, scale=0.92),
                  FadeIn(cta, shift=DOWN*0.32, scale=1.04),
                  GrowArrow(arrow), run_time=0.85)
        self.play(cta.animate.scale(1.07), arrow.animate.shift(DOWN*0.17),
                  rate_func=there_and_back, run_time=0.85)
        self.wait(2.5)
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1)
        self.wait(0.4)