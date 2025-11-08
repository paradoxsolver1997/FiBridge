import os
from tkinter import ttk
import webbrowser
from src.tabs.base_tab import BaseTab
from src.frames.title_frame import TitleFrame
from tkinter import Label, LEFT

help_path = os.path.abspath(
            os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "static", "help.html")
        )

class AboutTab(BaseTab):
    """
    Tab for sharing files between PC and mobile devices.
    Integrates server configuration for file transfer.
    """

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.build_content()

    def build_content(self):
        # Server configuration widget

        self.title_frame = TitleFrame(
            self,
            title_text="About FiBridge",
            comment_text="A secure, local bridge for file and data sharing between PC and mobile devices.",
        )
        self.title_frame.pack(fill="x", padx=(8, 8), pady=(8, 2))

        info_text = [
            "Author: Paradoxsolver",
            "License: MIT",
            "Project: https://github.com/paradoxsolver1997/FiBridge"
        ]

        self.title_frame = TitleFrame(
            self,
            title_text="Basic Information",
            comment_text=info_text,
        )
        self.title_frame.pack(fill="x", padx=(8, 8), pady=(2, 2))

        # Credits/Info
        thanks = [
            "Flask (https://flask.palletsprojects.com/)",
            "html5-qrcode (https://github.com/mebjas/html5-qrcode)",
        ]

        self.title_frame = TitleFrame(
            self,
            title_text="Special Thanks",
            comment_text=thanks,
        )
        self.title_frame.pack(fill="x", padx=(8, 8), pady=(2, 2))

        self.help_frame = ttk.LabelFrame(
            self, text="Help & Documentation", style="Bold.TLabelframe"
        )
        self.help_frame.pack(fill="x", padx=(8, 8), pady=(2, 2))

        ttk.Button(self.help_frame, text="Help", command=lambda: webbrowser.open(f"file://{help_path}"), width=6).pack(
            side="right", padx=2
        )
