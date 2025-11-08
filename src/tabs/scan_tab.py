import os
import tkinter as tk
from tkinter import ttk
from src.tabs.base_tab import BaseTab
from src.frames.title_frame import TitleFrame
import logging
from src.frames.text_frame import TextFrame


class ScanTab(BaseTab):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.qr_img = None
        self.output_dir = os.path.join(self.output_dir, "qr_output")
        self.build_content()

    def build_content(self):

        self.title_frame = TitleFrame(
            self,
            title_text="Remote Scan",
            comment_text="Scan QR codes from your phone, and push it back to your computer.",
        )
        self.title_frame.pack(fill="x", padx=8, pady=(8, 4))

        remote_frame = ttk.LabelFrame(
            self, text="Scan on Your Phone", style="Bold.TLabelframe"
        )
        remote_frame.pack(fill="x", padx=8, pady=(4, 8))
        ttk.Label(
            remote_frame,
            text='Step 1: Configure "Server Setup" and connect to your phone. Click "Help" for details.',
        ).pack(side="top", fill="x", padx=8, pady=(8, 4))
        ttk.Label(remote_frame, text="Step 2: Scan any QR code using your phone.").pack(
            side="top", fill="x", padx=8, pady=(4, 4)
        )
        row_3 = ttk.Frame(remote_frame)
        row_3.pack(side="top", fill="x", padx=8, pady=(4, 4))
        ttk.Label(row_3, text="Step 3: Click").pack(side="left", padx=0, pady=(0, 4))
        ttk.Button(row_3, text="Fetch Scan", command=lambda: self.pull_text()).pack(
            side="left", padx=(2, 2), pady=(0, 4)
        )
        ttk.Label(row_3, text="to view the scanned text in a popup.").pack(
            side="left", padx=0, pady=(0, 4)
        )

    def pull_text(self):
        """Pull latest_metadata and pop up the draw canvas."""

        self.log(logging.INFO, "Attempting to extract latest_metadata and pop up the draw canvas...")
        metadata = self.server_frame._server_manager.latest_metadata
        if not metadata or metadata.get("type") != "text":
            self.log(logging.WARNING, "No valid text metadata found.")
            return
        file_name = metadata.get("info")
        if not file_name:
            self.log(logging.WARNING, "draw metadata is missing file name!")
            return
        text_file = os.path.join(self.cache_dir, file_name)
        if not os.path.exists(text_file):
            self.log(logging.ERROR, f"Text file not found: {text_file}")
            return
        with open(text_file, "r", encoding="utf-8") as f:
            text = f.read()
        self.create_text(text)

    def create_text(self, text=None):
        self.text_window = tk.Toplevel(self)
        self.text_window.title("Signature Canvas")
        self.text_window.geometry(self.set_text_geometry())

        self.canvas_frame = TextFrame(self.text_window)
        self.canvas_frame.pack(fill="both", expand=True)
        if text:
            self.canvas_frame.set_text(text)

    def set_text_geometry(self):
        main_x = self.winfo_toplevel().winfo_x()
        main_y = self.winfo_toplevel().winfo_y()
        main_w = self.winfo_toplevel().winfo_width()
        main_h = self.winfo_toplevel().winfo_height()
        popup_w = 640
        popup_h = 360
        # Make the popup window stick to the right side of the main window
        popup_x = main_x + main_w
        popup_y = main_y

        return f"{popup_w}x{popup_h}+{popup_x}+{popup_y}"
