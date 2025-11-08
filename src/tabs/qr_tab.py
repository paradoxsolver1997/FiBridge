import os
import tkinter as tk
from tkinter import ttk, filedialog
import logging

from src.lib.qr import generate_qr_image
from src.lib.save_image import save_image_as_bitmap, save_image_as_vector
from src.tabs.base_tab import BaseTab
from src.frames.labeled_validated_entry import LabeledValidatedEntry
from src.frames.title_frame import TitleFrame


class QRTab(BaseTab):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.qr_img = None
        self.output_dir = os.path.join(self.output_dir, "qr_output")
        self.build_content()

    def build_content(self):

        self.title_frame = TitleFrame(
            self,
            title_text="QR Code Generation",
            comment_text="Generate QR codes from text or URLs, with optional logo embedding.",
        )
        self.title_frame.pack(fill="x", padx=8, pady=(8, 4))

        # Step 1: QR Settings
        frm = ttk.LabelFrame(self, text="Step 1: QR Settings", style="Bold.TLabelframe")
        frm.pack(padx=8, pady=(4, 4), fill="x")

        content_row = ttk.Frame(frm)
        content_row.pack(fill="x", padx=0, pady=(3, 2))
        self.content_var = tk.StringVar()
        ttk.Label(content_row, text="QR Content (URL or text):").pack(
            side="left", padx=(8, 4), pady=(8, 0)
        )
        ttk.Entry(content_row, textvariable=self.content_var, width=50).pack(
            side="left", padx=(0, 4), pady=(8, 0), expand=True, fill="x"
        )

        logo_row = ttk.Frame(frm)
        logo_row.pack(fill="x", padx=0, pady=(2, 4))
        self.logo_var = tk.StringVar()
        ttk.Label(logo_row, text="Logo Image (Optional):").pack(
            side="left", padx=(8, 4)
        )
        ttk.Entry(logo_row, textvariable=self.logo_var, width=50).pack(
            side="left", padx=(0, 4), expand=True, fill="x"
        )
        ttk.Button(logo_row, text="Browse...", command=self.browse_logo).pack(
            side="left"
        )

        size_row = ttk.Frame(frm)
        size_row.pack(fill="x", padx=0, pady=(0, 12))

        self.qr_size_var = tk.IntVar(value=300)
        self.qr_size_labeled_entry = LabeledValidatedEntry(
            size_row,
            var=self.qr_size_var,
            bounds=(100, 600),
            label_prefix="QR Size",
            width=8,
        )
        self.qr_size_labeled_entry.pack(side="left", padx=(8, 24))

        self.max_logo_ratio_var = tk.DoubleVar(value=0.4)
        self.logo_ratio_labeled_entry = LabeledValidatedEntry(
            size_row,
            var=self.max_logo_ratio_var,
            bounds=(0.1, 0.9),
            label_prefix="Max Logo Ratio",
            width=8,
            enable_condition=lambda: bool(self.logo_var.get().strip()),
            trace_vars=[self.logo_var],
        )
        self.logo_ratio_labeled_entry.pack(side="left", padx=(0, 4))

        # Step 2: Generate and Save
        frm_1 = ttk.LabelFrame(
            self, text="Step 2: Generate and Save", style="Bold.TLabelframe"
        )
        frm_1.pack(padx=8, pady=8, fill="x")

        ttk.Button(
            frm_1, text="Generate and Show QR Code", command=self.do_generate
        ).pack(side="left", padx=4, pady=(12, 12))
        ttk.Button(
            frm_1,
            text="Save as Bitmap",
            command=lambda: self.save(save_image_as_bitmap),
        ).pack(side="left", padx=4, pady=(12, 12))
        ttk.Button(
            frm_1,
            text="Save as Vector",
            command=lambda: self.save(save_image_as_vector),
        ).pack(side="left", padx=4, pady=(12, 12))

    def browse_logo(self, max_size_mb=None):
        """
        Browse a single image file, supporting type filtering and size limits.
        var: tk.StringVar bound variable
        filetypes: [('Images', '*.png;*.jpg'), ...]
        max_size_mb: max file size in MB, popup if exceeded
        title: dialog title
        """
        title = "Select logo image"
        filetypes = [("Images", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff")]
        sel = filedialog.askopenfilename(title=title, filetypes=filetypes)
        if not sel:
            return
        try:
            if max_size_mb and os.path.getsize(sel) > max_size_mb * 1024 * 1024:
                self.logger.log(
                    logging.WARNING,
                    f"The selected file exceeds {max_size_mb}MB and will not be loaded: {sel}",
                )
                return
        except Exception:
            pass
        self.logo_var.set(sel)

    def do_generate(self):
        content = self.content_var.get().strip()
        logo = self.logo_var.get().strip() or None
        qr_size = self.qr_size_var.get()
        max_logo_ratio = self.max_logo_ratio_var.get()
        if not content:
            self.logger.log(logging.WARNING, "No content, please enter QR content")
            return
        try:
            self.qr_img = generate_qr_image(
                content, qr_size=qr_size, logo_path=logo, max_logo_ratio=max_logo_ratio
            )
            self.winfo_toplevel().image_preview(self.qr_img.copy())
            self.logger.info("QR code generated.")
        except Exception as e:
            self.logger.log(logging.ERROR, f"QR generation failed: {e}")

    def save(self, save_callback):
        save_callback(self.qr_img)

    def pull_str(self, s):
        """Process the string pushed from the QR code and display it in the input box."""
        self.content_var.set(s)
