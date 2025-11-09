from tkinter import ttk
from src.frames.base_frame import BaseFrame
from src.libs.converter import check_tool


class ToolFrame(BaseFrame):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.build_contents()

    def build_contents(self):
        self.main_frame = ttk.LabelFrame(self, text="Tool Status")
        self.main_frame.pack(fill="x")
        tool_keys = [("potrace", "Potrace")]
        for key, label in tool_keys:
            status = "✔️" if check_tool(key) else "❌"
            color = "red" if status == "❌" else "black"
            ttk.Label(
                self.main_frame, text=f"{label}: {status}", foreground=color
            ).pack(side="left", padx=8, pady=8)
