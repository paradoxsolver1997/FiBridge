from tkinter import ttk, filedialog
import tkinter as tk
from src.frames.base_frame import BaseFrame
import logging


class TextFrame(BaseFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.build_contents()

    def build_contents(self):

        self.text_frame = ttk.LabelFrame(self, text="Scanned Contents")
        self.text_frame.pack(fill="x", padx=8, pady=(4, 8))

        self.button_row = ttk.Frame(self.text_frame)
        self.button_row.pack(side="bottom", padx=8, pady=(0, 4))
        ttk.Button(
            self.button_row, text="Copy to Clipboard", command=self._on_copy
        ).pack(side="left", padx=(0, 4))
        ttk.Button(self.button_row, text="Save", command=self._on_save).pack(
            side="left"
        )
        ttk.Button(self.button_row, text="Clear", command=self._on_clear).pack(
            side="left", padx=(4, 0)
        )

        self.scanned_text = tk.Text(self.text_frame, height=10, wrap="word")
        self.scanned_text.pack(fill="both", expand=True, padx=8, pady=8)

    def _on_clear(self):
        self.scanned_text.delete("1.0", tk.END)

    def _on_copy(self):
        text = self.scanned_text.get("1.0", tk.END).strip()
        self.clipboard_clear()
        self.clipboard_append(text)
        self.update()  # Ensure clipboard content is available

    def _on_save(self):
        text = self.scanned_text.get("1.0", tk.END).strip()
        file_path = filedialog.asksaveasfilename(
            title="Save Text",
            defaultextension=".txt",
            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
        )
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(text)
            except Exception as e:
                self.log(logging.ERROR, f"Failed to save text: {e}")

    def set_text(self, text):
        """
        Display the text content in the scanned results text box.
        """
        if hasattr(self, "scanned_text") and self.scanned_text:
            self.scanned_text.delete("1.0", tk.END)
            self.scanned_text.insert(tk.END, text)
