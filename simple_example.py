from manim import *


class SmileyFace(Scene):
    def construct(self):
        graphics = Group(Arc(start_angle=-140 * (PI / 180), angle=100 * (PI / 180)),
                         Dot().shift((UP + LEFT) * 0.5),
                         Dot().shift((UP + RIGHT) * 0.5))

        graphics_with_animation = ApplyWave(graphics)

        self.play(graphics_with_animation)
        self.wait()
