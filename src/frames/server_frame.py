import tkinter as tk
from tkinter import ttk
import webbrowser
import os
import logging

from src.utils.server_manager import ServerManager
from src.frames.labeled_validated_entry import LabeledValidatedEntry
from src.frames.base_frame import BaseFrame
from src.lib.qr import generate_qr_image

help_path = os.path.abspath(
            os.path.join(os.path.dirname(os.path.dirname(__file__)), "static", "help.html")
        )


class ServerFrame(BaseFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.host_ip = "127.0.0.1"
        self.port_var = tk.IntVar(value=5000)
        self._server_manager = ServerManager(log_func=self.log)
        self.ip_options = [
            ip for ip in self._server_manager.list_local_ips() if ip != self.host_ip
        ]
        self.ip_var = tk.StringVar(
            value=self.ip_options[0] if self.ip_options else self.host_ip
        )
        self.build_contents()

    def build_contents(self):

        self.main_frame = ttk.LabelFrame(self, text="Server Setup")
        self.main_frame.pack(fill="x")

        ttk.Label(self.main_frame, text="IP/Port:").pack(
            side="left", padx=(8, 8), pady=8
        )
        ttk.Combobox(
            self.main_frame,
            values=self.ip_options,
            textvariable=self.ip_var,
            state="readonly",
            width=12,
        ).pack(side="left", padx=0, pady=8)
        self.port_entry = LabeledValidatedEntry(
            self.main_frame,
            var=self.port_var,
            bounds=(1024, 65535),
            label_prefix="",
            show_limits=False,
            width=5,
        )
        self.port_entry.pack(side="left", padx=0, pady=8)
        # Status Entry
        self.status_var = tk.StringVar()
        self.status_entry = ttk.Entry(
            self.main_frame,
            textvariable=self.status_var,
            width=4,
            state="readonly",
            justify="center",
            font=("Segoe UI", 10, "bold"),
        )
        self.status_entry.pack(side="left", padx=0, pady=8)
        self._update_status()

        ttk.Button(self.main_frame, text="Help", command=lambda: webbrowser.open(f"file://{help_path}"), width=6).pack(
            side="right", padx=2
        )
        ttk.Button(self.main_frame, text="Cache", command=self._on_cache, width=6).pack(
            side="right", padx=2
        )
        self.server_btn = ttk.Button(
            self.main_frame, text="Start Server", command=self.toggle_server, width=10
        )
        self.server_btn.pack(side="right", padx=2)

    def _update_status(self):
        if getattr(self._server_manager, "is_running", False):
            self.status_var.set("ON")
            self.status_entry.config(foreground="green")
        else:
            self.status_var.set("OFF")
            self.status_entry.config(foreground="red")

    def get_url(self):
        # Respect HTTP/HTTPS based on server's SSL context
        scheme = getattr(self._server_manager, "scheme", "http")
        return f"{scheme}://{self.ip_var.get()}:{self.port_var.get()}/"

    def toggle_server(self):

        if not hasattr(self, "_server_manager") or self._server_manager is None:
            self.log(
                logging.ERROR, "ServerManager instance missing! Cannot start server."
            )
            return
        if not self._server_manager.is_running:
            self.log(logging.INFO, "Starting web server...May take several seconds...")
            try:
                self._server_manager.host = self.ip_var.get()
                self._server_manager.port = int(self.port_var.get())
                self._server_manager.start()
                self.server_btn.config(text="Stop Server")
                self._update_status()
                scheme = getattr(self._server_manager, "scheme", "http")
                self.winfo_toplevel().image_preview(generate_qr_image(self.get_url()))
                self.log(
                    logging.INFO,
                    f"Web server started at {scheme}://{self._server_manager.host}:{self._server_manager.port}/",
                )
            except Exception as e:
                self.log(logging.ERROR, f"Failed to start web server: {e}")
        else:
            try:
                self.winfo_toplevel().clear_preview()
                self._server_manager.stop()
                self.server_btn.config(text="Start Server")
                self._update_status()
                self.log(logging.INFO, "Web server stopped")
            except Exception as e:
                self.log(logging.ERROR, f"Failed to stop web server: {e}")

    def _on_cache(self):
        cache = self._server_manager.latest_metadata
        self.log(logging.WARNING, f"Latest cache metadata: {cache}")

    def activate(self):
        super().activate()
        self._update_status()
