import tkinter as tk
from tkinter import ttk
import os
import logging

import os
from PIL import Image, ImageTk

from src.tabs.base_tab import BaseTab
from src.frames.title_frame import TitleFrame
from src.frames.labeled_validated_entry import LabeledValidatedEntry
from src.frames.canvas_frame import CanvasFrame


class SignatureTab(BaseTab):
    def __init__(self, parent, title=None):
        super().__init__(parent, title=title)
        self.output_dir = os.path.join(self.output_dir, "signature_output")
        self.out_dir_var = tk.StringVar(value=self.output_dir)
        if not os.path.exists(self.out_dir_var.get()):
            os.makedirs(self.out_dir_var.get(), exist_ok=True)
        self.canvas_width = 450
        self.canvas_height = 150
        self.canvas_width_var = tk.IntVar(value=self.canvas_width)
        self.canvas_height_var = tk.IntVar(value=self.canvas_height)
        self.canvas_window = None
        self.build_content()

    def build_content(self):
        self.title_frame = TitleFrame(
            self,
            title_text="Draw as You Wish",
            comment_text="Draw or sign on the canvas below. Use the controls to adjust size and scale.",
        )
        self.title_frame.pack(fill="x", padx=8, pady=(8, 4))

        size_frame = ttk.LabelFrame(
            self, text="Option 1: Draw in Local Canvas", style="Bold.TLabelframe"
        )
        size_frame.pack(fill="x", padx=8, pady=(4, 8))
        self.width_labeled_entry = LabeledValidatedEntry(
            size_frame,
            var=self.canvas_width_var,
            bounds=(1, 1920),
            label_prefix="Width",
            show_limits=False,
            width=4,
        )
        self.width_labeled_entry.pack(side="left", padx=(12, 6), pady=(4, 8))
        self.height_labeled_entry = LabeledValidatedEntry(
            size_frame,
            var=self.canvas_height_var,
            bounds=(1, 1920),
            label_prefix="Height",
            show_limits=False,
            width=4,
        )
        self.height_labeled_entry.pack(side="left", padx=(12, 6), pady=(4, 8))
        ttk.Button(
            size_frame, text="Create Local Canvas", command=self.create_canvas
        ).pack(side="left", padx=(12, 6), pady=(4, 8))

        remote_frame = ttk.LabelFrame(
            self, text="Option 2: Draw in Remote Canvas", style="Bold.TLabelframe"
        )
        remote_frame.pack(side="left", fill="x", expand=True, padx=8, pady=(4, 8))
        ttk.Label(
            remote_frame, text='1. Configure "Server Setup". Click "Help" for details'
        ).pack(side="top", fill="x", padx=8, pady=(8, 4))
        ttk.Label(remote_frame, text="2. Draw or sign on your phone.").pack(
            side="top", fill="x", padx=8, pady=(4, 4)
        )
        row_3 = ttk.Frame(remote_frame)
        row_3.pack(side="top", fill="x", padx=8, pady=(4, 4))
        ttk.Label(row_3, text="3. Click").pack(side="left", padx=0, pady=(0, 4))
        ttk.Button(row_3, text="Fetch Image", command=lambda: self.pull_draw()).pack(
            side="left", padx=(2, 2), pady=(0, 4)
        )
        ttk.Label(row_3, text="to retrieve the latest drawing.").pack(
            side="left", padx=0, pady=(0, 4)
        )

    def create_canvas(self, img=None):
        self.canvas_window = tk.Toplevel(self)
        self.canvas_window.title("Signature Canvas")
        self.canvas_window.geometry(self.set_canvas_geometry())

        self.canvas_frame_popup = CanvasFrame(
            self.canvas_window,
            width=self.canvas_width_var.get(),
            height=self.canvas_height_var.get(),
        )
        self.canvas_frame_popup.pack(fill="both", expand=True)
        # Initialize size, scaling, and scrollbars

        if img:
            try:
                tk_img = ImageTk.PhotoImage(img)
                self.canvas_frame_popup.sig._loaded_img = tk_img  # Prevent GC
                self.canvas_frame_popup.sig.canvas.create_image(
                    0, 0, anchor="nw", image=tk_img
                )
                self.log(logging.INFO, f"Rendering successful in popup canvas")
            except Exception as e:
                self.log(logging.ERROR, f"Failed to render draw image: {e}")

    def set_canvas_geometry(self):
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

    def pull_draw(self):
        """Pull latest_metadata and pop up the draw canvas."""

        self.log(logging.INFO, "Attempting to extract latest_metadata and pop up the draw canvas...")
        metadata = self.server_frame._server_manager.latest_metadata
        if not metadata or metadata.get("type") != "draw":
            self.log(logging.WARNING, "No valid draw metadata found.")
            return
        draw_file = metadata.get("info")
        if not draw_file:
            self.log(logging.WARNING, "Draw metadata is missing filename.")
            return
        image_path = os.path.join(self.cache_dir, os.path.basename(draw_file))
        if not os.path.exists(image_path):
            self.log(logging.WARNING, f"No valid draw file found: {image_path}")
            return
        # Directly get size from image
        try:
            img = Image.open(image_path)
            width, height = img.size
        except Exception as e:
            self.log(logging.ERROR, f"Failed to load draw image: {e}")
            return
        # Set canvas size variables
        self.canvas_width_var.set(width)
        self.canvas_height_var.set(height)
        self.create_canvas(img)

    def get_canvas_size(self):
        return {
            "width": self.canvas_width_var.get(),
            "height": self.canvas_height_var.get(),
        }
