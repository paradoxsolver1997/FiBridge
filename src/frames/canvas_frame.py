import tkinter as tk
from tkinter import ttk, messagebox
from src.utils.signature_canvas import SignatureCanvas
from src.frames.base_frame import BaseFrame
from src.libs.save_image import save_image_as_vector, save_image_as_bitmap


class CanvasFrame(BaseFrame):
    def __init__(self, parent, width, height, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.master.protocol("WM_DELETE_WINDOW", self.close_canvas)
        self.canvas_width = width
        self.canvas_height = height
        self.canvas_scale = tk.DoubleVar(value=1.0)
        self.build_contents()

    def build_contents(self):
        self.transparent_var = tk.BooleanVar(value=True)
        self.crop_var = tk.BooleanVar(value=True)
        button_row = ttk.LabelFrame(self, text="Save Options")
        button_row.pack(side="bottom", fill="x", padx=8, pady=8)
        ttk.Checkbutton(
            button_row,
            text="Transparent background",
            variable=self.transparent_var,
            command=self.on_transparent_toggle,
        ).pack(side="left", padx=6)
        ttk.Checkbutton(button_row, text="Crop signature", variable=self.crop_var).pack(
            side="left", padx=6
        )
        ttk.Button(
            button_row,
            text="Save as Bitmap",
            command=lambda: self.sig.save(
                save_image_as_bitmap, cropped=self.crop_var.get()
            ),
        ).pack(side="left", pady=4)
        ttk.Button(
            button_row,
            text="Save as Vector",
            command=lambda: self.sig.save(
                save_image_as_vector, cropped=self.crop_var.get()
            ),
        ).pack(side="left", pady=4)

        main_frame = ttk.LabelFrame(self, text="Canvas", style="Bold.TLabelframe")
        main_frame.pack(fill="both", expand=True, padx=8, pady=(4, 8))
        main_row = ttk.Frame(main_frame)
        main_row.pack(fill="x", expand=True)

        self.scale_frame = ttk.LabelFrame(main_row, text="Control")
        self.scale_frame.pack(
            side="right", fill="y", expand=True, padx=(4, 4), pady=(4, 4)
        )
        self.scale_real_label = ttk.Label(self.scale_frame, text=f"Scale: 100%")
        self.scale_real_label.pack(pady=(12, 4))

        ttk.Button(
            self.scale_frame, text="Zoom in", command=lambda: self.scale_canvas(1.1)
        ).pack(pady=4)
        ttk.Button(
            self.scale_frame, text="Zoom out", command=lambda: self.scale_canvas(0.9)
        ).pack(pady=4)
        ttk.Button(self.scale_frame, text="Reset Scale", command=self.reset_scale).pack(
            pady=4
        )
        ttk.Button(
            self.scale_frame, text="Clear Canvas", command=self.clear_canvas
        ).pack(pady=4)
        ttk.Button(
            self.scale_frame, text="Close Canvas", command=self.close_canvas
        ).pack(pady=4)

        # Create canvas frame with a maximum height limit of 200
        canvas_frame = ttk.Frame(main_row, width=self.canvas_width, height=200)
        canvas_frame.pack(side="left", fill="both", expand=True)
        canvas_frame.pack_propagate(False)
        # Vertical scrollbar
        y_scroll = ttk.Scrollbar(canvas_frame, orient="vertical")
        y_scroll.pack(side="right", fill="y")
        # Create canvas and horizontal scrollbar subframe
        canvas_subframe = ttk.Frame(canvas_frame)
        canvas_subframe.pack(side="left", fill="both", expand=True)
        # Horizontal scrollbar
        x_scroll = ttk.Scrollbar(canvas_subframe, orient="horizontal")
        x_scroll.pack(side="bottom", fill="x")
        # Create canvas and bind scrollbars
        self.sig = SignatureCanvas(
            canvas_subframe, width=self.canvas_width, height=self.canvas_height
        )
        self.sig.pack(side="top", fill="both", expand=True)
        self.sig.start()
        self.sig.canvas.config(xscrollcommand=x_scroll.set, yscrollcommand=y_scroll.set)
        x_scroll.config(command=self.sig.canvas.xview)
        y_scroll.config(command=self.sig.canvas.yview)

        self.reset_scale()

    def on_transparent_toggle(self):
        pass

    def _on_scale_change(self, val):
        scale = float(val)
        self.sig.canvas.scale(tk.ALL, 0, 0, scale, scale)
        w = self.canvas_width * self.canvas_scale.get()
        h = self.canvas_height * self.canvas_scale.get()
        self.sig.canvas.config(scrollregion=(0, 0, w, h))

    def _on_update_scale_label(self, scale):
        self.scale_real_label.config(text=f"Scale: {int(scale*100)}%")

    def scale_canvas(self, scale):
        self.canvas_scale.set(self.canvas_scale.get() * scale)
        self._on_update_scale_label(self.canvas_scale.get())
        self._on_scale_change(scale)

    def reset_scale(self):
        current_scale = self.canvas_scale.get()
        if current_scale != 1.0:
            self._on_scale_change(1 / current_scale)
            self.canvas_scale.set(1.0)
        self._on_update_scale_label(1.0)
        self.sig.canvas.config(
            scrollregion=(0, 0, self.canvas_width, self.canvas_height)
        )

    def clear_canvas(self):
        self.sig.clear()
        self.sig.start()

    def close_canvas(self):
        if self.sig.is_dirty:
            # Raise the window before the popup
            self.master.lift()
            result = messagebox.askyesno(
                "Unsaved Changes", "The canvas has unsaved changes. Are you sure you want to close it?", parent=self.master
            )
            # Raise the window again to prevent it from being obscured by the main window
            self.master.lift()
            if not result:
                return
        self.master.destroy()
