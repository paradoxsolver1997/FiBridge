import tkinter as tk
from tkinter import ttk, filedialog
from src.tabs.base_tab import BaseTab
import os
import logging

from src.frames.title_frame import TitleFrame


class ShareTab(BaseTab):
    """
    Tab for sharing files between PC and mobile devices.
    Integrates server configuration for file transfer.
    """

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.output_dir = os.path.join(self.output_dir, "share_output")
        self.out_dir_var = tk.StringVar(value=self.output_dir)
        if not os.path.exists(self.out_dir_var.get()):
            os.makedirs(self.out_dir_var.get(), exist_ok=True)
        self.build_content()

    def build_content(self):
        # Server configuration widget

        self.title_frame = TitleFrame(
            self,
            title_text="File Share",
            comment_text="Share files between PC and mobile devices.",
        )
        self.title_frame.pack(fill="x", padx=(8, 8), pady=(8, 4))

        input_frame = ttk.LabelFrame(
            self, text="Option 1: Send Files to Phone", style="Bold.TLabelframe"
        )
        input_frame.pack(fill="x", padx=(8, 8), pady=(0, 8))
        # Input files
        input_row = ttk.Frame(input_frame)
        input_row.pack(fill="x", padx=0, pady=(4, 0))
        self.files_var = tk.StringVar()
        ttk.Label(input_row, text="Step 1. Choose files to send:").pack(
            side="left", padx=(8, 8)
        )
        ttk.Entry(input_row, textvariable=self.files_var).pack(
            side="left", padx=(2, 0), expand=True, fill="x"
        )
        ttk.Button(
            input_row,
            text="Browse...",
            command=lambda: self.browse_files(
                var=self.files_var,
                filetypes=[("All Files", "*.*")],
                max_size_mb=None,
                multi=True,
                title="Select files",
            ),
        ).pack(side="left", padx=4)
        ttk.Label(
            input_frame,
            text='Step 2: Configure "Server Setup" and connect to your phone. Click "Help" for details.',
        ).pack(side="top", fill="x", padx=8, pady=(4, 0))
        ttk.Label(
            input_frame, text="Step 3: On your phone, choose files and save them."
        ).pack(side="top", fill="x", padx=8, pady=(8, 4))

    def browse_files(
        self, var, filetypes, max_size_mb=None, multi=True, title="Select files"
    ):
        """
        General file selection, supports multi-select, type filter, size limit.
        var: tk.StringVar bound variable
        filetypes: [('Images', '*.png;*.jpg'), ...]
        max_size_mb: max file size in MB, popup if exceeded
        multi: allow multi-select
        title: dialog title
        """
        dlg = filedialog.askopenfilenames if multi else filedialog.askopenfilename
        sel = dlg(title=title, filetypes=filetypes)
        if not sel:
            return
        files = sel if isinstance(sel, (list, tuple)) else [sel]
        oversize = []
        if max_size_mb:
            for f in files:
                try:
                    if os.path.getsize(f) > max_size_mb * 1024 * 1024:
                        oversize.append(f)
                except Exception:
                    pass
        if oversize:
            self.log(
                logging.WARNING,
                f"The following files exceed {max_size_mb}MB and will not be loaded:\n"
                + "\n".join(oversize),
            )
            files = [f for f in files if f not in oversize]
        if files:
            var.set("\n".join(files))

    def get_file_list(self):
        return self.files_var.get().strip().split("\n")
