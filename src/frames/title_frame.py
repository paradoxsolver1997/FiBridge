from tkinter import ttk
from src.frames.base_frame import BaseFrame


class TitleFrame(BaseFrame):
    def __init__(self, parent, title_text, comment_text=None, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        title_frame = ttk.LabelFrame(self, text=title_text, style="Bold.TLabelframe")
        title_frame.pack(fill="x", expand=True, pady=(4, 4), padx=(0, 2))
        if comment_text:
            # Support comment_text as a string or a list of strings
            if isinstance(comment_text, str):
                comment_texts = [comment_text]
            else:
                comment_texts = list(comment_text)
            for text in comment_texts:
                comment_row = ttk.Frame(title_frame)
                comment_row.pack(fill="x", padx=(0, 4), pady=(2, 2))
                ttk.Label(comment_row, text=text).pack(
                    fill="x", expand=True, padx=(6, 4), pady=(0, 0)
                )
