import tkinter as tk
from tkinter import ttk
import tkinter.font as tkfont
from PIL import Image, ImageTk
import logging
import shutil, os
import sys
from tkinter import messagebox

from src.tabs.qr_tab import QRTab
from src.tabs.signature_tab import SignatureTab
from src.tabs.share_tab import ShareTab
from src.tabs.fetch_tab import FetchTab
from src.tabs.scan_tab import ScanTab
from src.tabs.about_tab import AboutTab
from src.frames.server_frame import ServerFrame
from src.frames.tool_frame import ToolFrame

from src.utils.logger import Logger


def init_styles():
    style = ttk.Style()
    # LabelFrame bold title font
    style.configure("Italic.TLabelframe.Label", font=("Segoe UI", 10, "italic"))
    style.configure("Bold.TLabelframe.Label", font=("Segoe UI", 10, "bold"))
    style.configure("Gray.TLabelframe.Label", foreground="gray")
    # Other styles that can be uniformly set:
    style.configure("TButton", font=("Segoe UI", 10))
    style.configure("TLabel", font=("Segoe UI", 10))
    style.configure("TEntry", font=("Segoe UI", 10))
    # You can continue to add other control styles


class App(tk.Tk):
    """Modular App for ImBridge (signature-focused subset)."""

    def __init__(self):
        super().__init__()

        init_styles()
        self.title("ImBridge")
        self.geometry("600x600")
        tkfont.nametofont("TkDefaultFont").config(family="Segoe UI", size=10)
        # Logging system
        self.logger = Logger(gui_widget=None)  # Bind with log_text later
        self.output_dir = os.path.join(
            os.path.dirname(os.path.dirname(__file__)), "output"
        )
        self.cache_dir = os.path.join(self.output_dir, "cache")
        # Bind window close event, clear cache on normal close
        self.protocol("WM_DELETE_WINDOW", self._on_app_exit)
        self.build_content()
        self.check_ssl_certificates()

    def build_content(self):
        # Main frame, divided into upper and lower parts, using grid for layout
        main_frame = ttk.Frame(self)
        main_frame.grid(row=0, column=0, sticky="nsew")
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=1)
        main_frame.rowconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=0)
        main_frame.columnconfigure(0, weight=3)
        main_frame.columnconfigure(1, weight=1)

        # Notebook main area
        self.nb = ttk.Notebook(main_frame)
        self.nb.grid(row=0, column=0, sticky="nsew")
        self.nb.bind("<<NotebookTabChanged>>", self.on_tab_changed)

        # Bottom area
        bottom_frame = ttk.LabelFrame(
            main_frame, text="Watch Panel", style="Bold.TLabelframe"
        )
        bottom_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=4, pady=4)
        bottom_frame.rowconfigure(0, weight=1)
        bottom_frame.columnconfigure(0, weight=0)
        bottom_frame.columnconfigure(1, weight=1)

        row_1 = ttk.Frame(bottom_frame)
        row_1.grid(row=0, column=0, columnspan=2, sticky="ew", pady=(8, 0))
        row_1.columnconfigure(0, weight=1)
        row_1.columnconfigure(1, weight=1)
        self.server_frame = ServerFrame(row_1)
        self.server_frame.grid(row=0, column=0, sticky="nsew")
        self.tool_frame = ToolFrame(row_1)
        self.tool_frame.grid(row=0, column=1, sticky="nsew")

        row_2 = ttk.Frame(bottom_frame)
        row_2.grid(row=1, column=0, columnspan=2, sticky="ew")
        log_frame = ttk.LabelFrame(row_2, text="Log Output")
        log_frame.grid(row=0, column=0, sticky="ew")
        self.preview_frame = ttk.LabelFrame(
            row_2, text="Preview", width=160, height=160, relief="groove"
        )
        self.preview_frame.grid(row=0, column=1, sticky="nsew", padx=0, pady=0)
        log_scroll = ttk.Scrollbar(log_frame, orient="vertical")
        log_text = tk.Text(
            log_frame,
            height=9,
            width=60,
            state="disabled",
            font=("Consolas", 10),
            yscrollcommand=log_scroll.set,
        )
        log_text.grid(row=0, column=0, sticky="ew", padx=4, pady=2)
        self.logger.set_gui_widget(log_text)
        log_scroll.config(command=log_text.yview)
        log_scroll.grid(row=0, column=1, sticky="ns")
        log_frame.rowconfigure(0, weight=1)
        log_frame.columnconfigure(0, weight=1)
        row_2.columnconfigure(0, weight=1)
        row_2.columnconfigure(1, weight=1)

        self.qr_tab = QRTab(self.nb)
        self.nb.add(self.qr_tab, text=" QR Generator ")
        self.scan_tab = ScanTab(self.nb)
        self.nb.add(self.scan_tab, text=" Remote Scan ")
        # SignatureTab only handles logic and callbacks, does not directly hold CanvasFrame
        self.signature_tab = SignatureTab(self.nb)
        self.nb.add(self.signature_tab, text=" Draw & Sign ")
        self.shr_tab = ShareTab(self.nb)
        self.nb.add(self.shr_tab, text=" File Share ")
        self.ftc_tab = FetchTab(self.nb)
        self.nb.add(self.ftc_tab, text=" File Fetch ")
        self.abt_tab = AboutTab(self.nb)
        self.nb.add(self.abt_tab, text=" About ")

        self.nb.select(0)

    def on_tab_changed(self, event=None):
        self.clear_preview()
        current_tab_id = self.nb.select()
        current_tab_obj = self.nb.nametowidget(current_tab_id)

        if current_tab_obj in (self.qr_tab, self.abt_tab):
            self.server_frame.deactivate()
        else:
            self.server_frame.activate()

        if current_tab_obj in (self.scan_tab, self.shr_tab, self.ftc_tab, self.abt_tab):
            self.tool_frame.deactivate()
        else:
            self.tool_frame.activate()

    def image_preview(self, image: Image.Image):
        """
        Display imgtk in preview_frame and keep reference to prevent GC.
        """
        self.clear_preview()
        if self.preview_frame:
            try:
                w = self.preview_frame.winfo_width()
                h = self.preview_frame.winfo_height()
                if w < 10 or h < 10:
                    # Default size if not properly initialized yet
                    w, h = 10, 10
                img = image.copy()
                img.thumbnail((w, h))
                imgtk = ImageTk.PhotoImage(img)
                label = tk.Label(self.preview_frame, image=imgtk)
                label.image = imgtk
                label.pack(expand=True)
            except Exception as e:
                tk.Label(self.preview_frame, text="Preview failed").pack(expand=True)

    def clear_preview(self):
        if self.preview_frame:
            for w in self.preview_frame.winfo_children():
                w.destroy()

    def _on_app_exit(self):
        self.clear_output_cache()
        self.destroy()

    def clear_output_cache(self):
        cache_dir = self.cache_dir
        if os.path.exists(cache_dir):
            for f in os.listdir(cache_dir):
                fp = os.path.join(cache_dir, f)
                try:
                    if os.path.isfile(fp) or os.path.islink(fp):
                        os.unlink(fp)
                    elif os.path.isdir(fp):
                        shutil.rmtree(fp)
                except Exception as e:
                    self.log(logging.ERROR, f"Failed to delete {fp}: {e}")

    def log(self, level, msg):
        self.logger.log(level, msg)


    def check_ssl_certificates(self):
        # Use the directory of this file for configs
        cert_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)))
        cert_path = os.path.join(cert_dir, 'cert.pem')
        key_path = os.path.join(cert_dir, 'key.pem')
        if not (os.path.exists(cert_path) and os.path.exists(key_path)):
            msg = (
                "SSL certificate files not found in " + cert_dir + ".\n"
                "HTTPS features will NOT work.\n\n"
                "Follow 'ReadMe' instruction to generate cert.pem and key.pem before starting FiBridge."
            )
            try:
                self.log(logging.WARNING, "FiBridge - Certificate Missing: " + msg)
            except Exception:
                print(msg)
            # Do NOT exit, just warn the user



