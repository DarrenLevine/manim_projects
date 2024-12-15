from manim import *
import re
from contextlib import contextmanager
from typing import Generator


@contextmanager
def context_section(
    self,
    name: str = "unnamed",
    type: str = DefaultSectionType.NORMAL,
    skip_animations: bool = False,
) -> Generator[None, None, None]:
    print(f"Entering section: {name}")
    self.next_section(name, type, skip_animations)
    yield
    print(f"Exiting section: {name}")


Scene.context_section = context_section


def MathTexColored(*args, **kargs):
    """same as MathTex, but with an optional colors dictionary argument"""
    color_map_i = kargs.pop('colors', {})
    vectors = kargs.pop('vectors', [])
    for txt in color_map_i:
        args = [re.sub(rf'(\b)({txt})(\b)', rf'\1{{\2}}\3', f' {k} ')[1:-1]
                for k in args]
    for txt in vectors:
        args = [re.sub(rf'(\b)({txt})(\b)', rf'\1\\vec{{\2}}\3', f' {k} ')[1:-1] for k in args]
    full_text = r'{{}}'.join(args)
    args = [x for x in re.split(r'(\s|\(|\)|\.\*|\*|\=)', full_text) if x]
    args = [k.replace(
        r'->', r'\rightarrow').replace(
        r'.*', r' ').replace(
        r'*', r'\cdot') for k in args]
    color_map = {
        rf'{{\vec{{{c}}}}}' if c in vectors else rf'{{{c}}}': v
        for c, v in color_map_i.items()}
    obj = MathTex(*args, **kargs, substrings_to_isolate=list(color_map.keys()))
    for s, c in color_map.items():
        for i, seg in enumerate(obj):
            if seg.tex_string == s:
                obj[i].set_color(c)
    return obj
