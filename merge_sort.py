from manim import *
import numpy as np

config.pixel_height = 1920
config.pixel_width = 1080
config.frame_rate = 60
config.frame_height = 16.0
config.frame_width = 9.0

class MergeSort(Scene):
    def construct(self):
        # TechFlux Color Scheme
        primary_purple = "#9D4EDD"
        light_purple = "#C77DFF"
        pink_purple = "#E0AAFF"
        deep_purple = "#7B2CBF"
        accent_cyan = "#00D9FF"

        self.camera.background_color = "#0a0a0a"

        # TechFlux Branding
        techflux = Text("TechFlux", font_size=44, weight=BOLD, color=primary_purple)
        techflux.to_corner(DR, buff=0.5)
        self.add(techflux)

        # Title
        title = Text("Merge Sort", font_size=56, weight=BOLD, color=light_purple)
        title.to_edge(UP, buff=1.2)
        self.add(title)

        # Subtitle
        subtitle = Text("Divide, Conquer, and Merge", font_size=32, color=pink_purple)
        subtitle.next_to(title, DOWN, buff=0.3)
        self.play(FadeIn(subtitle))
        self.wait(1.5)
        self.play(FadeOut(subtitle))

        # Complexity
        complexity = VGroup(
            MathTex(r"\text{Time: } O(n \log n)", font_size=36, color=pink_purple),
            MathTex(r"\text{Space: } O(n)", font_size=36, color=accent_cyan)
        ).arrange(DOWN, buff=0.3)
        complexity.to_edge(DOWN, buff=1.5)
        self.play(FadeIn(complexity))

        # Array to sort
        array = [38, 27, 43, 3, 9, 82, 10]
        n = len(array)

        box_size = 0.75
        spacing = 0.18
        total_width = n * (box_size + spacing) - spacing

        def create_boxes(arr, y_pos, color=deep_purple):
            boxes = VGroup()
            labels = VGroup()
            tw = len(arr) * (box_size + spacing) - spacing
            sx = -tw / 2
            for i, val in enumerate(arr):
                box = Square(
                    side_length=box_size,
                    fill_color=BLACK,
                    fill_opacity=1,
                    stroke_color=color,
                    stroke_width=4
                )
                x = sx + i * (box_size + spacing) + box_size / 2
                box.move_to([x, y_pos, 0])
                boxes.add(box)
                label = Text(str(val), font_size=32, color=WHITE, weight=BOLD)
                label.move_to(box.get_center())
                labels.add(label)
            return boxes, labels

        # --- STEP 1: Show original array ---
        step_label = Text("Original Array", font_size=36, color=accent_cyan, weight=BOLD)
        step_label.shift(UP * 5.5)
        self.play(FadeIn(step_label))

        boxes, labels = create_boxes(array, 4.5)
        self.play(
            LaggedStart(*[FadeIn(b) for b in boxes], lag_ratio=0.08),
            LaggedStart(*[FadeIn(l) for l in labels], lag_ratio=0.08),
            run_time=1.5
        )
        self.wait(1.5)

        # --- STEP 2: DIVIDE phase ---
        self.play(FadeOut(step_label))
        divide_label = Text("Step 1: Divide", font_size=36, color=accent_cyan, weight=BOLD)
        divide_label.shift(UP * 5.5)
        self.play(FadeIn(divide_label))
        self.wait(0.5)

        # Level 1 split: [38,27,43,3] and [9,82,10]
        left1 = [38, 27, 43, 3]
        right1 = [9, 82, 10]

        y1 = 2.8
        # Left group
        l1_boxes, l1_labels = create_boxes(left1, y1)
        for b in l1_boxes:
            b.shift(LEFT * 1.8)
        for l in l1_labels:
            l.shift(LEFT * 1.8)

        # Right group
        r1_boxes, r1_labels = create_boxes(right1, y1)
        for b in r1_boxes:
            b.shift(RIGHT * 2.2)
        for l in r1_labels:
            l.shift(RIGHT * 2.2)

        # Draw split arrows
        mid = boxes[3].get_center()
        arrow_l1 = Arrow(boxes[1].get_bottom(), l1_boxes[1].get_top(), color=light_purple, stroke_width=3, buff=0.15)
        arrow_r1 = Arrow(boxes[5].get_bottom(), r1_boxes[1].get_top(), color=light_purple, stroke_width=3, buff=0.15)

        self.play(
            GrowArrow(arrow_l1), GrowArrow(arrow_r1),
            LaggedStart(*[FadeIn(b) for b in l1_boxes], lag_ratio=0.06),
            LaggedStart(*[FadeIn(l) for l in l1_labels], lag_ratio=0.06),
            LaggedStart(*[FadeIn(b) for b in r1_boxes], lag_ratio=0.06),
            LaggedStart(*[FadeIn(l) for l in r1_labels], lag_ratio=0.06),
            run_time=1.5
        )
        self.wait(1)

        # Level 2 split
        y2 = 1.0
        # [38,27] [43,3] [9,82] [10]
        splits = [[38, 27], [43, 3], [9, 82], [10]]
        offsets = [LEFT * 3.2, LEFT * 0.9, RIGHT * 1.4, RIGHT * 3.5]

        all_l2_boxes = []
        all_l2_labels = []
        arrows_l2 = []

        for idx, (s, off) in enumerate(zip(splits, offsets)):
            sb, sl = create_boxes(s, y2)
            for b in sb:
                b.shift(off)
            for l in sl:
                l.shift(off)
            all_l2_boxes.append(sb)
            all_l2_labels.append(sl)

            # Arrow from parent
            if idx < 2:
                parent_box = l1_boxes[idx * 2 if idx == 0 else 2]
                a = Arrow(parent_box.get_bottom(), sb[0].get_top(), color=light_purple, stroke_width=2.5, buff=0.15)
            else:
                parent_box = r1_boxes[(idx - 2) * 2 if idx == 2 else 2]
                a = Arrow(parent_box.get_bottom(), sb[0].get_top(), color=light_purple, stroke_width=2.5, buff=0.15)
            arrows_l2.append(a)

        anims = []
        for a in arrows_l2:
            anims.append(GrowArrow(a))
        for sb in all_l2_boxes:
            anims.append(LaggedStart(*[FadeIn(b) for b in sb], lag_ratio=0.06))
        for sl in all_l2_labels:
            anims.append(LaggedStart(*[FadeIn(l) for l in sl], lag_ratio=0.06))

        self.play(*anims, run_time=1.5)
        self.wait(1)

        # Level 3 split: each pair into singles
        y3 = -0.8
        singles = [[38], [27], [43], [3], [9], [82], [10]]
        single_offsets = [LEFT * 3.8, LEFT * 2.5, LEFT * 1.2, RIGHT * 0.1, RIGHT * 1.2, RIGHT * 2.5, RIGHT * 3.5]

        all_l3_boxes = []
        all_l3_labels = []
        arrows_l3 = []

        for idx, (s, off) in enumerate(zip(singles, single_offsets)):
            sb, sl = create_boxes(s, y3)
            for b in sb:
                b.shift(off)
            for l in sl:
                l.shift(off)
            all_l3_boxes.append(sb)
            all_l3_labels.append(sl)

            parent_idx = idx // 2
            if parent_idx < len(all_l2_boxes):
                child_in_parent = idx % 2
                if child_in_parent < len(all_l2_boxes[parent_idx]):
                    parent_box = all_l2_boxes[parent_idx][child_in_parent]
                    a = Arrow(parent_box.get_bottom(), sb[0].get_top(), color=light_purple, stroke_width=2, buff=0.15)
                    arrows_l3.append(a)

        anims = []
        for a in arrows_l3:
            anims.append(GrowArrow(a))
        for sb in all_l3_boxes:
            anims.append(LaggedStart(*[FadeIn(b) for b in sb], lag_ratio=0.06))
        for sl in all_l3_labels:
            anims.append(LaggedStart(*[FadeIn(l) for l in sl], lag_ratio=0.06))

        self.play(*anims, run_time=1.5)
        self.wait(1)

        # Single element label
        single_label = Text("Single elements are already sorted!", font_size=28, color=accent_cyan)
        single_label.shift(DOWN * 2.2)
        self.play(FadeIn(single_label))
        self.wait(1.5)

        # --- STEP 3: Clear and show MERGE phase ---
        all_mobs = [boxes, labels, l1_boxes, l1_labels, r1_boxes, r1_labels,
                    arrow_l1, arrow_r1, single_label, divide_label]
        for sb in all_l2_boxes:
            all_mobs.append(sb)
        for sl in all_l2_labels:
            all_mobs.append(sl)
        for sb in all_l3_boxes:
            all_mobs.append(sb)
        for sl in all_l3_labels:
            all_mobs.append(sl)
        for a in arrows_l2:
            all_mobs.append(a)
        for a in arrows_l3:
            all_mobs.append(a)

        self.play(*[FadeOut(m) for m in all_mobs], run_time=1)
        self.wait(0.5)

        # --- MERGE PHASE ---
        merge_label = Text("Step 2: Merge & Sort", font_size=36, color=accent_cyan, weight=BOLD)
        merge_label.shift(UP * 5.5)
        self.play(FadeIn(merge_label))
        self.wait(0.5)

        # Show singles again at top
        y_start = 4.5
        singles_flat = [38, 27, 43, 3, 9, 82, 10]
        s_boxes, s_labels = create_boxes(singles_flat, y_start)
        self.play(
            LaggedStart(*[FadeIn(b) for b in s_boxes], lag_ratio=0.08),
            LaggedStart(*[FadeIn(l) for l in s_labels], lag_ratio=0.08),
            run_time=1
        )
        self.wait(1)

        # Merge level 1: pairs merge into sorted pairs
        y_m1 = 2.8
        merged1 = [[27, 38], [3, 43], [9, 82], [10]]
        m1_offsets = [LEFT * 3.2, LEFT * 0.9, RIGHT * 1.4, RIGHT * 3.5]

        all_m1_boxes = []
        all_m1_labels = []

        for s, off in zip(merged1, m1_offsets):
            mb, ml = create_boxes(s, y_m1, color=accent_cyan)
            for b in mb:
                b.shift(off)
            for l in ml:
                l.shift(off)
            all_m1_boxes.append(mb)
            all_m1_labels.append(ml)

        # Arrows
        m1_arrows = []
        pair_starts = [0, 2, 4, 6]
        for idx, ps in enumerate(pair_starts):
            if ps + 1 < len(s_boxes):
                a = Arrow(s_boxes[ps].get_bottom(), all_m1_boxes[idx][0].get_top(), color=pink_purple, stroke_width=2.5, buff=0.15)
                m1_arrows.append(a)
                if ps + 1 < len(s_boxes) and len(all_m1_boxes[idx]) > 1:
                    a2 = Arrow(s_boxes[ps + 1].get_bottom(), all_m1_boxes[idx][1].get_top(), color=pink_purple, stroke_width=2.5, buff=0.15)
                    m1_arrows.append(a2)
            else:
                a = Arrow(s_boxes[ps].get_bottom(), all_m1_boxes[idx][0].get_top(), color=pink_purple, stroke_width=2.5, buff=0.15)
                m1_arrows.append(a)

        anims = [GrowArrow(a) for a in m1_arrows]
        for mb in all_m1_boxes:
            anims.append(LaggedStart(*[FadeIn(b) for b in mb], lag_ratio=0.06))
        for ml in all_m1_labels:
            anims.append(LaggedStart(*[FadeIn(l) for l in ml], lag_ratio=0.06))

        self.play(*anims, run_time=1.5)
        self.wait(1)

        # Merge level 2: [27,38] + [3,43] → [3,27,38,43] and [9,82] + [10] → [9,10,82]
        y_m2 = 1.0
        merged2 = [[3, 27, 38, 43], [9, 10, 82]]
        m2_offsets = [LEFT * 1.5, RIGHT * 2.8]

        all_m2_boxes = []
        all_m2_labels = []

        for s, off in zip(merged2, m2_offsets):
            mb, ml = create_boxes(s, y_m2, color=light_purple)
            for b in mb:
                b.shift(off)
            for l in ml:
                l.shift(off)
            all_m2_boxes.append(mb)
            all_m2_labels.append(ml)

        m2_arrows = []
        a1 = Arrow(all_m1_boxes[0][0].get_bottom(), all_m2_boxes[0][0].get_top(), color=pink_purple, stroke_width=2.5, buff=0.15)
        a2 = Arrow(all_m1_boxes[1][0].get_bottom(), all_m2_boxes[0][2].get_top(), color=pink_purple, stroke_width=2.5, buff=0.15)
        a3 = Arrow(all_m1_boxes[2][0].get_bottom(), all_m2_boxes[1][0].get_top(), color=pink_purple, stroke_width=2.5, buff=0.15)
        a4 = Arrow(all_m1_boxes[3][0].get_bottom(), all_m2_boxes[1][1].get_top(), color=pink_purple, stroke_width=2.5, buff=0.15)
        m2_arrows = [a1, a2, a3, a4]

        anims = [GrowArrow(a) for a in m2_arrows]
        for mb in all_m2_boxes:
            anims.append(LaggedStart(*[FadeIn(b) for b in mb], lag_ratio=0.06))
        for ml in all_m2_labels:
            anims.append(LaggedStart(*[FadeIn(l) for l in ml], lag_ratio=0.06))

        self.play(*anims, run_time=1.5)
        self.wait(1)

        # Final merge: [3,27,38,43] + [9,10,82] → [3,9,10,27,38,43,82]
        y_final = -1.2
        final_sorted = [3, 9, 10, 27, 38, 43, 82]
        f_boxes, f_labels = create_boxes(final_sorted, y_final, color=accent_cyan)

        f_arrows = []
        a1 = Arrow(all_m2_boxes[0][0].get_bottom(), f_boxes[0].get_top(), color=pink_purple, stroke_width=2.5, buff=0.15)
        a2 = Arrow(all_m2_boxes[1][0].get_bottom(), f_boxes[3].get_top(), color=pink_purple, stroke_width=2.5, buff=0.15)
        f_arrows = [a1, a2]

        anims = [GrowArrow(a) for a in f_arrows]
        anims.append(LaggedStart(*[FadeIn(b) for b in f_boxes], lag_ratio=0.08))
        anims.append(LaggedStart(*[FadeIn(l) for l in f_labels], lag_ratio=0.08))

        self.play(*anims, run_time=1.5)
        self.wait(1)

        # Celebration
        self.play(
            *[b.animate.set_stroke(color=accent_cyan, width=5).set_fill(color=accent_cyan, opacity=0.2).scale(1.1) for b in f_boxes],
            run_time=0.6
        )
        self.play(
            *[b.animate.set_fill(color=BLACK, opacity=1).scale(1/1.1) for b in f_boxes],
            run_time=0.4
        )

        sorted_text = Text("Sorted!", font_size=48, color=accent_cyan, weight=BOLD)
        sorted_text.shift(DOWN * 2.5)
        self.play(FadeIn(sorted_text, shift=UP))
        self.wait(3)

        # Fade out
        self.play(*[FadeOut(m) for m in self.mobjects], run_time=1.5)
        self.wait(0.5)