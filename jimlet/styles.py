import ttkbootstrap as tb
from .geometry import geometry
from . import config as conf

def apply_styles():
    style = tb.Style(theme=conf.APP_THEME)

    style.configure(
        "Primary.Action.TButton",
        width=10,
        padding=(0, geometry.whp(1)),
    )

    style.configure(
        "Outline.Secondary.Action.TButton",
        width=10,
        padding=(0, geometry.whp(1)),
    )

    style.configure(
        "Red.TFrame",
        background="red"
    )


