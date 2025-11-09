import tkinter as tk
from tkinter import ttk, filedialog
from src.tabs.base_tab import BaseTab
import os
import logging

from src.frames.title_frame import TitleFrame


class FetchTab(BaseTab):
    """
    Tab for sharing files between PC and mobile devices.
    Integrates server configuration for file transfer.
    """

    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.output_dir = os.path.join(self.output_dir, "share_output")
        """
        self.out_dir_var = tk.StringVar(value=self.output_dir)
        if not os.path.exists(self.out_dir_var.get()):
            os.makedirs(self.out_dir_var.get(), exist_ok=True)
        """
        self.build_content()

    def build_content(self):
        # Server configuration widget

        self.title_frame = TitleFrame(
            self,
            title_text="File Fetch",
            comment_text="Fetch files from mobile devices to PC.",
        )
        self.title_frame.pack(fill="x", padx=(8, 8), pady=(8, 4))

        output_frame = ttk.LabelFrame(
            self, text="Fetch Files from Phone:", style="Bold.TLabelframe"
        )
        output_frame.pack(fill="x", padx=(8, 8), pady=(4, 4))
        """
        output_row = ttk.Frame(output_frame)
        output_row.pack(fill='x', padx=0, pady=(4, 0))
        ttk.Label(output_row, text='Step 1. Select folder to receive:').pack(side="left", padx=(8, 8))
        ttk.Entry(output_row, textvariable=self.out_dir_var).pack(side='left', padx=(0, 0), expand=True, fill='x')
        ttk.Button(output_row, text='Select...', command=lambda: self.select_out_dir()).pack(side='left', padx=4)
        """
        ttk.Label(
            output_frame,
            text='Step 1: Configure "Server Setup" and click "Start Server".',
        ).pack(side="top", fill="x", padx=8, pady=(4, 0))
        ttk.Label(output_frame, text="Step 2: Open the URL using your phone.").pack(
            side="top", fill="x", padx=8, pady=(4, 0)
        )
        ttk.Label(output_frame, text='Step 3: Browse files and click "Send".').pack(
            side="top", fill="x", padx=8, pady=(8, 4)
        )

        row_3 = ttk.Frame(output_frame)
        row_3.pack(side="top", fill="x", padx=8, pady=(4, 4))
        ttk.Label(row_3, text="Step 4: Click").pack(side="left", padx=0, pady=(0, 4))
        ttk.Button(row_3, text="Fetch Files", command=lambda: self.pull_files()).pack(
            side="left", padx=(2, 2), pady=(0, 4)
        )
        ttk.Label(row_3, text="to save.").pack(side="left", padx=0, pady=(0, 4))

    """
    def select_out_dir(self, title='Select output folder'):
        sel = filedialog.askdirectory(title=title)
        if sel:
            self.out_dir_var.set(sel)
    """

    def pull_files(self):
        """Pull latest_metadata and save files"""

        self.log(logging.INFO, "Attempting to extract latest_metadata and save files...")
        metadata = self.server_frame._server_manager.latest_metadata
        if not metadata or (metadata.get("type") not in {"text", "draw", "file"}):
            self.log(logging.WARNING, "No valid share metadata found.")
            return
        file_names = metadata.get("info", [])
        if not file_names:
            self.log(logging.WARNING, "share metadata is missing file name list!")
            return
        while True:
            out_dir = filedialog.askdirectory(
                title="Select Fetch Folder", initialdir=self.output_dir
            )
            if out_dir:
                break
            import tkinter.messagebox as mb

            res = mb.askyesno(
                "No Fetch Folder Provided",
                "You did not provide a Fetch Folder. If you continue, you may not be able to fetch these files after the cache is cleared. Do you want to exit?",
            )
            if res:
                self.log(logging.WARNING, "No output directory selected.")
                return
            # else: continue loop, let user select again
        for file_name in file_names:
            print(f"[pull_files] fetching: {file_name}")
            src_file = os.path.join(self.cache_dir, file_name)
            print(f"[pull_files] src_file: {src_file}")
            if not os.path.exists(src_file):
                self.log(logging.ERROR, f"File not found in cache: {src_file}")
                continue
            dest_file = os.path.join(out_dir, os.path.basename(file_name))
            try:
                with open(src_file, "rb") as sf, open(dest_file, "wb") as df:
                    df.write(sf.read())
                self.log(logging.INFO, f"File saved: {dest_file}")
            except Exception as e:
                self.log(logging.ERROR, f"Failed to save file {dest_file}: {e}")
