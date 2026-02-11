import os
import logging
from pathlib import Path
import platform
import tkinter as tk
from tkinterdnd2 import TkinterDnD
from .geometry import geometry
from . import config as conf

CURDIR = Path(__file__).parent

logger = logging.getLogger(__name__)

class BaseWindow:

    def __init__(self, title=conf.APP_NAME):
        self.root = TkinterDnD.Tk()
        base = float(self.root.tk.call("tk", "scaling"))
        if platform.system() == "Linux":
            self.root.tk.call("tk", "scaling", base * 1.5)

        self.root.withdraw()  
        self.root.title(title)
        self.set_geometry()
        self.root.resizable(False, False)

    def set_icon(self):
        assets_path = CURDIR / "assets"

        if platform.system() == "Windows":
            self.root.iconbitmap(assets_path / "jimlet.ico")
        else:
            icon = tk.PhotoImage(file=assets_path / "jimlet.png")
            self.root.iconphoto(True, icon)

    def set_geometry(self):
        screen_w = self.root.winfo_screenwidth()
        screen_h = self.root.winfo_screenheight()

        h = int(screen_h * geometry.height_ratio)
        w = int(h * geometry.aspect_ratio[0] / geometry.aspect_ratio[1])

        geometry.window_width = w
        geometry.window_height = h

        x = (screen_w - w) // 2
        y = (screen_h - h) // 2

        geometry.x = x
        geometry.y = y

        self.root.geometry(f"{w}x{h}+{x}+{y}")


    def show(self):

        self.root.deiconify()

        if platform.system() == "Darwin" and tk.TkVersion < 8.6:
            os.system(
                """/usr/bin/osascript -e '
                tell app "Finder"
                    to set frontmost of process "Python" to true
                end tell'
                """
            )

    def run(self, start_mainloop=False):

        self.show()

        if start_mainloop:
            self.root.mainloop()
