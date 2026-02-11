from urllib.parse import urlencode
import webbrowser
from tkinter import ttk
from ..geometry import geometry
from .. import config as conf

class AboutTab(ttk.Frame):
    def __init__(self, app):
        self.app = app
        self.c = self.app.c
        super().__init__(
            self.app.notebook,
            padding=(geometry.whp(4), geometry.whp(4))
        )
        self.create_widgets()

    def create_widgets(self):
        about_text = (
            "Jimlet Text-To-Speech Converter\n"
            "Free non-commercial edition\n"
            "Website: https://jimlet.com\n"
            "Engine profile: Tonic\n"
            f"Version: {conf.APP_VERSION}\n"
            f"Relelase date: {conf.APP_RELEASE_DATE}\n\n"
            "Jimlet is a local text-to-speech conversion tool.\n"
            "It converts text files into audio using an offline speech engine.\n\n"

            "Please read the LICENSE.txt file included with this application.\n\n"

            "Check out Jimlet Pro TTS Converter for the newest voice engine,\n"
            "multilingual support, and extended features.\n"
        )

        lbl = ttk.Label(
            self,
            text=about_text,
            justify="left",
        )
        lbl.grid(row=0, column=0, sticky="nsew")

        def open_website():

            base_url = "https://jimlet.com/"
            params = {
                "utm_source": "jimlet",
                "utm_medium": "app",
                "utm_campaign": "standard",
                "utm_content": "about_tab_button",
            }

            url = f"{base_url}?{urlencode(params)}"
            webbrowser.open(url)

        btn = ttk.Button(
            self,
            text="Visit website",
            command=open_website,
            padding=(geometry.whp(2), geometry.whp(1))
        )
        btn.grid(row=1, column=0, sticky="w", pady=(geometry.whp(4),0))

        self.grid_columnconfigure(0, weight=1)
