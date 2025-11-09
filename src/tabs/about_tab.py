import os
from tkinter import ttk
import tkinter.font as tkfont
import webbrowser
from src.tabs.base_tab import BaseTab
from src.frames.title_frame import TitleFrame
import tkinter as tk

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
        self.title_frame.pack(fill="x", padx=(8, 8), pady=(8, 4))

        self.info_frame = ttk.LabelFrame(self, text="Information", style="Bold.TLabelframe")
        self.info_frame.pack(fill="x", padx=(8, 8), pady=(4, 4))
        self.author = ttk.Label(self.info_frame, text="Author: Paradoxsolver")
        self.author.pack(side="top", anchor="w", padx=8, pady=(4, 0))
        
        self.license_row = ttk.Frame(self.info_frame)
        self.license_row.pack(side="top", fill="x", padx=8, pady=(2, 2))
        self.license_label = ttk.Label(self.license_row, text="License: ")
        self.license_label.pack(side="left", anchor="w", padx=(0, 0), pady=(0, 0))
        self.license_link = ttk.Label(self.license_row, text="MIT License", foreground="blue", cursor="hand2")
        self.license_link.pack(side="left", anchor="w", padx=0, pady=(0, 0))
        self.render_hyperlink_label(self.license_link)
        self.license_link.bind("<Button-1>", lambda e: self.show_license())

        self.project_row = ttk.Frame(self.info_frame)
        self.project_row.pack(side="top", fill="x", padx=8, pady=(2, 2))
        self.project_label = ttk.Label(self.project_row, text="Project: ")
        self.project_label.pack(side="left", anchor="w", padx=(0, 0), pady=(0, 0))
        self.project_link = ttk.Label(self.project_row, text="https://github.com/paradoxsolver1997/FiBridge", foreground="blue", cursor="hand2")
        self.project_link.pack(side="left", anchor="w", padx=0, pady=(0, 0))
        self.render_hyperlink_label(self.project_link)
        self.project_link.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/paradoxsolver1997/FiBridge"))


        self.thanks_frame = ttk.LabelFrame(self, text="Special Thanks", style="Bold.TLabelframe")
        self.thanks_frame.pack(fill="x", padx=(8, 8), pady=(4, 4))
        self.row_1 = ttk.Frame(self.thanks_frame)
        self.row_1.pack(side="top", fill="x", padx=8, pady=(2, 2))
        self.row_1_label = ttk.Label(self.row_1, text="Flask:")
        self.row_1_label.pack(side="left", anchor="w", padx=(0, 0), pady=(0, 0))
        self.row_1_link = ttk.Label(self.row_1, text="https://flask.palletsprojects.com/", foreground="blue", cursor="hand2")
        self.row_1_link.pack(side="left", anchor="w", padx=0, pady=(0, 0))
        self.render_hyperlink_label(self.row_1_link)
        self.row_1_link.bind("<Button-1>", lambda e: webbrowser.open("https://flask.palletsprojects.com/"))

        self.row_2 = ttk.Frame(self.thanks_frame)
        self.row_2.pack(side="top", fill="x", padx=8, pady=(2, 4))
        self.row_2_label = ttk.Label(self.row_2, text="html5-qrcode:")
        self.row_2_label.pack(side="left", anchor="w", padx=(0, 0), pady=(0, 0))
        self.row_2_link = ttk.Label(self.row_2, text="https://github.com/mebjas/html5-qrcode", foreground="blue", cursor="hand2")
        self.row_2_link.pack(side="left", anchor="w", padx=0, pady=(0, 0))
        self.render_hyperlink_label(self.row_2_link)
        self.row_2_link.bind("<Button-1>", lambda e: webbrowser.open("https://github.com/mebjas/html5-qrcode"))

        self.title_frame.pack(fill="x", padx=(8, 8), pady=(2, 2))
        self.help_frame = ttk.LabelFrame(
            self, text="Help & Documentation", style="Bold.TLabelframe"
        )
        self.help_frame.pack(fill="x", padx=(8, 8), pady=(2, 2))

        ttk.Button(self.help_frame, text="Open Help Document", command=lambda: webbrowser.open(f"file://{help_path}")).pack(
            side="left", padx=2, pady=(2, 2))
        

    def show_license(self):
        license_path = os.path.abspath(os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "LICENSE"))
        try:
            with open(license_path, "r", encoding="utf-8") as f:
                license_text = f.read()
        except Exception as ex:
            license_text = f"Failed to read LICENSE: {ex}"
        win = tk.Toplevel(self)
        win.title("MIT License")
        win.geometry("720x480")
        win.grab_set()
        frame = tk.Frame(win, bg="white")
        frame.pack(fill="both", expand=True)
        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")
        text = tk.Text(frame, wrap="word", font=("Consolas", 11), bg="white", fg="#222", yscrollcommand=scrollbar.set)
        text.insert("1.0", license_text)
        text.config(state="disabled")
        text.pack(fill="both", expand=True, padx=8, pady=8)
        scrollbar.config(command=text.yview)


    def render_hyperlink_label(self, label: ttk.Label):
        underline_font = tkfont.Font(self, label.cget("font"))
        underline_font.configure(underline=True, family="Segoe UI", size=10, weight="normal")
        label.configure(font=underline_font)
