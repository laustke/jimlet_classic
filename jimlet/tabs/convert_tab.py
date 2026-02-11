import logging
import webbrowser
from urllib.parse import urlencode
from tkinter import ttk
import tkinter.font as tkfont
from tkinterdnd2 import DND_FILES
from ..geometry import geometry

logger = logging.getLogger(__name__)

class ConvertTab(ttk.Frame):

    def __init__(self, app):
        self.app = app
        self.c = self.app.c

        super().__init__(
            self.app.notebook,
            padding=(geometry.whp(4), geometry.whp(4))
        )

        self._columns_fitted = False

        self.create_widgets()
        self.setup_dnd()

    def setup_dnd(self):
        self.drop_target_register(DND_FILES)  # pylint: disable=no-member
        self.dnd_bind("<<Drop>>", self.c.on_files_dropped)  # pylint: disable=no-member

        self.tree.drop_target_register(DND_FILES)  # pylint: disable=no-member
        self.tree.dnd_bind("<<Drop>>", self.c.on_files_dropped)  # pylint: disable=no-member

    def create_widgets(self):
        self.content = ttk.Frame(self)
        self.content.grid(row=0, column=0, sticky="nsew")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        top_row = ttk.Frame(self.content)
        top_row.grid(row=0, column=0, sticky="w")

        btn_open = ttk.Button(
            top_row,
            text="Open some text files",
            command=self.c.open_text_files,
            padding=(geometry.whp(2), geometry.whp(1)),
        )
        btn_open.grid(row=0, column=0, sticky="w")

        lbl_hint = ttk.Label(
            top_row,
            text="or drag and drop them into this window to convert"
        )
        lbl_hint.grid(row=0, column=1, padx=(geometry.whp(1), 0), sticky="w")

        self.columns = (
            "status",
            "text_file",
            "text_size",
            "speech_file",
            "speech_size",
            "duration",
        )

        self.tree = ttk.Treeview(
            self.content,
            columns=self.columns,
            show="headings",
            height=8
        )

        self.tree.heading("status", text="✔")
        self.tree.heading("text_file", text="Text File")
        self.tree.heading("text_size", text="Size")
        self.tree.heading("speech_file", text="Speech File")
        self.tree.heading("speech_size", text="Size")
        self.tree.heading("duration", text="Duration")

        self.tree.column("status", width=36, anchor="center", stretch=False)

        for col in self.columns:
            self.tree.column(col, anchor="center", stretch=True)

        self.tree.column("text_file", anchor="w")
        self.tree.column("speech_file", anchor="w")

        self.tree.grid(
            row=1,
            column=0,
            sticky="nsew",
            pady=(geometry.whp(4), 0)
        )

        bottom_row = ttk.Frame(self.content, style="BottomContainer.TFrame")
        bottom_row.grid(
            row=2,
            column=0,
            sticky="ew",
            pady=(geometry.whp(4), 0)
        )

        bottom_row.grid_columnconfigure(2, weight=1)

        BTN_WIDTH = 10

        btn_convert = ttk.Button(
            bottom_row,
            text="Convert",
            style="Action.TButton",
            width=BTN_WIDTH,
            padding=(0, geometry.whp(1)),
            command=self.c.start_conversion,
        )
        btn_convert.grid(row=0, column=0, padx=(0, geometry.whp(3)), sticky="w")

        btn_clear = ttk.Button(
            bottom_row,
            text="Clear",
            width=BTN_WIDTH,
            padding=(0, geometry.whp(1)),
            bootstyle="outline",
            command=self.c.new_batch,
        )
        btn_clear.grid(row=0, column=1, sticky="w")

        self.show_personal_use(bottom_row)

        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(1, weight=1)

        self.tree.bind("<Configure>", self._on_tree_configure)

    def show_personal_use(self, master):

        info = ttk.Frame(master)
        info.grid(row=0, column=3, sticky="ne")

        info.grid_rowconfigure(0, weight=0)
        info.grid_rowconfigure(1, weight=0)

        ttk.Label(
            info,
            text="Free non-commercial version"
        ).grid(row=0, column=0, columnspan=2, sticky="w")

        line = ttk.Frame(info)
        line.grid(row=1, column=0, sticky="e")

        ttk.Label(
            line,
            text="Upgrade to ",
        ).grid(row=0, column=0, sticky="w")

        base_font = tkfont.nametofont("TkDefaultFont")
        base_font_size=base_font.cget("size")

        link_font = base_font.copy()
        link_font.configure(
            underline=True,
            size = base_font_size
        )



        link = ttk.Label(
            line,
            text="Jimlet Pro",
            font=link_font,
            foreground="#0b5ed7",
            cursor="hand2"
        )
        link.grid(row=0, column=1, sticky="w")

        ttk.Label(
            line,
            text=" now!",
        ).grid(row=0, column=2, sticky="w")

        def open_site(_):

            base_url = "https://jimlet.com/pro/"
            params = {
                "utm_source": "jimlet",
                "utm_medium": "app",
                "utm_campaign": "standard",
                "utm_content": "convert_tab_link",
            }

            url = f"{base_url}?{urlencode(params)}"
            webbrowser.open(url)

        link.bind("<Button-1>", open_site)

    def _on_tree_configure(self, event):
        if self._columns_fitted:
            return

        total_width = event.width
        if total_width <= 1:
            return

        proportions = {
            "status":      0.04,
            "text_file":   0.30,
            "text_size":   0.10,
            "speech_file": 0.30,
            "speech_size": 0.10,
            "duration":    0.15,
        }

        for col, frac in proportions.items():
            self.tree.column(col, width=int(total_width * frac))

        self._columns_fitted = True

    def select_row(self, item_id):
        self.tree.selection_set(item_id)
        self.tree.focus(item_id)
        self.tree.see(item_id)

    def update_row(
        self,
        item_id,
        *,
        speech_file=None,
        speech_size=None,
        duration=None,
    ):
        values = list(self.tree.item(item_id, "values"))

        if speech_file is not None:
            values[3] = speech_file

        if speech_size is not None:
            values[4] = speech_size

        if duration is not None:
            values[5] = duration

        self.tree.item(item_id, values=values)
