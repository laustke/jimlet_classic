from pathlib import Path
import logging
import json
import threading
import tkinter as tk
from tkinter import filedialog
from ttkbootstrap.dialogs import Messagebox
from supertonic import TTS
from .utils import format_file_size, format_duration
from .sanitize_text import sanitize_text
from .save_audio import save_audio
from . import data_path

logger = logging.getLogger(__name__)

SPINNER = ["⠋","⠙","⠹","⠸","⠼","⠴","⠦","⠧","⠇","⠏"]
CHECK = "✔"

DEFAULT_SETTINGS = {
    "voice": "F1",
    "quality": 5,
    "speed": 0.9,
    "max_chunk_length": 300,
    "silence_duration": 0.3
}

class Controller:

    def __init__(self, app):
        self.app = app

        d = DEFAULT_SETTINGS

        self.voice_var = tk.StringVar(master=self.app.root, value=d["voice"])
        self.quality_var = tk.IntVar(value=d["quality"])
        self.speed_var = tk.DoubleVar(value=d["speed"])
        self.max_chunk_length_var = tk.IntVar(value=d["max_chunk_length"])
        self.silence_duration_var = tk.DoubleVar(value=d["silence_duration"])


        self.source_folder: Path | None = None
        self.text_file_names: set[str] = set()

        self.grid_empty = True
        self.conversion_performed = False

        self.is_converting = False
        self.current_index = 0

        self._spinner_job = None
        self._spinner_index = 0
        self._spinner_item = None

        self._tts: TTS | None = None

    def _start_spinner(self, item_id: str) -> None:
        self._stop_spinner()

        self._spinner_item = item_id
        self._spinner_index = 0

        def spin():
            char = SPINNER[self._spinner_index % len(SPINNER)]
            self.app.convert_tab.tree.set(item_id, "status", char)
            self._spinner_index += 1
            self._spinner_job = self.app.root.after(120, spin)

        spin()

    def _stop_spinner(self, done: bool = False) -> None:
        if self._spinner_job:
            self.app.root.after_cancel(self._spinner_job)
            self._spinner_job = None

        if self._spinner_item:
            self.app.convert_tab.tree.set(
                self._spinner_item,
                "status",
                CHECK if done else ""
            )

        self._spinner_item = None

    def open_text_files(self) -> None:
        file_paths = filedialog.askopenfilenames(
            parent=self.app.root,
            title="Select text files",
            filetypes=[("Text files", "*.txt"), ("All files", "*.*")],
        )

        if not file_paths:
            return

        self.add_files(list(file_paths))

    def on_files_dropped(self, event) -> None:
        file_paths = self.app.root.splitlist(event.data)
        self.add_files(list(file_paths))

    def add_files(self, file_paths: list[str]) -> None:
        for path in file_paths:
            p = Path(path)
            if p.is_file() and p.suffix.lower() == ".txt":
                self.add_dropped_file(path)

    def add_dropped_file(self, path: str) -> bool:
        tab = self.app.convert_tab
        p = Path(path)

        if not p.exists() or not p.is_file():
            return False

        if self.conversion_performed:
            self.new_batch()

        if self.source_folder is None:
            self.source_folder = p.parent
        elif p.parent != self.source_folder:
            Messagebox.show_info(
                "Convert first",
                "Please convert selected files first."
            )
            return False

        if p.name in self.text_file_names:
            return False

        tab.tree.insert(
            "",
            "end",
            values=(
                "",
                p.name,
                format_file_size(p.stat().st_size),
                "",
                "",
                "",
            ),
        )

        self.text_file_names.add(p.name)
        self.grid_empty = False
        return True

    def start_conversion(self) -> None:
        if self.is_converting:
            return

        if self.grid_empty:
            Messagebox.show_info(
                "Please add some files to convert",
                "Add Files"
            )
            return

        if self.conversion_performed:
            self.reset_conversion_results()

        self.is_converting = True
        self.current_index = 0
        self._convert_next()


    def _convert_next(self) -> None:
        tab = self.app.convert_tab
        items = tab.tree.get_children()

        if self.current_index >= len(items):
            self.is_converting = False
            self.conversion_performed = True
            return

        item_id = items[self.current_index]
        tab.select_row(item_id)
        self._start_spinner(item_id)

        filename = tab.tree.item(item_id, "values")[1]
        input_path = self.source_folder / filename
        output_path = input_path.with_suffix(".wav")


        def worker():
            try:
                duration_sec = self._convert_file(input_path, output_path)

                self.app.root.after(
                    0,
                    lambda: self._on_file_converted(
                        item_id,
                        output_path.name,
                        format_file_size(output_path.stat().st_size),
                        format_duration(duration_sec),
                    )
                )

            except Exception:
                logger.exception("Conversion failed: %s", input_path)
                self.app.root.after(
                    0,
                    lambda: self._on_file_converted(item_id)
                )

        threading.Thread(target=worker, daemon=True).start()

    def _on_file_converted(
        self,
        item_id: str | None = None,
        speech_file: str | None = None,
        speech_size: str | None = None,
        duration: str | None = None,
        failed: bool = False,
    ) -> None:
        tab = self.app.convert_tab

        if item_id:
            self._stop_spinner(done=not failed)
            if failed:
                tab.tree.set(item_id, "status", "✖")
            else:
                tab.update_row(
                    item_id,
                    speech_file=speech_file,
                    speech_size=speech_size,
                    duration=duration,
                )

        self.current_index += 1
        self._convert_next()

    def reset_conversion_results(self) -> None:
        tab = self.app.convert_tab

        for item_id in tab.tree.get_children():
            tab.update_row(
                item_id,
                speech_file="",
                speech_size="",
                duration="",
            )
            tab.tree.set(item_id, "status", "")

        self.current_index = 0
        self.conversion_performed = False

    def _get_tts(self) -> TTS:
        if self._tts is None:
            self._tts = TTS(
                auto_download=True
            )
        return self._tts

    def _convert_file(self, input_path: Path, output_path: Path) -> float:
        tts = self._get_tts()

        text = input_path.read_text(encoding="utf-8", errors="replace")
        text = sanitize_text(text)

        if not text.strip():
            raise ValueError("Input text is empty")

        voice_style = tts.get_voice_style(
            voice_name=self.voice_var.get()
        )

        wav, duration = tts.synthesize(
            text,
            voice_style=voice_style,
            total_steps=self.quality_var.get(),
            speed=self.speed_var.get(),
            max_chunk_length=self.max_chunk_length_var.get(),
            silence_duration=self.silence_duration_var.get(),
        )

        save_audio(wav, tts.sample_rate, str(output_path))

        return float(duration)

    def new_batch(self):
        self._stop_spinner()

        tab = self.app.convert_tab
        for item in tab.tree.get_children():
            tab.tree.delete(item)

        self.source_folder = None
        self.text_file_names.clear()

        self.grid_empty = True
        self.conversion_performed = False
        self.is_converting = False
        self.current_index = 0

    def apply_settings(self, settings: dict | None = None) -> None:
        d = settings if settings is not None else DEFAULT_SETTINGS

        self.voice_var.set(d["voice"])
        self.quality_var.set(d["quality"])
        self.speed_var.set(d["speed"])
        self.max_chunk_length_var.set(d["max_chunk_length"])
        self.silence_duration_var.set(d["silence_duration"])

    def get_settings(self) -> dict:
        return {
            "voice": self.voice_var.get(),
            "quality": self.quality_var.get(),
            "speed": self.speed_var.get(),
            "max_chunk_length": self.max_chunk_length_var.get(),
            "silence_duration": self.silence_duration_var.get(),
        }

    def save_settings(self) -> None:
        settings_path = data_path / "settings.json"

        try:
            with settings_path.open("w") as f:
                json.dump(self.get_settings(), f, indent=4)
        except Exception as exc:
            logger.exception("Failed to save settings: %s", exc)


    def load_settings(self) -> dict:
        settings_path = data_path / "settings.json"

        settings = DEFAULT_SETTINGS.copy()

        if not settings_path.exists():
            return settings

        try:
            with settings_path.open("r") as f:
                loaded = json.load(f)

            if isinstance(loaded, dict):
                settings.update(loaded)

        except Exception as exc:
            logger.exception("Failed to load settings, using defaults: %s", exc)

        return settings
