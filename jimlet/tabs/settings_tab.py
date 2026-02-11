from tkinter import ttk
from ..geometry import geometry

class SettingsTab(ttk.Frame):
    def __init__(self, app):
        self.app = app
        self.c = self.app.c
        super().__init__(
            self.app.notebook,
            padding=(geometry.whp(4), geometry.whp(4))
        )
        self.create_widgets()

    def apply_settings(self, settings: dict | None = None) -> None:
        self.c.apply_settings(settings)

        self.quality_scale.set(self.c.quality_var.get())
        self.speed_scale.set(self.c.speed_var.get())

    def on_reset_clicked(self):
        self.apply_settings()


    def create_widgets(self):
        self.columnconfigure(0, weight=0)
        self.columnconfigure(1, weight=1)

        ttk.Label(
            self,
            text="Voice",
        ).grid(row=0, column=0, sticky="w", padx=(0, 20), pady=10)

        voice_frame = ttk.Frame(self)
        voice_frame.grid(row=0, column=1, sticky="w")

        for col, v in enumerate(["M1", "M2", "M3", "M4", "M5"]):
            ttk.Radiobutton(
                voice_frame,
                text=v,
                value=v,
                variable=self.c.voice_var,
            ).grid(row=0, column=col, padx=geometry.whp(2), sticky="w")

        for col, v in enumerate(["F1", "F2", "F3", "F4", "F5"]):
            ttk.Radiobutton(
                voice_frame,
                text=v,
                value=v,
                variable=self.c.voice_var,
            ).grid(
                row=1,
                column=col,
                padx=geometry.whp(2),
                pady=(geometry.whp(4), 0),
                sticky="w",
            )

        ttk.Label(
            self,
            text="Quality",
        ).grid(row=1, column=0, sticky="w", padx=(0, 20), pady=10)

        quality_frame = ttk.Frame(self)
        quality_frame.grid(row=1, column=1, sticky="ew")
        quality_frame.columnconfigure(0, weight=1)

        def on_quality_change(value):
            self.c.quality_var.set(int(float(value)))

        self.quality_scale = ttk.Scale(
            quality_frame,
            from_=2,
            to=15,
            orient="horizontal",
            command=on_quality_change,
        )
        self.quality_scale.set(self.c.quality_var.get())
        self.quality_scale.grid(row=0, column=0, sticky="ew")

        ttk.Label(
            quality_frame,
            textvariable=self.c.quality_var,
            width=3,
        ).grid(row=0, column=1, padx=(10, 0))

        ttk.Label(
            self,
            text="Speed",
        ).grid(row=2, column=0, sticky="w", padx=(0, 20), pady=10)

        speed_frame = ttk.Frame(self)
        speed_frame.grid(row=2, column=1, sticky="ew")
        speed_frame.columnconfigure(0, weight=1)

        def on_speed_change(value):
            self.c.speed_var.set(round(float(value), 2))

        self.speed_scale = ttk.Scale(
            speed_frame,
            from_=0.7,
            to=2.0,
            orient="horizontal",
            command=on_speed_change,
        )
        self.speed_scale.set(self.c.speed_var.get())
        self.speed_scale.grid(row=0, column=0, sticky="ew")

        ttk.Label(
            speed_frame,
            textvariable=self.c.speed_var,
            width=5,
        ).grid(row=0, column=1, padx=(10, 0))

        ttk.Label(
            self,
            text="Max chunk length",
        ).grid(row=3, column=0, sticky="w", padx=(0, 20), pady=10)

        chunk_frame = ttk.Frame(self)
        chunk_frame.grid(row=3, column=1, sticky="w")

        ttk.Entry(
            chunk_frame,
            textvariable=self.c.max_chunk_length_var,
            width=8,
        ).grid(row=0, column=0, sticky="w")

        ttk.Label(
            chunk_frame,
            text="characters",
        ).grid(row=0, column=1, padx=(10, 0), sticky="w")

        ttk.Label(
            self,
            text="Silence between chunks",
        ).grid(row=4, column=0, sticky="w", padx=(0, 20), pady=10)

        silence_frame = ttk.Frame(self)
        silence_frame.grid(row=4, column=1, sticky="w")

        ttk.Entry(
            silence_frame,
            textvariable=self.c.silence_duration_var,
            width=8,
        ).grid(row=0, column=0, sticky="w")

        ttk.Label(
            silence_frame,
            text="seconds",
        ).grid(row=0, column=1, padx=(10, 0), sticky="w")


        buttons_frame = ttk.Frame(self)
        buttons_frame.grid(row=5, column=0, sticky="w", pady=(20, 0))

        BTN_WIDTH = 10

        save_btn = ttk.Button(
            buttons_frame,
            text="Save",
            width=BTN_WIDTH,
            padding=(0, geometry.whp(1)),
            command=self.c.save_settings
        )
        save_btn.grid(row=0, column=0, padx=(0, geometry.whp(4)))

        reset_btn = ttk.Button(
            buttons_frame,
            text="Reset",
            width=BTN_WIDTH,
            padding=(0, geometry.whp(1)),
            bootstyle="outline",
            command=self.on_reset_clicked,
        )
        reset_btn.grid(row=0, column=1)

        for i in range(6):
            self.grid_rowconfigure(i, pad=geometry.whp(3))
