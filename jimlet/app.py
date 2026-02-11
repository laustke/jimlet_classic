import logging
from tkinter import ttk, font
from .base_window import BaseWindow
from .styles import apply_styles
from .tabs import ConvertTab, SettingsTab, AboutTab
from .controller import Controller
from . import config as conf

logger = logging.getLogger(__name__)


class JimletApp(BaseWindow):

    def __init__(self, title="Jimlet TTS Converter"):
        super().__init__(title)
        self.c = Controller(self)
        self.set_font_size()
        self.set_icon()
        apply_styles()
        self.create_widgets()

        settings = self.c.load_settings()

        self.c._suspend_autosave = True
        self.settings_tab.apply_settings(settings)
        self.c._suspend_autosave = False

    def set_font_size(self):
        fs = conf.FONT_SIZE
        font.nametofont("TkDefaultFont").configure(size=fs)
        font.nametofont("TkTextFont").configure(size=fs)
        font.nametofont("TkFixedFont").configure(size=fs)
        font.nametofont("TkMenuFont").configure(size=fs)
        font.nametofont("TkHeadingFont").configure(size=fs)

    def create_widgets(self):

        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        self.notebook = ttk.Notebook(self.root)
        print("Notebook: ", self.notebook.cget("style"))
        self.notebook.grid(row=0, column=0, sticky="nsew")

        self.convert_tab = ConvertTab(self)
        self.settings_tab = SettingsTab(self)
        self.about_tab = AboutTab(self)

        self.notebook.add(self.convert_tab, text="Convert")
        self.notebook.add(self.settings_tab, text="Settings")
        self.notebook.add(self.about_tab, text="About")
