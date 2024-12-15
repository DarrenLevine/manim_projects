from extended_manim import *


class PerceptronAnimation(Scene):
    def construct(self):

        max_min = 4
        max_axis = 5
        small_offset = max_axis * 0.1
        start_x_val = -max_min * 0.8
        t = ValueTracker(start_x_val)

        with self.context_section("equation introduction", skip_animations=False):

            ct = {"h": YELLOW, "tanh": YELLOW}
            c = {"x": BLUE, "tan": YELLOW, "WORLD": PURPLE, "w": GREEN}
            c.update(ct)
            eqs = dict(colors=c, vectors=('w', 'x'))

            self.play(Write(Text('Perceptron:').scale(0.9).to_edge(UL)).set_run_time(1.))

            f_of_x_equals = MathTexColored("f(x) = ", **eqs).scale(1.5).shift(LEFT * 1.3)
            eq_with_h = MathTexColored("h(x*w)", **eqs).scale(1.5).shift(RIGHT * 1.3)
            self.play(AnimationGroup(
                Write(f_of_x_equals, rate_func=linear),
                Write(eq_with_h, rate_func=linear), lag_ratio=0.8))
            self.wait()

            self.play(
                AnimationGroup(
                    FadeOut(f_of_x_equals,
                            target_position=eq_with_h.copy().to_corner(UL).shift(DOWN + RIGHT * 0.4).get_center()),
                    eq_with_h.animate.to_corner(UL).shift(DOWN + RIGHT * 0.4)
                )
            )

            eq_x_part, eq_dot_part, eq_w_part = eq_with_h[2], eq_with_h[3], eq_with_h[4]

        with self.context_section("equation breakdown: matrix multiply and sum", skip_animations=False):
            x = Matrix([["x_{0}"], ["x_{1}"], ["..."], ["x_{N}"]]).set_color(BLACK).set_column_colors(c['x'])
            x.to_edge(LEFT).shift(DOWN * 0.2)

            m = Matrix([[r"\times"], [r"\times"], ["{{}}"], [r"\times"]]).set_color(BLACK).set_column_colors(WHITE)
            m.to_edge(LEFT).shift(DOWN * 0.2 + RIGHT + np.array([0.25, 0, 0]))

            w = Matrix([["w_{0}"], ["w_{1}"], ["..."], ["w_{N}"]]).set_color(BLACK).set_column_colors(c['w'])
            w.to_edge(LEFT).shift(DOWN * 0.2 + RIGHT * 2)

            sum_text = Text('+')
            root = np.array([0, -max_axis / 2, 0])
            a = (root[0] - small_offset * 1.5, root[1] + max_axis * 0.5, 0)
            sum_text.move_to(np.array(a) - np.array([0.5, 0., 0.]))

            sum_lines = []
            for i in [1.2, 0.4, -1.2]:
                s = w.get_right() + UP * i
                sum_lines += [
                    CubicBezier(s, s + 1 * RIGHT,
                                sum_text.get_left() - 1 * RIGHT, sum_text.get_left() - RIGHT * 0.4)]

            arrow_head = Triangle(fill_color=WHITE, fill_opacity=1, color=WHITE
                                  ).rotate(-PI * 0.5).move_to(sum_lines[0].get_end()).scale(0.15)

            ax = Axes(
                x_range=[-max_min, max_min],
                y_range=[-max_min / 2, max_min / 2],
                x_length=max_axis,
                y_length=max_axis,
                axis_config={"include_tip": False}
            )
            ax.move_to(root + max_axis * np.array([0.5, 0.5, 0]))

            self.play(AnimationGroup(
                GrowFromPoint(x, eq_x_part).set_run_time(0.8),
                GrowFromPoint(m, eq_dot_part).set_run_time(0.8),
                GrowFromPoint(w, eq_w_part).set_run_time(0.8),
                Create(sum_lines[0]),
                Create(sum_lines[1]),
                FadeIn(arrow_head),
                Create(sum_lines[2]),
                GrowFromCenter(sum_text),
                GrowFromPoint(ax, sum_text),
                lag_ratio=0.3
            ).set_run_time(3.2))

        with self.context_section("equation breakdown: plotted transfer function", skip_animations=False):
            ax = Axes(
                x_range=[-max_min, max_min],
                y_range=[-max_min / 2, max_min / 2],
                x_length=max_axis,
                y_length=max_axis,
                axis_config={"include_tip": True})
            ax.move_to(root + max_axis * np.array([0.5, 0.5, 0]))

            heaviside = lambda x: x > 0.
            h_graph = ax.plot(
                heaviside,
                color=YELLOW_D,
                x_range=[-max_min, max_min, 0.01],
                use_smoothing=False
            )
            self.play(GrowFromPoint(h_graph, eq_with_h.get_center()).set_run_time(1.3))

        with self.context_section("equation breakdown: switch from heaviside to tanh", skip_animations=False):

            approx = MathTexColored('\\text{Heaviside/Step Function } h \\approx tanh', colors=ct
                                    ).to_edge(UP).shift(RIGHT * 2)

            tanh_func = np.tanh
            graph = ax.plot(
                tanh_func,
                color=YELLOW_D,
                x_range=[-max_min, max_min],
                use_smoothing=False,
            )
            eq_with_tanh = MathTexColored("tan", "h(x*w)", **eqs).scale(1.5).move_to(eq_with_h)
            self.play(Write(approx).set_run_time(0.9))
            self.play(
                AnimationGroup(
                    AnimationGroup(
                        Transform(h_graph, graph),
                        TransformMatchingTex(eq_with_h, eq_with_tanh)),
                    lag_ratio=0.6,
                    run_time=3.))
            self.wait()
            self.play(FadeOut(approx))

            plotted_point = Dot()
            plotted_point.add_updater(lambda x: x.move_to(ax.c2p(t.get_value(), tanh_func(t.get_value()))))
            self.add(plotted_point)

            def get_blue_dotted_line():
                small_offset = max_axis * 0.1
                xy = ax.c2p(t.get_value(), tanh_func(t.get_value()), 1)
                b = (root[0] - small_offset, root[1] + max_axis * 0.5, xy[2])
                c = (root[0] - small_offset, root[1] - small_offset, xy[2])
                d = (xy[0], root[1] - small_offset, xy[2])
                e = xy
                f = (root[0] + max_axis + small_offset * 1, xy[1], xy[2])
                lines = []
                lines += [DashedLine(a, b, color=BLUE_D)]
                lines += [DashedLine(b, c, color=BLUE_D)]
                lines += [DashedLine(c, d, color=BLUE_D)]
                x_line = DashedLine(d, e, color=BLUE_D)
                y_line = DashedLine(e, f, color=BLUE_D).add_tip(tip_width=0.25, tip_length=0.25)
                x_value_label = Text(f'{xy[0]:.3}').scale(0.5).move_to((xy[0], root[1] - small_offset * 2, xy[2]))
                y_value_label = Text(f'{xy[1]:.3}').scale(0.5).move_to((root[0] + max_axis + small_offset * 2, xy[1], xy[2]))
                lines += [x_value_label, x_line, y_line, y_value_label]
                return VGroup(*lines)

            self.play(Create(always_redraw(get_blue_dotted_line)))

            self.play(t.animate(run_time=1.2).set_value(max_min * 0.9))
            self.play(t.animate(run_time=1.2).set_value(-max_min * 0.9))
            self.play(t.animate(run_time=1.2).set_value(max_min * 0.9))
            self.play(t.animate(run_time=1.2).set_value(start_x_val))

        self.wait()
